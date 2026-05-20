"""
Tiny FX rate fetcher with in-process TTL cache.

Source: the same free `@fawazahmed0/currency-api` JSON feed the frontend
uses. We pull the INR-base table and convert anything to INR with one
lookup. Cache is process-local with a 5-minute TTL; for a single-box
deploy that's fine.
"""
import logging
import time
from threading import Lock
from urllib.request import urlopen
import json

logger = logging.getLogger(__name__)

_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/inr.json"
_TTL_SECS = 300

_cache = {"at": 0.0, "rates": None}
_lock = Lock()


def _fetch():
    with urlopen(_URL, timeout=8) as resp:
        data = json.loads(resp.read())
    # The feed shape is {"date": "...", "inr": {"usd": 0.012, "eur": 0.011, ...}}
    return data.get("inr") or {}


def get_rates():
    """Return the dict of {currency_code -> units per 1 INR}, or {} on failure."""
    now = time.time()
    if _cache["rates"] is not None and (now - _cache["at"]) < _TTL_SECS:
        return _cache["rates"]
    with _lock:
        # double-check after acquiring lock
        if _cache["rates"] is not None and (time.time() - _cache["at"]) < _TTL_SECS:
            return _cache["rates"]
        try:
            rates = _fetch()
            _cache["rates"] = rates
            _cache["at"] = time.time()
            return rates
        except Exception as e:
            logger.warning("FX fetch failed: %s", e)
            # Fall back to a stale cache if we have one.
            return _cache["rates"] or {}


def to_inr(amount, currency):
    """
    Convert `amount` denominated in `currency` (e.g. 'eur', 'usd') to INR.
    Returns a float. Raises ValueError on unknown currency or no rates.
    """
    if amount is None:
        raise ValueError("amount is required")
    currency = (currency or "inr").lower().strip()
    if currency == "inr":
        return float(amount)
    rates = get_rates()
    if not rates:
        raise ValueError("FX rates unavailable; please retry in a moment")
    rate = rates.get(currency)
    if not rate:
        raise ValueError(f"unknown currency '{currency}'")
    # rate = units of `currency` per 1 INR, so dividing converts the other way.
    return float(amount) / float(rate)
