from flask import g
from mysql.connector import Error

from models import Note
from util.logger import Logger


class NotesHandler:
    @property
    def _dbConnection(self):
        return g.db

    def __init__(self):
        super().__init__()
        self.logging = Logger().get_logger()

    def checkIfNoteInTrip(self, tripId, noteId):
        note = self._dbConnection.session.query(Note).filter_by(tripId=tripId).filter_by(noteId=noteId).first()
        return note is not None

    def checkIfUserOwnsTrips(self, userId, noteId):
        note = self._dbConnection.session.query(Note).filter_by(noteId=noteId).filter_by(userId=userId).first()
        return note is not None

    def createNote(self, userId, tripId, note):
        try:
            newNote = Note(
                userId=userId,
                tripId=tripId,
                note=note
            )
            self._dbConnection.session.add(newNote)
            # Not sure if this is okay, check later
            self._dbConnection.session.commit()
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error creating new note: {e}")

    def editNote(self, noteId, note):
        try:
            # Fetch the note to update
            existingNote = self._dbConnection.session.query(Note).filter_by(noteId=noteId).first()

            if not existingNote:
                # If no expense found, return False
                return False
            existingNote.note = note
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error updating note for noteId {noteId}; error: {e}")
            return False

    def deleteNote(self, noteId):
        try:
            self._dbConnection.session.query(Note).filter(
                Note.noteId == noteId,
            ).delete()

            # Commit the transaction
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error deleting note: {e}")
            return False

    def fetchNotes(self, tripId, page):
        try:
            page_size = 10
            offset = (page - 1) * page_size

            total_items = self._dbConnection.session.query(Note).filter_by(tripId=tripId).count()
            total_pages = (total_items + page_size - 1) // page_size  # Ceiling division

            notes = (
                self._dbConnection.session.query(Note)
                .filter_by(tripId=tripId)
                .order_by(Note.noteId.desc())
                .limit(page_size)
                .offset(offset)
                .all()
            )

            return {
                'notes': [
                    {
                        'userId': note.userId,
                        'tripId': note.tripId,
                        'noteId': note.noteId,
                        'note': note.note,
                    }
                    for note in notes
                ],
                'totalItems': total_items,
                'currentPage': page,
                'totalPages': total_pages
            }

        except Error as e:
            self.logging.error(f"Error fetching notes for trip: {e}")
            return None

