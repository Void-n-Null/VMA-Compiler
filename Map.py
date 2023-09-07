from VMFCodeFactories.BrushFactory import BrushFactory
from VMFCodeFactories.EntityFactory import EntityFactory
import json
textures = json.load(open("Data/Constants/textures.json","r"))
class Map:
    def __init__(self):
        self.solids = []
        self.entities = []
    def set_texture(self, name: str):
        BrushFactory.current_material = name
        return True
    def add_entity(self, type, x, y, z, extra_data={}):
        entity = EntityFactory.create_point_entity(len(self.entities) + 1, type, x, y, z, extra_data)
        self.entities.append(entity)
    def add_broad_entity(self, attributes, objects):
        entity = EntityFactory.create_broad_entity(attributes,objects, len(self.entities))
        self.entities.append(entity)
    def add_solid(self, x, y, z, width, depth, height):
        solid = BrushFactory.create_brush(x, y, z, width, depth, height)
        self.solids.append(solid)
