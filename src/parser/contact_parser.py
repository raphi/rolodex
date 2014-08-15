import logging

from src.formater import contact_format
from src.formater.contact_format import ContactFormat


class ContactParseError(Exception):
    """
    Custom exception raise by the ContactParser when parser the input fails
    :param message: information about the error
    :param failing_entry: failing input
    """

    def __init__(self, message, failing_entry):
        Exception.__init__(self, message)
        self.failing_entry = failing_entry


class ContactParser(object):
    """
    ContactParser defines a list of valid formats, based on regex.
    Default regex parts can be used or extended.
    You can define here additional valid formats reusing the default regex part or using your own regex.
    :param formats: you can provide your own custom formats. Uses 3 pre-defined formats by default
    """

    def __init__(self, formats=None):
        if formats:
            self.formats = formats
        else:
            self.formats = [ContactFormat([contact_format.RE_LAST_NAME,
                                           contact_format.RE_FIRST_NAME,
                                           contact_format.RE_PHONE,
                                           contact_format.RE_COLOR,
                                           contact_format.RE_ZIPCODE]),
                            ContactFormat([contact_format.RE_FIRST_NAME,
                                           contact_format.RE_LAST_NAME,
                                           contact_format.RE_ZIPCODE,
                                           contact_format.RE_PHONE,
                                           contact_format.RE_COLOR]),
                            ContactFormat([contact_format.RE_FIRST_NAME + " " + contact_format.RE_LAST_NAME,
                                           contact_format.RE_COLOR,
                                           contact_format.RE_ZIPCODE,
                                           contact_format.RE_PHONE])]

    def parse(self, entry):
        """
        Parse the given entry according to the defined valid formats
        :param entry: text entry to parse
        :return: Contact if the entry is considered a valid input by the allowed pre-defined formats
        :raise ContactParseError: the entry is not valid according to the pre-defined formats
        """
        for valid_format in self.formats:
            contact = valid_format.get_match(entry)

            if contact:
                logging.debug("Contact successfully parsed: %s" % contact)
                return contact

        raise ContactParseError("Could not parse given input: %s" % entry, entry)
