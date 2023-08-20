from ParameterExtractor import ParameterExtractor
import re
from commands import commands
import ErrorLog
class CommandExecutor:
    @staticmethod
    def execute_line(line: str, line_number: int):
        # Remove comments and unnecessary spaces, then convert to lowercase
        line = line.split('//')[0].strip().lower()
        line = line.split('#')[0].strip().lower()

        if not line:
            return

        regex = r"(\w+)\((.*)\)"
        if match := re.match(regex, line):
            CommandExecutor._execute_command(match, line_number)
        else:
            ErrorLog.ReportError("Invalid command format")

    @staticmethod
    def _execute_command(match, line_number):
        function_name, parameters_str = match.groups()

        try:
            parameters = ParameterExtractor.extract_parameters(parameters_str)
        except Exception as e:
            ErrorLog.ReportError(f"Error extracting parameters: {e}")
            return

        ErrorLog.currentLine = line_number

        if function_name in commands:
            commands[function_name]["function"](parameters)
        else:
            ErrorLog.ReportError(f"Command \"{function_name}\" not recognized")