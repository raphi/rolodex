"""
Simple Contact object
"""


class Contact(object):
    """
    All fields are required.
    :param first_name: user first name
    :param last_name: user last name
    :param phone: user 10 digits phone number. This attribute is formatted to: 424-4242-4242
    :param color: user color
    :param zipcode: user 5 digits zipcode
    """

    def __init__(self, first_name, last_name, phone, color, zipcode):
        self.firstname = first_name
        self.lastname = last_name
        self.phonenumber = self.format_phone(phone)
        self.color = color
        self.zipcode = zipcode

    @staticmethod
    def format_phone(phone):
        # Custom phone number formatting
        clean_phonenumber = phone.replace(" ", "").replace("-", "").replace(",", "").replace(".", "").replace("(", "").replace(")", "")
        return format(int(clean_phonenumber[:-1]), ",").replace(",", "-") + clean_phonenumber[-1]

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)