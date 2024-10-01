class Audio:
    def __init__(self, ID, title, file_name, description, BPM, genre, audio_type ):
        self._ID = ID
        self._title = title
        self._file_name = file_name
        self._description = description
        self._BPM = BPM
        self._genre = genre
        self._audio_type = audio_type

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def description(self):
        return self._descripcion

    @description.setter
    def description(self, descripcion):
        self._description = descripcion

    @property
    def BPM(self):
        return self._BPM

    @BPM.setter
    def BPM(self, BPM):
        self._BPM = BPM

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        self._genre = genre

    @property
    def audio_type(self):
        return self._audio_type

    @audio_type.setter
    def audio_type(self, audio_type):
        self._audio_type = audio_type