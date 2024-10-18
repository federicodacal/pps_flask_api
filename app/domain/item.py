class Item:
    def __init__(self, ID, id_audio, id_creator, price, status):
        self._ID = ID
        self._id_audio = id_audio
        self._id_creator = id_creator
        self._price = price
        self._status = status

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def id_audio(self):
        return self._id_audio

    @id_audio.setter
    def id_audio(self, id_audio):
        self._id_audio = id_audio

    @property
    def id_creator(self):
        return self._id_creator

    @id_creator.setter
    def id_creator(self, id_creator):
        self._id_creator = id_creator

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self.status = status
