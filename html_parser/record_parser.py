from html.parser import HTMLParser
from typing import Type
from . import record


class RecordParser(HTMLParser):
    base_uri = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
    records = []
    dataTag = 'td'
    column = 0
    currentTag = ''
    withinTR = False
    collectData = False
    startCollectionAfterOne = 1
    case_number = ''  # column 1
    citation_number = []  # column 2
    info = []  # column 3
    date_location = []  # column 4
    type_status = []  # column 5
    charges = []  # column 6+
    case_detail_link = ''

    def record_reset(self):
        self.case_number = ''  # column 1
        self.citation_number = []  # column 2
        self.info = []  # column 3
        self.date_location = []  # column 4
        self.type_status = []  # column 5
        self.charges = []  # column 6+
        self.case_detail_link = ''

    def handle_starttag(self, tag, attrs):
        if tag == self.dataTag:
            self.column += 1
        if tag == 'a' and self.collectData:
            self.case_detail_link = self.base_uri + dict(attrs)['href']
        if tag == 'tr' and self.currentTag == 'tr':
            self.withinTR = True
        elif tag == 'tr':
            self.currentTag = tag

    def handle_endtag(self, tag):
        if tag == 'tr' and self.withinTR:
            self.withinTR = False
        elif tag == 'tr' and self.collectData:
            self.column = 0
            self.currentTag = ''
            current_record = record.Record(self.info, self.case_number, self.citation_number, self.date_location,
                                    self.type_status, self.charges, self.case_detail_link)
            self.records.append(current_record)
            self.record_reset()

    def handle_data(self, data):
        if self.currentTag == 'tr' and self.collectData:
            if self.column == 1:
                self.case_number = data

            elif self.column == 2:
                self.citation_number.append(data)

            elif self.column == 3:
                self.info.append(data)

            elif self.column == 4:
                self.date_location.append(data)

            elif self.column == 5:
                self.type_status.append(data)

            else:
                self.charges.append(data)

        if 'Charge(s)' == data:
            self.collectData = True

    # TODO: Handle parse errors. Notify user.
    def error(self, message):
        pass
