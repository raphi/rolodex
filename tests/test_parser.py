import unittest

from src.parser.contact_parser import ContactParser, ContactParseError
from src.formater import contact_format
from src.formater.contact_format import ContactFormat
from src.models.contact import Contact


class ParserTest(unittest.TestCase):
    """
    Testing the Parser functionalities and behavior.
    The default Parser must respect the 3 allowed format and reject entries that don't match the pattern.
    The Parser also needs to be flexible in order to add/implement custom new formats.
    """
    def setUp(self):
        self.parser = ContactParser()

    def test_invalid_formats(self):
        self.assertRaises(ContactParseError, self.parser.parse, "0.358358554738")
        self.assertRaises(ContactParseError, self.parser.parse, "13121, Gustavson, Natashia, (491)-571-5970, blue")
        self.assertRaises(ContactParseError, self.parser.parse, "(555)-111-1111, Won, George, aqua marine, 77594")
        self.assertRaises(ContactParseError, self.parser.parse, "red, Shanika, Rodh, (709)-353-2921, 60864")
        self.assertRaises(ContactParseError, self.parser.parse, "Rachele Maze, 64938, 607 089 6760")
        self.assertRaises(ContactParseError, self.parser.parse, "Rachele Maze, 607 089 6760")
        self.assertRaises(ContactParseError, self.parser.parse, "Magaly, , 64568, 289 471 3436, blue")
        self.assertRaises(ContactParseError, self.parser.parse, "Maurita, Awong, 16296, 191 933 8599, ")

    def test_valid_formats(self):
        self.assertIsInstance(self.parser.parse("Lastname, Firstname, (703)-742-0996, Blue, 10013"), Contact)
        self.assertIsInstance(self.parser.parse("Firstname Lastname, Red, 11237, 703 955 0373"), Contact)
        self.assertIsInstance(self.parser.parse("Firstname, Lastname, 10013, 646 111 0101, Green"), Contact)
        self.assertIsInstance(self.parser.parse("Rachele Maze, pink, 64938, 607 089 6760"), Contact)
        self.assertIsInstance(self.parser.parse("Booker T., Washington, 87360, 373 781 7380, yellow"), Contact)
        self.assertIsInstance(self.parser.parse("James Murphy, yellow, 83880, 018 154 6474"), Contact)
        self.assertIsInstance(self.parser.parse("Maurita, Awong, 16296, 191 933 8599, blue"), Contact)

    def test_custom_format(self):
        # Define a new format using default regex
        custom_format = [ContactFormat([contact_format.RE_PHONE,
                                        contact_format.RE_COLOR,
                                        contact_format.RE_ZIPCODE,
                                        contact_format.RE_LAST_NAME,
                                        contact_format.RE_FIRST_NAME])]

        # Create the custom parser
        custom_parser = ContactParser(formats=custom_format)

        self.assertRaises(ContactParseError, custom_parser.parse, "(555)-111-1111, Won, George, aqua marine, 77594")

        entry = "191 933 8599, pink, 10036, Maurita, Awong"

        # Valid entry defined in the new parser rules
        self.assertIsInstance(custom_parser.parse(entry), Contact)

        # Invalid entry using the regular default parser rules
        self.assertRaises(ContactParseError, self.parser.parse, entry)

    def test_custom_regex(self):
        # Defining custom sub-regex that do not make a lot of sense IRL
        re_color = "(?P<color>red?)"
        re_first_name = "(?P<firstname>[a-z]+)"
        re_last_name = "(?P<lastname>[a-z]+)"
        re_phone = "(?P<phonenumber>[()\-\d]{6})"
        re_zipcode = "(?P<zipcode>\d{3})"

        # Define a new format using custom regex
        custom_format = [ContactFormat([re_color, re_first_name, re_last_name, re_phone, re_zipcode], separator="#")]

        # Create the custom parser
        custom_parser = ContactParser(formats=custom_format)

        self.assertRaises(ContactParseError, custom_parser.parse, "(555)-111-1111, Won, George, aqua marine, 77594")

        entry = "red#Francis#Rougemont#123456#424"

        # Valid entry defined in the new parser rules
        self.assertIsInstance(custom_parser.parse(entry), Contact)

        # Invalid entry using the regular default parser rules
        self.assertRaises(ContactParseError, self.parser.parse, entry)
