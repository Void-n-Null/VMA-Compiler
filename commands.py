from data import AddEntity, AddSolid, SetSolidTexture, textures, entity_types
import ErrorLog
# Create a global commands dictionary
commands = {}
def command(example="", notes = ""):
    """
    A decorator to add functions to the global commands dictionary.
    
    Parameters:
        example (str): Example usage of the function.
    """
    def decorator(func):
        commands[func.__name__] = {"function": func, "example": example, "notes": notes}
        return func
    return decorator

@command(example="Brush(0,0,0,32,64,32)"
        ,notes="A brush refers to a solid block or structure, fully rectangular and solid \n A brush's position will remain its lowest south west vertex, all scaling will be relative to that point")
def brush(parameters: list):
    """
    Adds a solid rectangular brush (a building block in map design).

    6 Parameters:
        parameters (list): x, y, z coordinates followed by width, depth, and height.
    """
    x, y, z, width, depth, height = map(int, parameters[:6])
    if width <= 0 or height <= 0 or depth <= 0:
        ErrorLog.ReportError("Could not create brush with zero or negative scale")
        return
    AddSolid(x, y, z, width, depth, height)
texture_list = "".join(f"- {texture}\n" for texture in textures.keys())
@command(example="SetTexture(DEV)",notes=f"Existing textures are  \n{texture_list}")
def settexture(parameters: list):
    """
    Sets the texture for the next solid (brush) to be created.

    1 Parameter:
        parameters (list): Name of the texture.
    """
    name = str(parameters[0])
    if not SetSolidTexture(name):
        ErrorLog.ReportError(f"Texture: {name} invalid")

@command(example="SpawnPoint(Red,32,64,128)", notes="Spawn points are locations where players are spawned, either on red team or blue team")
def spawnpoint(parameters: list):
    """
    Sets a spawn point for players based on the team.

    4 Parameters:
        parameters (list): Team name followed by x, y, z coordinates.
    """
    try:
        TeamName = parameters[0].lower()
    except Exception:
        ErrorLog.ReportError("Incorrect Team label")
        return

    team_mapping = {
        "red": 2, "r": 2, "2": 2,
        "blu": 3, "blue": 3, "b": 3, "3": 3
    }
    TeamValue = team_mapping.get(TeamName)

    if not TeamValue:
        ErrorLog.ReportError(f"Team {TeamName} not valid")
        return

    AddEntity("info_player_teamspawn", parameters[1], parameters[2], parameters[3], {"TeamNum": TeamValue})

@command(example="HollowBrush(0,0,0,32,64,32,8)",notes="- The hollow brush is essentially a room or a hollowed-out cube with walls of specified thickness.")
def hollowbrush(parameters: list):
    """
    Adds a hollow rectangular brush with specified thickness.

    7 Parameters:
        parameters (list): x, y, z coordinates followed by width, depth, height, and wall thickness.
    """
    x, y, z, width, depth, height, thickness = map(int,parameters[:7])
        # Check for valid thickness
    if thickness <= 0:
        ErrorLog.ReportError("Thickness cannot be zero or negative")
        return

    if width - 2*thickness <= 0 or depth - 2*thickness <= 0 or height - 2*thickness <= 0:
        ErrorLog.ReportError("Thickness too large for the given dimensions")
        return

    # Floor
    brush([x, y, z, width, depth, thickness])
    # Ceiling
    brush([x, y, z + height - thickness, width, depth, thickness])
    # North wall
    brush([x, y, z + thickness, width, thickness, height - 2*thickness])
    # South wall
    brush([x, y + depth - thickness, z + thickness, width, thickness, height - 2*thickness])
    # West wall
    brush([x, y + thickness, z + thickness, thickness, depth - 2*thickness, height - 2*thickness])
    # East wall
    brush([x + width - thickness, y + thickness, z + thickness, thickness, depth - 2*thickness, height - 2*thickness])

entity_type_list = '\n'.join(f"{type} - extra data: {data}" for type, data in entity_types.items())
@command(example="Entity(light,0,0,0,{\"_light\": \"255 255 255 200\"})",notes=f"Existing Entity types: \n {entity_type_list}")
def entity(parameters: list):
    """
    Creates an Entity
    
    5 Parameters:
        Entity Type, x , y ,z, extra data dictionary
    """
    type,x,y,z,data = parameters[0],parameters[1],parameters[2],parameters[3],parameters[4]

    AddEntity(type,x,y,z,data)

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
    report = documentation_report()
    print(report)