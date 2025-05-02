from dbHandlers.noteHandler import NotesHandler


class NotesService:
    Handler: NotesHandler

    def __init__(self, notesHandler: NotesHandler):
        self.Handler = notesHandler

    def fetchNotesForATrip(self, tripId: str, page: int):
        return self.Handler.fetchNotes(tripId, page)

    def createNote(self, postData: dict):
        userId = postData.get('userId')
        tripId = postData.get('tripId')
        note = postData.get('note')
        return self.Handler.createNote(userId, tripId, note)

    def editNote(self, postData):
        userId = postData.get('userId')
        tripId = postData.get('tripId')
        note = postData.get('note')
        noteId = postData.get('noteId')
        if not self.checkIfNoteBelongsToTrip(tripId, noteId) or not self.checkIfUserOwnsTrips(userId, noteId):
            return False
        return self.Handler.editNote(noteId, note)

    def deleteNote(self, userId, tripId, noteId):
        if not self.checkIfNoteBelongsToTrip(tripId, noteId) or not self.checkIfUserOwnsTrips(userId, noteId):
            return False
        return self.Handler.deleteNote(noteId)

    def checkIfNoteBelongsToTrip(self, tripId, noteId):
        return self.Handler.checkIfNoteInTrip(tripId, noteId)

    def checkIfUserOwnsTrips(self, userId, noteId):
        return self.Handler.checkIfUserOwnsTrips(userId, noteId)
