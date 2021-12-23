from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__
