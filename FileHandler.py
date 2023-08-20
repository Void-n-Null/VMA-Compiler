import os

class FileHandler:
    @staticmethod
    def file_exists(path: str) -> bool:
        return os.path.exists(path)
    
    @staticmethod
    def load_file(path: str) -> str:
        with open(path, "r") as f:
            return f.read()

    @staticmethod
    def save_file(content: str, path: str):
        with open(path, "w") as f:
            f.write(content)