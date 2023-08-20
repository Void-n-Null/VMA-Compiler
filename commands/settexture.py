from command_registry import command
from data import textures, SetSolidTexture
import ErrorLog

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