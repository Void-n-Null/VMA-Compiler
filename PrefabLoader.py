from FileHandler import FileHandler
import os
class PrefabLoader:
    @staticmethod
    def load_prefabs(path: str = "Data/Prefabs"):
        return {
            os.path.splitext(filename)[0]: FileHandler.load_file(os.path.join(path, filename))
            for filename in os.listdir(path)
        }