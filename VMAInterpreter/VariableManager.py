import re
import ErrorLog

class VariableManager:
    ASSIGNMENT_PATTERN = re.compile(r"(\w+)\s*=\s*(.*)")
    def __init__(self, interpreter):
        self.contexts = [{}]
        self.interpreter = interpreter

    def push_context(self):
        self.contexts.append({})

    def pop_context(self):
        self.contexts.pop()

    def set_variable(self, var_name, value):
        self.contexts[-1][var_name] = value
    
    def get_variable(self, var_name):
        for context in reversed(self.contexts):
            if var_name in context:
                return context[var_name]
        return None
    
    def handle_assignment(self, line: str) -> bool:
        match = VariableManager.ASSIGNMENT_PATTERN.match(line)
        if not match:
            return False

        var_name, expression = match.groups()
        if evaluation := self.evaluate_expression(expression):
            self.set_variable(var_name, str(evaluation))
            return True
        else:
            return False

    def evaluate_expression(self,expression: str) -> str:
        expression = self.replace_variables_in_str(expression)
        try:
            return str(eval(expression))
        except Exception as e:
            ErrorLog.ReportError(f"Error evaluating expression: {expression}: {e}")
            return None

    def replace_variables_in_params(self, parameters: list) -> list:
        new_params = []
        for parameter in parameters:
            value = self.get_variable(str(parameter))
            new_params.append(value if value is not None else parameter)
        return new_params
    
    def replace_variables_in_str(self, expression: str) -> str:
        def repl(match):
            var_name = match.group(1)
            value = self.get_variable(var_name) or var_name
            return value

        all_keys = [key for context in self.contexts for key in context.keys()]
        pattern = r"\b(" + "|".join(re.escape(var) for var in all_keys) + r")\b"
        return re.sub(pattern, repl, expression)


