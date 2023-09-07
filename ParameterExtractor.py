import contextlib
import json
import ErrorLog
from collections import deque
class ParameterExtractor:

    @staticmethod
    def extract_parameters(parameters_str: str) -> list:
        parameters = []
        stack = deque()
        temp_str = ""

        for char in parameters_str:
            if char == '{':
                stack.append('{')
                temp_str += char
            elif char == '}':
                if not stack or stack[-1] != '{':
                    ErrorLog.ReportError("Unmatched closing brace detected.")
                else:
                    stack.pop()
                    temp_str += char
                    if not stack:
                        parameters.append(ParameterExtractor._convert_parameter(temp_str.strip()))
                        temp_str = ""
            elif char == ',' and not stack:
                parameters.append(ParameterExtractor._convert_parameter(temp_str.strip()))
                temp_str = ""
            else:
                temp_str += char

        if stack:
            ErrorLog.ReportError("Unmatched opening brace detected.")
            return []
        if temp_str:
            parameters.append(ParameterExtractor._convert_parameter(temp_str.strip()))

        print(parameters)
        return parameters

    @staticmethod
    def _convert_parameter(param: str):
        """Converts a parameter string to its respective data type."""
        if param.isdigit():
            return int(param)
        if param.replace('.', '', 1).isdigit():
            return float(param)
        return param.strip('"').strip("'")
