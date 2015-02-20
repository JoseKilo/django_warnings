
class DjangoWarning(Warning):
    def __init__(self, message=None, identifier=None, url_params=None):
        self.message = message or 'Unknown Warning'
        self.identifier = identifier
        self.url_params = url_params
