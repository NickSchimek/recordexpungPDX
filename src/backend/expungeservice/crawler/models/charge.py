from expungeservice.crawler.models.disposition import Disposition
from expungeservice.crawler.models.expungement_result import ExpungementResult


class Charge:

    def __init__(self, name, statute, level, date):
        self.name = name
        self.statute = statute
        self.level = level
        self.date = date
        self.disposition = Disposition()
        self.expungement_result = ExpungementResult()
