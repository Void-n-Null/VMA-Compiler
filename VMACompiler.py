import os
from data import entities, solids
from FileHandler import FileHandler
from PrefabLoader import PrefabLoader
from CommandExecutor import CommandExecutor
import ErrorLog
class VMACompiler:
    def __init__(self, file_path: str):
        ErrorLog.currentLine = 0
        self.file_path = file_path
        if (FileHandler.file_exists("template.txt")):
            self.template = FileHandler.load_file("template.txt")
        else:
            ErrorLog.ReportError("Template File not found.")
        self.prefabs = PrefabLoader.load_prefabs()

    def compile(self) -> str:
        output = self.template
        VMAText = FileHandler.load_file(self.file_path)

        for prefab_name, prefab_content in self.prefabs.items():
            output = output.replace(f"<{prefab_name}>", f"{prefab_name}\n{prefab_content}")

        for i, line in enumerate(VMAText.splitlines()):
            CommandExecutor.execute_line(line, i + 1)

        output = output.replace("[ENTITIES]", '\n'.join(entities))
        output = output.replace("[SOLIDS]", '\n'.join(solids))
        return '\n'.join(line for line in output.splitlines() if line.strip())

    def save_vmf(self, vmf_content: str):
        output_path = f"{os.path.splitext(self.file_path)[0]}.vmf"
        FileHandler.save_file(vmf_content, output_path)
        return output_path

    def compile_to_vmf(self):
        data = self.compile()
        return self.save_vmf(data)