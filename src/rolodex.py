import argparse
import logging
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.parser.contact_parser import ContactParser, ContactParseError
from src.export.export_to_json import ExportToJson


__author__ = "Raphael Daguenet <raphael.daguenet@gmail.com>"
__status__ = "production"
__version__ = "1.0.0"
__date__ = "05 August 2014"


def rolodex(input_file_path, output_file_path):
    """
    Rolodex takes entries of personal information in multiple formats from the given input file and
    normalizes each entry into a standard JSON format
    :param input_file_path: input file to parse
    :param output_file_path: optional: save the results to the output file
    """
    parser = ContactParser()
    extracted_contacts = []
    parse_errors_indexes = []

    try:
        with open(input_file_path) as input_file:
            for index, line in enumerate(input_file):
                try:
                    # Remove line breaks at the end of the entry
                    contact = parser.parse(line.rstrip())
                    # The parser found a valid contact, we add it to the final list
                    extracted_contacts.append(contact)
                except ContactParseError, e:
                    logging.warn(e)
                    # We keep track of the line index in case of an error
                    parse_errors_indexes.append(index)
                except Exception, e:
                    logging.error(e)

        # Export the results and errors indexes to JSON
        ExportToJson.export_contacts(extracted_contacts, parse_errors_indexes, output_file_path)

        logging.info("nb contacts extracted: %s" % len(extracted_contacts))
        logging.info("nb invalid input: %s" % len(parse_errors_indexes))
    except IOError, e:
        logging.error(e)


def main():
    """
    Main program entry point.
    Defines and get the program's arguments and then execute the program's logic calling rolodex() function
    """
    verbose = ["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"]

    parser = argparse.ArgumentParser(description="Rolodex parses the input file and extract contact information. "
                                                 "You can specify the output file where to save the JSON results. "
                                                 "Or you can omit this option and specify verbosity level to DEBUG.")
    parser.epilog = "Example: python rolodex.py -f sample.in -o result.out"
    parser.add_argument("-f", "--file", help="input file to parse", required=True)
    parser.add_argument("-o", "--output", help="output file to save the JSON results", required=False)
    parser.add_argument("-v", "--verbose", help="verbosity level: %s" % verbose, required=False)
    args = vars(parser.parse_args())

    if args["verbose"] and args["verbose"].upper() in verbose:
        logging.basicConfig(level=args["verbose"].upper())
    else:
        # Default logging level
        logging.basicConfig(level=logging.FATAL)

    input_file_path = args["file"]
    output_file_path = args["output"] if args["output"] else None

    rolodex(input_file_path, output_file_path)


if __name__ == "__main__":
    main()