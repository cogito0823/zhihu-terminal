class SpiderBaseclass(object):
    
    def __init__(self, client):
        self.client = client
        self.logger = self.client.logger