import ErrorLog
from CommandRegistry import command
from Map import Map
import json
entity_types = json.load(open("Data/Constants/entity_types.json","r"))

entity_type_list = '\n'.join(f"{type} - extra data: {data}" for type, data in entity_types.items())
@command(example="Entity(light,0,0,0,{\"_light\": \"255 255 255 200\"})",notes=f"Existing Entity types: \n {entity_type_list}")
def entity(map: Map, parameters: list):
    """
    Creates an Entity
    
    5 Parameters:
        Entity Type, x , y ,z, extra data dictionary
    """
    if (len(parameters) >= 4):
        type,x,y,z = parameters[0],parameters[1],parameters[2],parameters[3]
    else:
        ErrorLog.ReportError("Not enough parameters for creating Entity")
    data = parameters[4] if (len(parameters) >= 5) else {}
    map.add_entity(type,x,y,z,data)
    
@command(example= "BroadEntity({'classname': 'info_player_teamspawn', 'angles': '0 0 0', 'teamnum': '2', 'origin': '88 32 65.0046'})")
def broadentity(map: Map, parameters: list):
    translation_table = str.maketrans("\"'", "'\"")
    attributes = parameters[0].translate(translation_table)
    objects = parameters[2].translate(translation_table)
    print(attributes)
    print(objects)
    attributes = json.loads(attributes)
    objects = json.loads(objects)
    
    map.add_broad_entity(attributes,objects)