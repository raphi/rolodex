import re
import logging

from src.models.contact import Contact


# Default regex. You can use it, improve it or use your own.
RE_SEPARATOR = ", "
RE_COLOR = "(?P<color>[\sa-z]+)"
RE_FIRST_NAME = "(?P<firstname>[a-z\-\s\.]+)"
RE_LAST_NAME = "(?P<lastname>[a-z\-\s\.]+)"
RE_PHONE = "(?P<phonenumber>[()\-\d\s\+]{10,15})"
RE_ZIPCODE = "(?P<zipcode>\d{5})"


class ContactFormatError(Exception):
    """
    Custom exception raise by the ContactFormat class when the ContactFormat rules are not valid.
    Usually, it means that Contact required attributes (firstname, lastname, phone, zipcode, color) are missing
    in the regex.
    :param message: information about the error
    :param regex: the failing regex
    """

    def __init__(self, message, regex):
        Exception.__init__(self, message)
        self.regex = regex


class ContactFormat(object):
    """
    ContactFormat class defines one valid pattern for the parser engine.
    It takes a list of regex patterns in order to create one finalized regex pattern.
    get_match()
    :param formats: list of default or custom regex patterns
    :param flags: See re module allowed flags
    :param separator: a separator used to join the list of formats
    """

    def __init__(self, formats, flags=re.IGNORECASE, separator=RE_SEPARATOR):
        # Join the different parts of the regex into one single regex with a defined separator
        regex = separator.join(formats)

        # Final full regex
        self.regex = re.compile("^" + regex + "$", flags)

        logging.debug("Regex contact format applied: %s with flags: %s" % (self.regex.pattern, self.regex.flags))

    def get_match(self, entry):
        """
        Main function that executes the matching between the given entry and the defined pattern
        :param entry: the input to parse against this ContactFormat pattern
        :return: a Contact object if the match is successful or None if the entry does not conform to this ContactFormat
        :raise ContactFormatError: Exception raise if the match is successful but the regex is incorrect because
        it's missing one or multiple required Contact attributes
        """

        # Perform the regex matching
        match = self.regex.match(entry)

        if match:
            try:
                # Get the regex named groups in a dictionary
                match_dict = match.groupdict()

                # Extract regex named groups and create a Contact object
                contact = Contact(match_dict["firstname"],
                                  match_dict["lastname"],
                                  match_dict["phonenumber"],
                                  match_dict["color"],
                                  match_dict["zipcode"])

                return contact
            except:
                # We assume that a valid contact needs all attributes
                raise ContactFormatError("ContactFormat regex is invalid. "
                                         "It's missing a required Contact attribute: %s" % self.regex.pattern,
                                         self.regex)

        # No match according to this ContactFormat pattern
        return None