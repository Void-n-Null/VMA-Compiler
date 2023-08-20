class EntityFactory:

    @staticmethod
    def create_entity(id, type, x, y, z, extra_data={}):
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