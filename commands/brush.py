from CommandRegistry import command
from Map import Map
import ErrorLog

@command(example="Brush(0,0,0,32,64,32)",notes="A brush refers to a solid block or structure, fully rectangular and solid \n A brush's position will remain its lowest south west vertex, all scaling will be relative to that point")
def brush(current_map: Map,parameters: list):
    """
    Adds a solid rectangular brush (a building block in map design).

    6 Parameters:
        parameters (list): x, y, z coordinates followed by width, depth, and height.
    """
    x, y, z, width, depth, height = map(int, parameters[:6])
    if width <= 0 or height <= 0 or depth <= 0:
        ErrorLog.ReportError("Could not create brush with zero or negative scale")
        return
    current_map.add_solid(x, y, z, width, depth, height)