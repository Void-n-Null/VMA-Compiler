from ParameterExtractor import ParameterExtractor
from Map import Map
from CommandRegistry import commands
import ErrorLog
import pkgutil
import re

package_name = 'commands'
for _, module_name, _ in pkgutil.iter_modules([package_name]):
    pkgutil.importlib.import_module(f"{package_name}.{module_name}")



class CommandParser:
    CMD_PATTERN = re.compile(r"(\w+)\((.*)\)")

    @staticmethod
    def parse(line: str):
        if match := CommandParser.CMD_PATTERN.match(line):
            function_name, parameters_str = match.groups()
            try:
                parameters = ParameterExtractor.extract_parameters(parameters_str)
            except Exception as e:
                ErrorLog.ReportError(f"Error extracting parameters: {e}")
                return None, []
        else:
            ErrorLog.ReportError(f"Invalid format: \"{line}\"")
            return None, []
        return function_name, parameters

class CommandExecutor:
    FOR_LOOP_PATTERN = re.compile(r"for\s+(\w+)\s+in\s+range\((\d+)\)\s*{")
    def __init__(self, interpreter, map: Map) -> None:
        self.map: Map = map
        self.interpreter = interpreter
    def _execute_command(self, line):
        function_name, parameters = CommandParser.parse(line)
        if function_name in commands:
            try:
                parameters = self.interpreter.variable_manager.replace_variables_in_params(parameters)
                commands[function_name]["function"](self.map, parameters)
            except Exception as e:
                ErrorLog.ReportError(f"Error executing command \"{function_name}\": {e}")
        else:
            ErrorLog.ReportError(f"Command \"{function_name}\" not recognized")

