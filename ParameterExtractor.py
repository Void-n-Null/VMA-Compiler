import json

class ParameterExtractor:

    @staticmethod
    def extract_parameters(parameters_str: str) -> list:
        # Extract dictionaries from the parameter string
        extracted_dict, parameters_str = ParameterExtractor._extract_dict(parameters_str)

        # Split parameters and convert them to their respective types
        parameters = [
            ParameterExtractor._convert_parameter(param)
            for param in parameters_str.split(',')
        ]

        # Replace placeholders with the actual extracted dictionaries
        parameters = [
            param if param != 'DICTPLACEHOLDER' else extracted_dict
            for param in parameters
        ]

        return parameters

    @staticmethod
    def _convert_parameter(param: str):
        """Converts a parameter string to its respective data type."""
        if param.isdigit():
            return int(param)
        if param.replace('.', '', 1).isdigit():
            return float(param)
        if param == 'DICTPLACEHOLDER':
            return param
        # Attempt to convert the parameter to a dictionary
        try:
            return json.loads(param)
        except json.JSONDecodeError:
            # Strip surrounding quotes if present
            return param.strip('"').strip("'")

    @staticmethod
    def _extract_dict(s: str) -> (dict, str):
        """Extracts the first dictionary from a string and returns the dictionary and the modified string."""
        start, end = s.find('{'), s.rfind('}')
        if start != -1 and end != -1:
            # Extract the substring that represents the dictionary
            dict_str = s[start:end + 1]
            try:
                extracted_dict = json.loads(dict_str)
                # Replace the dictionary in the original string with a placeholder
                s = s.replace(dict_str, 'DICTPLACEHOLDER')
                return extracted_dict, s
            except json.JSONDecodeError:
                pass
        return {}, s
