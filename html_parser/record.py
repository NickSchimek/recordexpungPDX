class Record:

    def __init__(self, info, case_number, citation_number, date_location, type_status, charges, case_detail_link):
        self.info = info  # List:   name and dob
        self.case_number = case_number  # String: case number
        self.citation_number = citation_number  # List:   citation numbers
        self.date_location = date_location  # List:   location and date of incident
        self.type_status = type_status  # List:   violation type, and current status
        self.charges = charges  # List:   charges.
        self.case_detail_link = case_detail_link
