class Purchase:
    def __init__(self, ID, id_buyer, items, checkout_flow, status):
        self._ID = ID
        self._id_buyer = id_buyer
        self._items = items
        self._checkout_flow = checkout_flow
        self._status = status

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def items(self):
        return self._items

    @items.setter
    def _items(self, _items):
        self._items = _items

    @property
    def id_buyer(self):
        return self._id_buyer

    @id_buyer.setter
    def id_buyer(self, id_buyer):
        self._id_buyer = id_buyer

    @property
    def checkout_flow(self):
        return self._checkout_flow

    @checkout_flow.setter
    def checkout_flow(self, checkout_flow):
        self._checkout_flow = checkout_flow

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
