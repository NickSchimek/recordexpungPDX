class FinancialTableData:

    def __init__(self):
      self._header_tag = 'b'
      self._parse_balance = False

    def store_data(self, case_parser, data):
        if self._parse_balance:
            case_parser.balance_due = data
            self._parse_balance = False

    def check_tag(self, tag):
      if self._header_tag == tag:
          self._parse_balance = True
