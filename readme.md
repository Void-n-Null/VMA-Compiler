# VMA: Valve Map Abstraction

In August 2023 I wanted to know if an LLM could build a playable Team Fortress 2 map. The immediate obstacle is Valve's map format. VMF is verbose, largely undocumented, and hostile to programmatic generation: a single cube needs six sides, each with plane definitions, texture axis vectors computed from surface normals, and correct vertex winding order.

Here is one of the six sides a cube needs in raw VMF:

```vmf
solid
{
    "id" "2"
    side
    {
        "id" "1"
        "plane" "(0 64 64) (64 64 64) (64 0 64)"
        "material" "DEV/DEV_MEASUREGENERIC01B"
        "uaxis" "[1 0 0 0] 0.25"
        "vaxis" "[0 -1 0 0] 0.25"
        "rotation" "0"
        "lightmapscale" "16"
        "smoothing_groups" "0"
    }
    // ... 5 more sides
}
```

Here is the same cube in VMA:

```vma
Brush(0, 0, 0, 64, 64, 64)
```

So the project became: reverse engineer VMF by staring at decompiled official maps, work out how Hammer derives texture axes from cross products against the dominant world axis, and put a tiny scripting language on top so that neither a human nor a model ever has to think about any of it.

## What's here

- **Compiler** (`compile.py`): VMA source to a VMF you can open in Hammer or feed to VBSP/VVIS/VRAD.
- **Decompiler** (`VMFDecompiler.py`): the reverse. Parses an existing VMF, extracts brush dimensions from vertex data, and reconstructs VMA commands.
- **A small language**: `Brush`, `SetTexture`, `Entity`, `SpawnPoint`, plus variables, arithmetic expressions, for loops, and comments. New commands register through a decorator and self-document.

```vma
wall_height = 256

SetTexture(WOOD)
Brush(-512, -512, 0, 1024, 1024, 16)      // Floor

SetTexture(DEV)
Brush(-512, -512, 16, 1024, 32, wall_height)  // North wall

SpawnPoint(Red, -400, 0, 32)
SpawnPoint(Blue, 400, 0, 32)
```

Python 3.8+, no external dependencies.

## Did the AI part work?

Sort of. A 2023-era model could not write VMF at all, but given the four VMA commands and a short description it could reliably produce an arena: floor, perimeter walls, spawns for both teams, a platform in the middle. A 1000-brush map in VMA is also roughly 50x smaller than the equivalent VMF, which matters when every token costs money.

## Where the idea went

The Python stopped here, but the problem didn't. [VMFSharp](https://github.com/Void-n-Null/VMFSharp) is the 2026 successor, the same VMF-generation core rebuilt as a proper C# library with brush carving and real tests, and [GravyBox](https://github.com/Void-n-Null/GravyBox) is the editor-shaped continuation of wanting better graybox tooling than Hammer. This repo is the origin point, preserved as it was.

BSD 3-Clause, see [LICENSE](LICENSE).
