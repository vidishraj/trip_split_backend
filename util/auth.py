from functools import wraps
from flask import request, jsonify, g
from firebase_admin import auth


def require_auth(fn):
    """Verify the Firebase ID token and attach user_email to flask.g."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get('Authorization', '')
        if not header.startswith('Bearer '):
            return jsonify({"Error": "Auth info missing."}), 403
        try:
            decoded = auth.verify_id_token(header.split(' ', 1)[1])
        except Exception as ex:
            return jsonify({"Error": f"Auth failed: {ex}"}), 403
        user_email = decoded.get('email')
        if not user_email:
            return jsonify({"Error": "Auth failed."}), 403
        g.user_email = user_email
        return fn(*args, **kwargs)
    return wrapper


def require_trip_auth(trip_id_source):
    """
    Run after require_auth. Resolves a tripId via `trip_id_source(request)`
    and enforces that the authed user belongs to that trip.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            trip_id = trip_id_source(request)
            if not trip_id:
                return jsonify({"Error": "Missing tripId."}), 400
            if not self.tripUserService.checkIfUserHasAuthority(g.user_email, trip_id):
                return jsonify({"Error": "User does not has Auth."}), 403
            g.trip_id = trip_id
            return fn(self, *args, **kwargs)
        return wrapper
    return decorator
