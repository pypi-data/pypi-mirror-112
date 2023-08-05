class manifestv1:
    def __init__(self, guid):
        self.format_version = 1
        self.guid = guid
        self.layouts = dict()

    def json(self):
        d = {
            'format-version': self.format_version,
            'guid': self.guid,
        }
        return ''
