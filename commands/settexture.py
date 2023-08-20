from CommandRegistry import command
from Map import Map
from Map import textures
import ErrorLog

texture_list = "".join(f"- {texture}\n" for texture in textures.keys())
@command(example="SetTexture(DEV)",notes=f"Existing textures are  \n{texture_list}")
def settexture(map: Map,parameters: list):
    """
    Sets the texture for the next solid (brush) to be created.

    1 Parameter:
        parameters (list): Name of the texture.
    """
    name = str(parameters[0])
    response = map.set_texture(name)
    if not response:
        ErrorLog.ReportError(f"Texture: {name} invalid")