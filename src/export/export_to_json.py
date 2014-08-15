import json
import logging
import operator


class ExportToJson(object):
    """
    ExportToJson class provides a static method to export the results into a valid JSON format.
    """

    def __init__(self):
        pass

    @staticmethod
    def export_contacts(contacts, indexes_parse_errors, output_file_path=None):

        """

        :param contacts: list of Contact objects
        :param indexes_parse_errors: list of indexes representing the indexes failing entries
        :param output_file_path: optional file path to write the JSON results in (using 'w' write mode)
        :return None if failed or the JSON string
        """
        json_results = None

        try:
            # Get the dictionary definition of Contact objects in order to be serializable by the json Encoder
            contacts_dict = [contact.__dict__ for contact in contacts]

            # Sort the contact list by ascending alphabetical order by Lastname first then Firstname
            contacts_dict.sort(key=operator.itemgetter("lastname", "firstname"))

            # Construct the final result dictionary
            results = {"entries": contacts_dict,
                       "errors": indexes_parse_errors}

            # Get the results formatted in correct JSON
            json_results = json.dumps(results, sort_keys=True, indent=2, separators=(',', ': '))

            logging.debug(json_results)

            # If the output file option is provided, we save the JSON results in the specified file
            if output_file_path:
                open(output_file_path, 'w').write(json_results)
                logging.info("Results saved in JSON format in %s" % output_file_path)
        except IOError, e:
            logging.error(e)
            logging.error("The results have NOT been saved")
        except Exception, e:
            logging.error(e)

        return json_results