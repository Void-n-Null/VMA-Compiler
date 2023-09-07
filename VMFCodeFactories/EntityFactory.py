class EntityFactory:

    @staticmethod
    def create_point_entity(id, type, x, y, z, extra_data={}):
        if extra_data is None or extra_data == "":
            extra_str = ""
        else:
            extra_str = ''.join(f'\t"{key}" "{value}"\n' for key, value in extra_data.items())
        
        return f'''entity
        {{
        \t"id" "{id}"
        \t"classname" "{type}"
        \t"angles" "0 0 0"
        \t"spawnflags" "511"
        \t"origin" "{x} {y} {z}"
        {extra_str}
        \teditor
        \t{{
        \t\t"color" "220 30 220"
        \t\t"visgroupshown" "1"
        \t\t"visgroupautoshown" "1"
        \t\t"logicalpos" "[0 0]"
        \t}}
        }}'''
    @staticmethod
    def create_broad_entity(attributes = {}, objects = {}, count = 0):
        attributes["id"] = count+1
        attribute_str = ''.join(f'\t"{key.strip()}" "{str(value).strip()}"\n' for key, value in attributes.items())

        object_str = ""
        for object_name, object in objects.items():
            name: str = object_name
            value = object.replace("'", '"')
            valuelines = value.splitlines()
            stripped_value = ""
            for line in valuelines:
                stripped_value += "\t\t"
                stripped_value += line.replace("\t","") + "\n"
            
            value = '\n'.join(valuelines)
            for r in "!@#$%^&*(\")\' ":
                name = name.replace(r,"")
            name = name.strip()
            print(name)
            object_str += f"\n\t{name}\n" + "\t{\n" + stripped_value + "\n\t}"
        return f'''entity
{{
{attribute_str}
{object_str}
}}
'''