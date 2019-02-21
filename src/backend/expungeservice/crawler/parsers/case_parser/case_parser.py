import re

from html.parser import HTMLParser

from expungeservice.crawler.parsers.case_parser.charge_table_data import ChargeTableData
from expungeservice.crawler.parsers.case_parser.event_table_data import EventTableData
from expungeservice.crawler.parsers.case_parser.financial_table_data import FinancialTableData
from expungeservice.crawler.parsers.case_parser.default_state import DefaultState


class CaseParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._table_title = ''
        self._within_table_header = False
        self._charge_table_data = []
        self._event_table_data = []

        self.balance_due = '0'
        self.hashed_dispo_data = {}
        self.hashed_charge_data = {}

        self._current_parser_state = DefaultState()

    def handle_starttag(self, tag, attrs):
        if CaseParser.__at_table_title(tag, attrs):
            self._within_table_header = True
            self._current_parser_state = DefaultState()
        self._current_parser_state.check_tag(tag)

    def handle_endtag(self, tag):
        charge_table = 'Charge Information'
        event_table = 'Events & Orders of the Court'
        financial_table = 'Financial Information'

        if self.__exiting_table_header(tag):
            self._within_table_header = False
            if charge_table == self._table_title:
                self._current_parser_state = ChargeTableData()
            elif event_table == self._table_title:
                self._current_parser_state = EventTableData()
            elif financial_table == self._table_title:
                self._current_parser_state = FinancialTableData()

        if self.__end_of_file(tag):
            self.__format_dispo_data()
            self.__create_charge_hash()

    def handle_data(self, data):
        self._current_parser_state.store_data(self, data)

    # TODO: Add error handling.
    def error(self, message):
        pass

    # Private methods

    @staticmethod
    def __at_table_title(tag, attrs):
        return tag == 'div' and dict(attrs).get('class') == 'ssCaseDetailSectionTitle'

    def __exiting_table_header(self, end_tag):
        return self._within_table_header and end_tag == 'tr'

    def __end_of_file(self, tag):
        return tag == 'body'

    def __format_dispo_data(self):
        dispo_data = self.__filter_dispo_events()
        for dispo_row in dispo_data:
            start_index = 2
            if len(dispo_row[3].split('.\xa0')) == 2:
                start_index = 3

            while start_index < len(dispo_row) - 1:
                charge_id, charge = dispo_row[start_index].split('.\xa0')
                charge_id = int(charge_id)
                self.hashed_dispo_data[charge_id] = {}
                self.hashed_dispo_data[charge_id]['date'] = dispo_row[0]
                self.hashed_dispo_data[charge_id]['charge'] = charge
                self.hashed_dispo_data[charge_id]['ruling'] = dispo_row[start_index + 1]
                start_index += 2

    def __filter_dispo_events(self):
        dispo_list = []
        for event_row in self._event_table_data:
            if len(event_row) > 3 and event_row[3] == 'Disposition':
                dispo_list.append(event_row)

        result = []
        index = 0
        for dispo_row in dispo_list:
            result.append([])
            for data in dispo_row:
                if data != '\xa0':
                    result[index].append(data)
            index += 1

        return result

    def __create_charge_hash(self):
        index = 0
        while index < len(self._charge_table_data):
            charge_id = int(re.compile('\d*').match(self._charge_table_data[index]).group())
            self.hashed_charge_data[charge_id] = {}
            self.hashed_charge_data[charge_id]['name'] = self._charge_table_data[index + 1]
            self.hashed_charge_data[charge_id]['statute'] = self._charge_table_data[index + 2]
            self.hashed_charge_data[charge_id]['level'] = self._charge_table_data[index + 3]
            self.hashed_charge_data[charge_id]['date'] = self._charge_table_data[index + 4]
            index += 5
