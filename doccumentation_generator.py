from CommandRegistry import commands
import pkgutil
package_name = 'commands'
for _, module_name, _ in pkgutil.iter_modules([package_name]):
    pkgutil.importlib.import_module(f"{package_name}.{module_name}")

def documentation_report():
    """
    Print out a well-documented report on all functions using their docstrings.
    """
    intro = "VMA: Valve Map Abstraction \n A simple language for creating Valve Map Files (VMF) using human readable commands"
    functions = "".join(
        f"Command: {name}\nDescription: {details['function'].__doc__}\nExample: {details['example']}\n\n Notes: {details['notes']}\n{'-' * 20}\n"
        for name, details in commands.items()
    )
    return f"{intro} \n {functions}"

if __name__ == "__main__":
    print(documentation_report())