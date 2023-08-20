commands = {}

def command(example="", notes=""):
    def decorator(func):
        commands[func.__name__] = {"function": func, "example": example, "notes": notes}
        return func
    return decorator
