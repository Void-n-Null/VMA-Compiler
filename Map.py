from BrushFactory import BrushFactory
from EntityFactory import EntityFactory

entity_types = {
            "light": "(R G B Brightness) _light: 255 255 255 200"
        }
textures = {
            "DEV": "DEV/DEV_MEASUREGENERIC01B",
            "WOOD": "CP_MANOR/WOOD_FLOOR01",
            "SKYBOX": "TOOLS/TOOLSSKYBOX"
        }
class Map:
    def __init__(self):
        self.solids = []
        self.entities = []
    def set_texture(self, name: str):
        name = name.upper()
        if name not in self.textures:
            return False
        BrushFactory.current_material = self.textures[name]
        return True

    def add_entity(self, type, x, y, z, extra_data={}):
        entity = EntityFactory.create_entity(len(self.entities) + 1, type, x, y, z, extra_data)
        self.entities.append(entity)

    def add_solid(self, x, y, z, width, depth, height):
        solid = BrushFactory.create_brush(x, y, z, width, depth, height)
        self.solids.append(solid)

# Example usage:
# my_map = Map()
# my_map.set_variable("some_key", "some_value")
# my_map.add_solid(0, 0, 0, 10, 10, 10)
