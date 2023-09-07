import re
import ErrorLog

FOR_LOOP_PATTERN = re.compile(r"for\s+(\w+)\s+range\s+(\d+)\s*{")

class ForLoopHandler:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    @staticmethod
    def is_for_loop(line: str) -> bool:
        return "for " in line and "{" in line and FOR_LOOP_PATTERN.match(line)

    def get_loop_end(self, start_line: int) -> int:
        brace_count = 1  # since we have already found one opening brace '{'
        for idx, script_line in enumerate(self.interpreter.script[start_line + 1:], start=start_line + 1):
            brace_count += script_line.count("{")
            brace_count -= script_line.count("}")
            if brace_count == 0:
                return idx
        return None

    def execute_for_loop(self, loop_line, start_line):
        match = FOR_LOOP_PATTERN.match(loop_line)
        loop_var, iterations = match.groups()
        iterations = int(iterations)
        loop_end = self.get_loop_end(start_line)

        if loop_end is None:
            ErrorLog.ReportError("for loop could not detect a closing '}'")
            return start_line  # Return the current line to signify an error.

        loop_body_start = start_line + 1

        for i in range(iterations):
            self.interpreter.variable_manager.set_variable(loop_var, str(i))
            idx = loop_body_start
            while idx < loop_end:
                line = self.interpreter.script[idx]
                if ForLoopHandler.is_for_loop(line):
                    self.execute_for_loop(line, idx)
                    idx = self.get_loop_end(idx) + 1  # Continue after the inner loop
                else:
                    self.interpreter.interpret(line, idx)
                    idx += 1

        # After processing all iterations, return the end of this loop to resume execution.
        return loop_end + 1
