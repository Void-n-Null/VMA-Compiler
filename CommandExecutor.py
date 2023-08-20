from ParameterExtractor import ParameterExtractor
import re
from Map import Map
from CommandRegistry import commands
import ErrorLog
import pkgutil
package_name = 'commands'
for _, module_name, _ in pkgutil.iter_modules([package_name]):
    pkgutil.importlib.import_module(f"{package_name}.{module_name}")

class CommandExecutor:
    variables = {}  # Store the variable names and their values
    def __init__(self,map: Map) -> None:
        self.map:Map = map
    VAR_PATTERN = re.compile(r"var\s+(\w+)\s*=\s*(.*)")
    CMD_PATTERN = re.compile(r"(\w+)\((.*)\)")
    def execute_line(self, line: str, line_number: int):
        # Remove comments, unnecessary spaces, and convert to lowercase in one pass
        line = re.split('//|#', line)[0].strip().lower()
        ErrorLog.currentLine = line_number
        if not line:
            return

        # Handle variable assignment
        if line.startswith("var "):
            if match := CommandExecutor.VAR_PATTERN.match(line):
                var_name, var_value = match.groups()
                CommandExecutor.variables[var_name] = var_value.strip()
            else:
                ErrorLog.ReportError("Invalid variable assignment format")
            return

        # Replace variables in the command line
        line = CommandExecutor._replace_variables(line)

        if match := CommandExecutor.CMD_PATTERN.match(line):
            self._execute_command(match)
        else:
            ErrorLog.ReportError("Invalid command format")

    @staticmethod
    def _replace_variables(line: str) -> str:
        for var_name, var_value in CommandExecutor.variables.items():
            placeholder = f"${{{var_name}}}"
            if placeholder in line:
                line = line.replace(placeholder, var_value)
        return line

    def _execute_command(self, match):
        function_name, parameters_str = match.groups()

        try:
            parameters = ParameterExtractor.extract_parameters(parameters_str)
        except Exception as e:
            ErrorLog.ReportError(f"Error extracting parameters: {e}")
            return
        if function_name in commands:
            try:
                commands[function_name]["function"](self.map,parameters)
            except Exception as e:
                ErrorLog.ReportError(f"Error executing command \"{function_name}\": {e}")
        else:
            ErrorLog.ReportError(f"Command \"{function_name}\" not recognized")
