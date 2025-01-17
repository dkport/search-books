import json
from types import SimpleNamespace


class ParseResponse:
    """
    A utility class to parse a string input into a JSON object or raw text.

    This class provides a method to determine if the input string is valid JSON
    and parses it accordingly. If the input is not valid JSON, it is treated as raw text.
    """

    @staticmethod
    def run(input_string):
        """
        Parses the input string to determine if it is valid JSON or raw text.

        Args:
            input_string (str or dict): The input to parse. Can be a JSON string, a dictionary, 
                                        or raw text.

        Returns:
            SimpleNamespace: An object with two attributes:
                - is_json (bool): Indicates if the input was successfully parsed as JSON.
                - data: The parsed JSON object if `is_json` is True, otherwise the raw text.
        """
        result = SimpleNamespace()
        try:
            # If it's already a dict, set is_json directly
            if isinstance(input_string, dict):
                result.is_json = True
                result.data = input_string
            else:
                # Attempt to parse as JSON
                result.is_json = True
                result.data = json.loads(input_string)
        except ValueError:
            # Not valid JSON
            result.is_json = False
            result.data = input_string
        return result
