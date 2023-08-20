from SideFactory import SideFactory

class BrushFactory:
    current_material = "DEV/DEV_MEASUREGENERIC01B"
    
    @staticmethod
    def calculate_cube_corners(x, y, z, width, depth, height):
        x2, y2, z2 = x + width, y + depth, z + height
        return x2, y2, z2

    @staticmethod
    def create_brush(x, y, z, width, depth, height):
        x2, y2, z2 = BrushFactory.calculate_cube_corners(x, y, z, width, depth, height)
        
        sides = [
            SideFactory.create_side(1, f"({x} {y2} {z2}) ({x2} {y2} {z2}) ({x2} {y} {z2})", 
                        [f"{x} {y2} {z2}", f"{x2} {y2} {z2}", f"{x2} {y} {z2}", f"{x} {y} {z2}"]),
            SideFactory.create_side(2, f"({x} {y} {z}) ({x2} {y} {z}) ({x2} {y2} {z})", 
                        [f"{x} {y} {z}", f"{x2} {y} {z}", f"{x2} {y2} {z}", f"{x} {y2} {z}"]),
            SideFactory.create_side(3, f"({x} {y2} {z2}) ({x} {y} {z2}) ({x} {y} {z})", 
                        [f"{x} {y2} {z2}", f"{x} {y} {z2}", f"{x} {y} {z}", f"{x} {y2} {z}"]),
            SideFactory.create_side(4, f"({x2} {y2} {z}) ({x2} {y} {z}) ({x2} {y} {z2})", 
                        [f"{x2} {y2} {z}", f"{x2} {y} {z}", f"{x2} {y} {z2}", f"{x2} {y2} {z2}"]),
            SideFactory.create_side(5, f"({x2} {y2} {z2}) ({x} {y2} {z2}) ({x} {y2} {z})", 
                        [f"{x2} {y2} {z2}", f"{x} {y2} {z2}", f"{x} {y2} {z}", f"{x2} {y2} {z}"]),
            SideFactory.create_side(6, f"({x2} {y} {z}) ({x} {y} {z}) ({x} {y} {z2})", 
                        [f"{x2} {y} {z}", f"{x} {y} {z}", f"{x} {y} {z2}", f"{x2} {y} {z2}"]),
        ]

        solid = "solid\n{\n\t\"id\" \"2\"\n"
        for side in sides:
            solid += SideFactory.format_side_for_vmf(side, BrushFactory.current_material)
        solid += "}"

        return solid

# Usage example:
# brush = BrushFactory.create_brush(0, 0, 0, 1, 1, 1)
# print(brush)
