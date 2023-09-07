from geometry_operations import cross_product, compute_texture_axes

class SideFactory:

    @staticmethod
    def create_side(id, plane, vertices):
        normal = SideFactory.extract_normal_from_plane(plane)
        uaxis, vaxis = compute_texture_axes(normal)
        return {
            "id": str(id),
            "plane": plane,
            "vertices": vertices,
            "uaxis": uaxis,
            "vaxis": vaxis
        }
        
    @staticmethod
    def extract_normal_from_plane(plane):
        # Remove any leading and trailing parentheses and then split the string
        points = [tuple(map(float, p.strip('()').split())) for p in plane.split(') (')]
        
        # Calculate vectors from the points
        vec1 = (points[1][0] - points[0][0], points[1][1] - points[0][1], points[1][2] - points[0][2])
        vec2 = (points[2][0] - points[1][0], points[2][1] - points[1][1], points[2][2] - points[1][2])

        # Calculate the normal using the cross product
        normal = cross_product(vec1, vec2)
        length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
        return (normal[0]/length, normal[1]/length, normal[2]/length)

    @staticmethod
    def format_side_for_vmf(side, material="DEV/DEV_MEASUREGENERIC01B", tabs=1):
        formatted_side = f"""side
{{
    "id" "{side['id']}"
    "plane" "{side['plane']}"
    vertices_plus
    {{
"""
        for vertex in side['vertices']:
            formatted_side += f'\t\t"v" "{vertex}"\n'
        formatted_side += "\t}\n"

        formatted_side += f'\t"material" "{material}"\n'
        formatted_side += f'\t"uaxis" "{side["uaxis"]} 0.25"\n'
        formatted_side += f'\t"vaxis" "{side["vaxis"]} 0.25"\n'
        formatted_side += """\t"rotation" "0"
    "lightmapscale" "16"
    "smoothing_groups" "0"
}
"""

        # Add X amount of tabs to each line
        tab_string = "\t" * tabs
        return "\n".join(
            [
                tab_string + line if line else line
                for line in formatted_side.split("\n")
            ]
        )

# Usage example:
# side = SideFactory.create_side(1, "(0 0 0) (1 1 1) (2 2 2)", [(0, 0, 0), (1, 1, 1), (2, 2, 2)])
# print(SideFactory.format_side_for_vmf(side))
