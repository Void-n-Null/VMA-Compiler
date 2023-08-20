import brush_creator
import entity_creator

solids = []
entities = []
textures = {"DEV": "DEV/DEV_MEASUREGENERIC01B",
            "WOOD": "CP_MANOR/WOOD_FLOOR01",
            "SKYBOX": "TOOLS/TOOLSSKYBOX"}
entity_types = {
    "light": "(R G B Brightness) _light: 255 255 255 200"
}

def SetSolidTexture(name: str):
    name = name.upper()
    if (name not in textures):
        return False
    brush_creator.current_material = textures[name]
    return True

def AddEntity(type,x,y,z,extra_data = {}):
    entities
    entity = entity_creator.create_entity(len(entities) + 1, type,x,y,z,extra_data)
    entities.append(entity)

def AddSolid(x,y,z,width,depth,height):
    global solids
    solid = brush_creator.create_brush(x,y,z,width,depth,height)
    solids.append(solid)