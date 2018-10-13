## Author: Nick Schimek
## Python version 3.7.0
## Parses HTML from OJCIN and creates a record for each row in the table.


from html.parser import HTMLParser

class Record():

  def __init__(self, info, case_number, citation_number, date_location, type_status, charges):
      self.info            = info            # List:   name and dob
      self.case_number     = case_number     # String: case number
      self.citation_number = citation_number # List:   citation numbers
      self.date_location   = date_location   # List:   location and date of incident
      self.type_status     = type_status     # List:   violation type, and current status
      self.charges         = charges         # List:   charges.

class MyHTMLParser(HTMLParser):
    records = []
    dataTag = 'td'
    column = 0
    currentTag = ''
    withinTR = False
    collectData = False
    startCollectionAfterOne = 1
    case_number     = '' # column 1
    citation_number = [] # column 2
    info            = [] # column 3
    date_location   = [] # column 4
    type_status     = [] # column 5
    charges         = [] # column 6+

    count = 0

    def record_reset(self):
        self.case_number     = '' # column 1
        self.citation_number = [] # column 2
        self.info            = [] # column 3
        self.date_location   = [] # column 4
        self.type_status     = [] # column 5
        self.charges         = [] # column 6+

    def handle_starttag(self, tag, attrs):
        if (tag == self.dataTag):
            self.column += 1
        if (tag == 'tr' and self.currentTag == 'tr'):
            self.withinTR = True
        elif (tag == 'tr'):
            self.currentTag = tag

    def handle_endtag(self, tag):
        if (tag == 'tr' and self.withinTR):
            self.withinTR = False
        elif (tag == 'tr'and self.collectData):
            self.column = 0
            self.currentTag = ''
            record = Record(self.info, self.case_number, self.citation_number, self.date_location, self.type_status, self.charges)
            self.records.append(record)
            #print("")


    def handle_data(self, data):
        #print("Encountered some data:", data)
        if (self.currentTag == 'tr' and self.collectData):
            if (self.column == 1):
                self.case_number = data

            elif (self.column == 2):
                self.citation_number.append(data)

            elif (self.column == 3):
                self.info.append(data)

            elif (self.column == 4):
                self.date_location.append(data)

            elif (self.column == 5):
                self.type_status.append(data)
            else:
                self.count += 1
                self.charges.append(data)

                self.record_reset()

        if ('Charge(s)' == data):
            self.collectData = True



parser = MyHTMLParser()
parser.feed('''
Paste in source HTML here. Right click on web page and select view source.
copy and paste here.
'''
)

## Remove first and last record, The first one is duplicate due to when I turn on collection the last is empty.
del parser.records[0]
del parser.records[-1]


print("Number of records", len(parser.records), "\n")

count = 0
for record in parser.records:
    count += 1
    print("Record number:", count)
    print(record.info)
    print(record.case_number)
    print(record.citation_number)
    print(record.date_location)
    print(record.type_status)
    print(record.charges)
    print("\n--------------------------------------------------------------\n")
