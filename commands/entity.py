import ErrorLog
from command_registry import command
from data import entity_types, AddEntity

entity_type_list = '\n'.join(f"{type} - extra data: {data}" for type, data in entity_types.items())
@command(example="Entity(light,0,0,0,{\"_light\": \"255 255 255 200\"})",notes=f"Existing Entity types: \n {entity_type_list}")
def entity(parameters: list):
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
    AddEntity(type,x,y,z,data)