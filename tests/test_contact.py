import unittest

from src.models.contact import Contact


class ContactTest(unittest.TestCase):

    def test_simple_contact(self):
        """
        Check that the values used to create the Contact object are usable and not modified
        """
        contact = Contact("Raphael", "Daguenet", "456-987-7890", "blue", "10036")

        self.assertEqual(contact.firstname, "Raphael")
        self.assertEqual(contact.lastname, "Daguenet")
        self.assertEqual(contact.phonenumber, "456-987-7890")
        self.assertEqual(contact.color, "blue")
        self.assertEqual(contact.zipcode, "10036")

    def test_phone_formatting(self):
        """
        Check that phone number is always formatted to: 111-111-1111
        """
        contact = Contact("Raphael", "Daguenet", "456 987 7890", "blue", "10036")
        self.assertEqual(contact.phonenumber, "456-987-7890")

        contact = Contact("Raphael", "Daguenet", "456.987.7890", "blue", "10036")
        self.assertEqual(contact.phonenumber, "456-987-7890")

        contact = Contact("Raphael", "Daguenet", "456 987 7890", "blue", "10036")
        self.assertEqual(contact.phonenumber, "456-987-7890")

        contact = Contact("Raphael", "Daguenet", "(456) 987-7890", "blue", "10036")
        self.assertEqual(contact.phonenumber, "456-987-7890")
