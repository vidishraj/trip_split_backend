from sqlalchemy.exc import SQLAlchemyError
from flask import g

from models import ChatMessage, User
from util.logger import Logger


class ChatHandler:
    """Persistence for the trip-shared assistant transcript."""

    @property
    def _db(self):
        return g.db

    def __init__(self):
        super().__init__()
        self.logging = Logger().get_logger()

    def append(self, trip_id, user_id, role, content, image_count=0):
        try:
            msg = ChatMessage(
                tripId=trip_id,
                userId=user_id,
                role=role,
                content=content,
                imageCount=image_count,
            )
            self._db.session.add(msg)
            self._db.session.commit()
            return msg.id
        except SQLAlchemyError as e:
            self._db.session.rollback()
            self.logging.error(f"chat append failed: {e}")
            return None

    def fetch_for_trip(self, trip_id, limit=200):
        """Return last `limit` messages (oldest first) joined with the
        sender's display name. Assistant turns return userName=None."""
        try:
            rows = (
                self._db.session.query(
                    ChatMessage.id,
                    ChatMessage.role,
                    ChatMessage.content,
                    ChatMessage.imageCount,
                    ChatMessage.createdAt,
                    ChatMessage.userId,
                    User.userName,
                )
                .outerjoin(User, ChatMessage.userId == User.userId)
                .filter(ChatMessage.tripId == trip_id)
                .order_by(ChatMessage.id.desc())
                .limit(limit)
                .all()
            )
            return list(reversed([
                {
                    'id': r.id,
                    'role': r.role,
                    'content': r.content,
                    'imageCount': r.imageCount,
                    'createdAt': r.createdAt.isoformat() if r.createdAt else None,
                    'userId': r.userId,
                    'userName': r.userName,
                }
                for r in rows
            ]))
        except SQLAlchemyError as e:
            self.logging.error(f"chat fetch failed: {e}")
            return []

    def fetch_recent_for_model(self, trip_id, limit=20):
        """Compact form fed to the model — role + content + sender name."""
        try:
            rows = (
                self._db.session.query(
                    ChatMessage.role,
                    ChatMessage.content,
                    User.userName,
                )
                .outerjoin(User, ChatMessage.userId == User.userId)
                .filter(ChatMessage.tripId == trip_id)
                .order_by(ChatMessage.id.desc())
                .limit(limit)
                .all()
            )
            return list(reversed([
                {
                    'role': r.role,
                    'content': r.content,
                    'userName': r.userName,
                }
                for r in rows
            ]))
        except SQLAlchemyError as e:
            self.logging.error(f"chat fetch-for-model failed: {e}")
            return []
