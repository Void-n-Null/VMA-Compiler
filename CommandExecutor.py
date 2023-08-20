from ParameterExtractor import ParameterExtractor
import re
from command_registry import commands
import ErrorLog
import pkgutil
package_name = 'commands'
for _, module_name, _ in pkgutil.iter_modules([package_name]):
    pkgutil.importlib.import_module(f"{package_name}.{module_name}")

class CommandExecutor:
    variables = {}  # Store the variable names and their values

    VAR_PATTERN = re.compile(r"var\s+(\w+)\s*=\s*(.*)")
    CMD_PATTERN = re.compile(r"(\w+)\((.*)\)")

    @staticmethod
    def execute_line(line: str, line_number: int):
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
            CommandExecutor._execute_command(match, line_number)
        else:
            ErrorLog.ReportError("Invalid command format")

    @staticmethod
    def _replace_variables(line: str) -> str:
        for var_name, var_value in CommandExecutor.variables.items():
            placeholder = f"${{{var_name}}}"
            if placeholder in line:
                line = line.replace(placeholder, var_value)
        return line

    @staticmethod
    def _execute_command(match, line_number):
        function_name, parameters_str = match.groups()

        try:
            parameters = ParameterExtractor.extract_parameters(parameters_str)
        except Exception as e:
            ErrorLog.ReportError(f"Error extracting parameters: {e}")
            return
        if function_name in commands:
            try:
                commands[function_name]["function"](parameters)
            except Exception as e:
                ErrorLog.ReportError(f"Error executing command \"{function_name}\": {e}")
        else:
            ErrorLog.ReportError(f"Command \"{function_name}\" not recognized")
