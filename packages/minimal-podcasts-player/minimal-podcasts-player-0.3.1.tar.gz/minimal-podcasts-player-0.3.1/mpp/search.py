from urllib.request import urlopen
import urllib.parse
from PyQt5.QtCore import pyqtSignal, QThread, QVariant
import json


class itunes(QThread):
    data = pyqtSignal(QVariant)
    baseUrl = 'https://itunes.apple.com/search'

    def __init__(self, terms):
        super().__init__()
        self.terms = terms

    def run(self):
        data = {}
        data['term'] = self.terms
        data['media'] = 'podcast'
        url_values = urllib.parse.urlencode(data)
        full_url = self.baseUrl + '?' + url_values
        with urlopen(full_url) as response:
            rawData = response.read().decode('utf-8')
            data = json.loads(rawData)
            for result in data['results']:
                if 'feedUrl' in result:
                    self.data.emit(result)
