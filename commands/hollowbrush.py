import ErrorLog
from CommandRegistry import command
from . import brush
from Map import Map

@command(example="HollowBrush(0,0,0,32,64,32,8)",notes="- The hollow brush is essentially a room or a hollowed-out cube with walls of specified thickness.")
def hollowbrush(map: Map,parameters: list):
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
    brush(map,[x, y, z, width, depth, thickness])
    # Ceiling
    brush(map,[x, y, z + height - thickness, width, depth, thickness])
    # North wall
    brush(map,[x, y, z + thickness, width, thickness, height - 2*thickness])
    # South wall
    brush(map,[x, y + depth - thickness, z + thickness, width, thickness, height - 2*thickness])
    # West wall
    brush(map,[x, y + thickness, z + thickness, thickness, depth - 2*thickness, height - 2*thickness])
    # East wall
    brush(map,[x + width - thickness, y + thickness, z + thickness, thickness, depth - 2*thickness, height - 2*thickness])
