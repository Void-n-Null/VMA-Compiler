
from side_creator import create_side, format_side_for_vmf

current_material = "DEV/DEV_MEASUREGENERIC01B"

def calculate_cube_corners(x, y, z, width, depth, height):
    x2, y2, z2 = x + width, y + depth, z + height
    return x2, y2, z2

def create_brush(x, y, z, width, depth, height):
    x2, y2, z2 = calculate_cube_corners(x, y, z, width, depth, height)
    
    sides = [
        create_side(1, f"({x} {y2} {z2}) ({x2} {y2} {z2}) ({x2} {y} {z2})", 
                    [f"{x} {y2} {z2}", f"{x2} {y2} {z2}", f"{x2} {y} {z2}", f"{x} {y} {z2}"]),
        create_side(2, f"({x} {y} {z}) ({x2} {y} {z}) ({x2} {y2} {z})", 
                    [f"{x} {y} {z}", f"{x2} {y} {z}", f"{x2} {y2} {z}", f"{x} {y2} {z}"]),
        create_side(3, f"({x} {y2} {z2}) ({x} {y} {z2}) ({x} {y} {z})", 
                    [f"{x} {y2} {z2}", f"{x} {y} {z2}", f"{x} {y} {z}", f"{x} {y2} {z}"]),
        create_side(4, f"({x2} {y2} {z}) ({x2} {y} {z}) ({x2} {y} {z2})", 
                    [f"{x2} {y2} {z}", f"{x2} {y} {z}", f"{x2} {y} {z2}", f"{x2} {y2} {z2}"]),
        create_side(5, f"({x2} {y2} {z2}) ({x} {y2} {z2}) ({x} {y2} {z})", 
                    [f"{x2} {y2} {z2}", f"{x} {y2} {z2}", f"{x} {y2} {z}", f"{x2} {y2} {z}"]),
        create_side(6, f"({x2} {y} {z}) ({x} {y} {z}) ({x} {y} {z2})", 
                    [f"{x2} {y} {z}", f"{x} {y} {z}", f"{x} {y} {z2}", f"{x2} {y} {z2}"]),
    ]

    solid = "solid\n{\n\t\"id\" \"2\"\n"
    for side in sides:
        solid += format_side_for_vmf(side,current_material)
    solid += "}"

    return solid