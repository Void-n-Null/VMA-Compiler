import re
import ErrorLog
from Map import Map
from .CommandExecutor import CommandExecutor
from .ForLoopHandler import ForLoopHandler
from .VariableManager import VariableManager

class Interpreter:
    def __init__(self, script: str, map: Map,):
        self.script = script
        self.command_executor = CommandExecutor(self, map)
        self.for_loop_handler = ForLoopHandler(self)
        self.variable_manager = VariableManager(self)
        self.skip_stack = []

    def interpret(self, line: str, line_number: int):
        ErrorLog.currentLine = line_number
        clean_line = re.split('//|#', line)[0].strip().lower()
        if (clean_line == ""):
            return
        handled_as_assignment = self.variable_manager.handle_assignment(clean_line)
        if not handled_as_assignment:
            self.command_executor._execute_command(clean_line)
