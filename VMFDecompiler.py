import os
import re
from collections import Counter
import geometry_operations

class VMFDecompiler:
    VERTEX_PATTERN = re.compile(r'"v" "(-?\d+\.?\d*e?-?\d*) (-?\d+\.?\d*e?-?\d*) (-?\d+\.?\d*e?-?\d*)"')
    PLANE_PATTERN = re.compile(r'"plane" "([^"]+)"')
    MATERIAL_PATTERN = re.compile(r'"material" "([^"]+)"')
    ATTRIBUTE_PATTERN = re.compile(r'\t"([^"]+)" "([^"]+)"')
    def __init__(self, input_path: str):
        self.input_path = input_path
    
    @staticmethod
    def parse_vmf_solid(vmf_code, count):
        vertices = VMFDecompiler.VERTEX_PATTERN.findall(vmf_code)
        vertices = [(float(x), float(y), float(z)) for x, y, z in vertices]
        
        planes = VMFDecompiler.PLANE_PATTERN.findall(vmf_code)
        for plane in planes:
                    coords = [geometry_operations.parse_number(coord) for coord in re.findall(r"[-]?\d+[.]?\d*", plane)]
                    vertices.extend([(coords[i], coords[i+1], coords[i+2]) for i in range(0, 9, 3)])

        try:
            min_vals, max_vals = zip(*[(min(coord), max(coord)) for coord in zip(*vertices)])
            dims = [int(max_val - min_val) for min_val, max_val in zip(min_vals, max_vals)]
            if 0 in dims:
                print(f"ERROR ON BRUSH {count}: Dimension is zero", *min_vals, *max_vals)
        except Exception as e:
            print(f"ERROR ON BRUSH {count}: {e}")

        filtered_materials = [material for material in VMFDecompiler.MATERIAL_PATTERN.findall(vmf_code) if "NODRAW" not in material.upper()]
        common_material = Counter(filtered_materials).most_common(1)[0][0] if filtered_materials else None

        return {
            'material': common_material,
            'x': int(min_vals[0]),
            'y': int(min_vals[1]),
            'z': int(min_vals[2]),
            'width': dims[0],
            'depth': dims[1],
            'height': dims[2]
        }

    @staticmethod
    def find_objects(code):
        code, objects, stack = "\n" + code, [], []
        obj_name, obj_content, inside_quotes, capture_name = "", "", False, False

        for i, c in enumerate(code):
            if c == '"' and code[i - 1] != '\\':
                inside_quotes = not inside_quotes
        
            if inside_quotes: continue

            if c == '\n' and not stack:
                capture_name = True
                continue

            if c == '{':
                if capture_name:
                    obj_name = obj_name.strip()
                    capture_name = False
                stack.append(i)
                continue

            if c == '}':
                start = stack.pop()
                if not stack:
                    obj_content = code[start + 1:i].strip()
                    objects.append((obj_name, obj_content))
                    obj_name, obj_content = "", ""
                    continue

            if capture_name:
                obj_name += c

        return objects

    @staticmethod
    def find_objects_recursively(input_code):
        if isinstance(input_code, str):
            objects = VMFDecompiler.find_objects(input_code)
        else:
            objects = [VMFDecompiler.find_objects(obj[1]) for obj in input_code]
            objects = [item for sublist in objects for item in sublist]

        return objects

    @staticmethod
    def parse_vmf_entity(entity_code):
        objects = VMFDecompiler.find_objects_recursively(entity_code)
        output_objects = {obj[0]: obj[1] for obj in objects}
        
        for obj in objects:
            entity_code = entity_code.replace(obj[1], "")

        attributes = dict(VMFDecompiler.ATTRIBUTE_PATTERN.findall(entity_code))
        return {"attributes": attributes, "objects": output_objects}

    def decompile(self):
        VMALines = []
        with open(self.input_path, 'r') as f:
            VMFCode = f.read().lower()
        objects = VMFDecompiler.find_objects(VMFCode)
        objects_dict = {}
        brushes = []
        entities = []

        for object in objects:
            objects_dict[object[0]] = object[1]
        if not objects_dict.get('world'):
            print("WORLD NOT FOUND, NO BRUSHES")
        else:
            world_objects = VMFDecompiler.find_objects_recursively(objects_dict["world"])
            for i, world_object in enumerate(world_objects):
                if "solid" in world_object[0]:
                    brushes.append(VMFDecompiler.parse_vmf_solid(world_object[1], i))
        for object in objects:
            if "entity" in object[0]:
                entities.append(VMFDecompiler.parse_vmf_entity(object[1]))
        for brush in brushes:
            if brush['material'] is None:
                continue
            VMALines.append(f"SetTexture({brush['material'].upper()})")
            VMALines.append(f"Brush({brush['x']},{brush['y']},{brush['z']},{brush['width']},{brush['depth']},{brush['height']})")
        for entity in entities:
            VMALines.append(f"BroadEntity({entity['attributes']},{entity['objects']})")

        return '\n'.join(VMALines)

    def save_to_vma(self):
        VMACode = self.decompile()
        output_path = f"{os.path.splitext(self.input_path)[0]}.vma"
        with open(output_path, "w") as out_file:
            out_file.write(VMACode)
        print(f"Decompiled {self.input_path} to {output_path}")
        return output_path

if __name__ == "__main__":
    decompiler = VMFDecompiler("Test\koth_harvest_final_d_exp.vmf")
    decompiler.save_to_vma()
