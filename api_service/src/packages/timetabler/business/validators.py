from datetime import datetime
class Validators:

    @staticmethod
    def is_valid_str_time(time_str: str, time_format: str = "%I:%M %p") -> bool:
        """
        Validates if the given string is a valid time.
        :param time_str: The time string to validate.
        :param time_format: The format against which to validate the time string (default: "%I:%M %p").
        :return: True if valid, False otherwise.
        """
        try:
            # Parse the string with the given format
            datetime.strptime(time_str, time_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def pre_input_parse_validation(json_obj):
        pass

    @staticmethod
    def post_input_parse_validation(university_obj):
        pass
    