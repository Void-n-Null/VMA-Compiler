# VMA — Valve Map Abstraction

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![License](https://img.shields.io/badge/license-BSD%203--Clause-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)

**A human-readable abstraction layer for Valve Map Files (VMF) designed for AI-assisted map generation.**

*Reverse-engineered from Valve's proprietary format • Built for simplicity • Optimized for AI workflows*

</div>

---

## 🎯 The Problem

Valve Map Files (`.vmf`) are complex, verbose, and notoriously difficult to generate programmatically. A single brush (cube) requires:

- 6 sides with precise 3D plane definitions
- Texture coordinate calculations using cross products
- UV axis computations based on surface normals
- Proper vertex winding order for each face
- Nested hierarchical structures with unique IDs

**Here's what a simple cube looks like in raw VMF:**

```vmf
solid
{
    "id" "2"
    side
    {
        "id" "1"
        "plane" "(0 64 64) (64 64 64) (64 0 64)"
        vertices_plus
        {
            "v" "0 64 64"
            "v" "64 64 64"
            "v" "64 0 64"
            "v" "0 0 64"
        }
        "material" "DEV/DEV_MEASUREGENERIC01B"
        "uaxis" "[1 0 0 0] 0.25"
        "vaxis" "[0 -1 0 0] 0.25"
        "rotation" "0"
        "lightmapscale" "16"
        "smoothing_groups" "0"
    }
    // ... 5 more sides with similar complexity
}
```

**The same cube in VMA:**

```vma
Brush(0, 0, 0, 64, 64, 64)
```

---

## 🧠 The Vision: AI-Friendly Map Generation

This project was born from a simple question: *Can AI generate playable Team Fortress 2 maps?*

The answer required solving several challenges:

1. **VMF is too complex for direct generation** — Even advanced LLMs struggle with the precise geometric calculations and nested structures required
2. **The format is undocumented** — Required reverse-engineering through analysis of existing maps
3. **Geometry calculations are non-trivial** — Texture alignment requires understanding 3D math concepts like cross products and normal vectors

**VMA solves this by providing:**
- A minimal instruction set that an AI can learn quickly
- Automatic handling of all geometric calculations
- Human-readable syntax for easy validation and debugging
- Bidirectional conversion (compile to VMF, decompile from VMF)

---

## 🔬 Technical Deep-Dive: Reverse Engineering VMF

### Understanding the Format

VMF files use a custom key-value format with nested blocks. Through extensive analysis of official Valve maps, this project decoded:

#### 1. **Solid Geometry Structure**
```
solid {
    id → Unique identifier
    side (×6) {
        plane → Three 3D points defining the plane
        vertices_plus → Actual corner vertices
        material → Texture path
        uaxis/vaxis → Texture alignment vectors
    }
}
```

#### 2. **Plane Definitions**
Each face is defined by three points in **counter-clockwise winding order**. The parser extracts these using regex:
```python
PLANE_PATTERN = re.compile(r'"plane" "([^"]+)"')
```

#### 3. **Texture Axis Calculation**
The most complex reverse-engineering involved understanding how Hammer calculates texture alignment:

```python
def compute_texture_axes(plane):
    # Find the dominant world axis for this surface
    primary_axis = max(world_axes, key=lambda ax: abs(dot_product(ax, plane)))
    
    # U-axis: perpendicular to normal and world up
    uaxis = cross_product(primary_axis, (0, 0, 1))
    
    # V-axis: perpendicular to normal and U-axis
    vaxis = cross_product(primary_axis, uaxis)
    
    return uaxis, vaxis
```

#### 4. **Entity System**
Point entities (lights, spawn points, etc.) are simpler but still require proper formatting:
```
entity {
    id, classname, origin, angles, spawnflags, ...
    editor { color, visgroupshown, ... }
}
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        VMA Source File                           │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  SetTexture(WOOD)                                          │  │
│  │  Brush(0, 0, 0, 512, 512, 16)    // Floor                  │  │
│  │  SpawnPoint(Red, 128, 128, 32)                             │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                         VMA Compiler                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Interpreter │→ │   Command   │→ │     VMF Code Factories  │  │
│  │             │  │  Executor   │  │  ┌───────────────────┐  │  │
│  │ • Variables │  │             │  │  │  BrushFactory     │  │  │
│  │ • For Loops │  │ • Registry  │  │  │  EntityFactory    │  │  │
│  │ • Comments  │  │ • Dispatch  │  │  │  SideFactory      │  │  │
│  └─────────────┘  └─────────────┘  │  └───────────────────┘  │  │
│                                     └─────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                         VMF Output                               │
│         Playable in Team Fortress 2 / Source Engine              │
└──────────────────────────────────────────────────────────────────┘
```

### Module Breakdown

| Module | Purpose |
|--------|---------|
| `VMACompiler.py` | Main compiler orchestration — loads templates, prefabs, and coordinates compilation |
| `VMAInterpreter/` | Language interpreter with support for variables, loops, and expressions |
| `VMFCodeFactories/` | Low-level VMF generation — handles geometry calculations and formatting |
| `VMFDecompiler.py` | **Reverse process** — converts existing VMF files back to VMA |
| `CommandRegistry.py` | Decorator-based command registration system |
| `commands/` | Individual command implementations (extensible) |

---

## 📖 VMA Language Reference

### Commands

#### `Brush(x, y, z, width, depth, height)`
Creates a solid rectangular brush (building block of Source maps).

```vma
// Create a floor: 512x512 units, 16 units thick
Brush(0, 0, 0, 512, 512, 16)

// Create a wall
Brush(0, 0, 16, 16, 512, 256)
```

> **Note:** Position is anchored at the lowest south-west vertex. All dimensions must be positive.

---

#### `SetTexture(texture_name)`
Sets the texture for subsequent brushes.

```vma
SetTexture(WOOD)
Brush(0, 0, 0, 256, 256, 16)    // Wood floor

SetTexture(DEV)
Brush(0, 0, 16, 256, 16, 128)   // Dev-textured wall
```

**Available Textures:**
| Alias | Full Path |
|-------|-----------|
| `DEV` | `DEV/DEV_MEASUREGENERIC01B` |
| `WOOD` | `CP_MANOR/WOOD_FLOOR01` |
| `SKYBOX` | `TOOLS/TOOLSSKYBOX` |

---

#### `Entity(type, x, y, z, {extra_data})`
Creates a point entity at the specified location.

```vma
// Add a light
Entity(light, 256, 256, 128, {"_light": "255 255 255 200"})
```

---

#### `SpawnPoint(team, x, y, z)`
Creates a player spawn point for the specified team.

```vma
SpawnPoint(Red, 128, 128, 32)
SpawnPoint(Blue, 384, 384, 32)

// Also accepts: R, 2 (Red) or B, Blu, 3 (Blue)
```

---

#### `BroadEntity({attributes}, {objects})`
Creates complex entities with nested objects (used primarily by the decompiler).

---

### Programming Features

#### Variables
```vma
floor_height = 0
wall_height = 256

Brush(0, 0, floor_height, 512, 512, 16)
Brush(0, 0, 16, 16, 512, wall_height)
```

#### Expressions
```vma
base_x = 100
offset = base_x + 50    // Evaluates to 150

room_size = 512
half_room = room_size / 2
```

#### Comments
```vma
// Single-line comment
Brush(0, 0, 0, 64, 64, 64)    // Inline comment

# Python-style comments also work
```

---

## 🔄 Bidirectional Conversion

### Compile: VMA → VMF
```bash
python compile.py my_map.vma
# Output: my_map.vmf
```

### Decompile: VMF → VMA
```python
from VMFDecompiler import VMFDecompiler

decompiler = VMFDecompiler("existing_map.vmf")
decompiler.save_to_vma()
# Output: existing_map.vma
```

The decompiler:
1. Parses the nested VMF structure recursively
2. Extracts brush dimensions from vertex data
3. Identifies the most common texture per brush (ignoring NODRAW)
4. Reconstructs VMA commands that would generate equivalent geometry

---

## 🤖 AI Integration Guide

### Why VMA Works for AI

| Challenge | How VMA Solves It |
|-----------|-------------------|
| Token efficiency | A 1000-brush map in VMA is ~50× smaller than the equivalent VMF |
| Learning curve | 4 core commands vs. hundreds of VMF fields |
| Validation | Simple syntax means fewer malformed outputs |
| Iteration | AI can reason about "make the room bigger" as simple parameter changes |

### Example Prompt Engineering

```
You are a map designer using VMA (Valve Map Abstraction).
Generate a simple arena map with:
- A 1024x1024 unit floor
- Walls around the perimeter (256 units tall, 32 units thick)
- Red spawn on the west side
- Blue spawn on the east side
- A central raised platform

Commands available:
- Brush(x, y, z, width, depth, height)
- SetTexture(DEV | WOOD | SKYBOX)
- SpawnPoint(Red|Blue, x, y, z)
```

### Sample AI Output
```vma
// Floor
SetTexture(WOOD)
Brush(-512, -512, 0, 1024, 1024, 16)

// Walls (32 units thick, 256 tall)
SetTexture(DEV)
Brush(-512, -512, 16, 1024, 32, 256)   // North
Brush(-512, 480, 16, 1024, 32, 256)    // South
Brush(-512, -480, 16, 32, 960, 256)    // West
Brush(480, -480, 16, 32, 960, 256)     // East

// Central platform
Brush(-128, -128, 16, 256, 256, 64)

// Spawn points
SpawnPoint(Red, -400, 0, 32)
SpawnPoint(Blue, 400, 0, 32)
```

---

## 🛠️ Extending VMA

### Adding New Commands

Create a new file in `commands/`:

```python
# commands/my_command.py
from CommandRegistry import command
from Map import Map

@command(
    example="MyCommand(param1, param2)",
    notes="What this command does"
)
def mycommand(current_map: Map, parameters: list):
    """
    Docstring describing the command.
    
    Parameters:
        parameters (list): Description of expected parameters
    """
    # Implementation
    pass
```

The `@command` decorator automatically:
- Registers the command in the global registry
- Makes it available in VMA scripts (case-insensitive)
- Includes it in auto-generated documentation

### Adding New Textures

Edit `Data/Constants/textures.json`:
```json
{
    "DEV": "DEV/DEV_MEASUREGENERIC01B",
    "WOOD": "CP_MANOR/WOOD_FLOOR01",
    "BRICK": "BRICK/BRICKWALL001",
    "METAL": "METAL/METALFLOOR001"
}
```

---

## 📁 Project Structure

```
VMA/
├── compile.py                 # CLI entry point
├── VMACompiler.py             # Main compiler class
├── VMFDecompiler.py           # VMF → VMA converter
├── Map.py                     # Map state container
│
├── VMAInterpreter/            # Language interpreter
│   ├── Interpreter.py         # Main interpreter loop
│   ├── CommandExecutor.py     # Command dispatch
│   ├── VariableManager.py     # Variable scoping & evaluation
│   └── ForLoopHandler.py      # Loop processing
│
├── VMFCodeFactories/          # VMF code generation
│   ├── BrushFactory.py        # Solid geometry generation
│   ├── EntityFactory.py       # Entity generation
│   └── SideFactory.py         # Face/plane calculations
│
├── commands/                  # Command implementations
│   ├── brush.py
│   ├── entity.py
│   ├── settexture.py
│   └── spawnpoint.py
│
├── Data/
│   ├── Constants/             # Texture & entity definitions
│   └── Prefabs/               # VMF template fragments
│
├── CommandRegistry.py         # Decorator-based registration
├── ParameterExtractor.py      # Argument parsing
├── geometry_operations.py     # 3D math utilities
├── ErrorLog.py                # Error tracking
├── FileHandler.py             # I/O utilities
├── PrefabLoader.py            # Template loading
└── template.txt               # Base VMF structure
```

---

## 🧪 Technical Highlights

### Geometry Engine
The `SideFactory` computes proper texture alignment using:
- **Cross products** for perpendicular axis calculation
- **Dot products** to find the dominant surface orientation
- **Normal vectors** derived from plane definitions

### Parser Design
The VMF decompiler handles Valve's non-standard format using:
- **Stack-based parsing** for nested structures
- **Quote-aware tokenization** to handle embedded strings
- **Recursive descent** for arbitrary nesting depth

### Interpreter Architecture
The VMA interpreter features:
- **Context-based variable scoping** for nested loops
- **Expression evaluation** via safe `eval()` with variable substitution
- **Dynamic command loading** via `pkgutil.iter_modules()`

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- No external dependencies

### Basic Usage

1. **Create a VMA file** (`my_map.vma`):
```vma
SetTexture(DEV)
Brush(0, 0, 0, 512, 512, 16)
SpawnPoint(Red, 256, 256, 32)
```

2. **Compile to VMF**:
```bash
python compile.py my_map.vma
```

3. **Open in Hammer** or compile with VBSP/VVIS/VRAD for your Source game.

---

## 📜 License

BSD 3-Clause License — See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

This project was made possible by:
- Extensive analysis of official Valve map files
- The Source SDK documentation community
- The dream of AI-generated playable game content

---

<div align="center">

**Built with curiosity, reverse engineering, and a vision for AI-assisted game development.**

*"The best way to understand a format is to rebuild it from scratch."*

</div>
