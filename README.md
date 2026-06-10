# RetroPad — build123d CAD Recreation

A complete parametric recreation of the [RetroPad case](https://github.com/jtgans/RetroPad/tree/master/case) using [build123d](https://build123d.readthedocs.io/en/latest/), a Python-based CAD scripting library built on OpenCASCADE.

---

## Project Structure

```
assignment/
├── CAD_Files/
│   ├── Retropad_topPad.step
│   ├── Retropad_topPad.stl
│   ├── Retropad_BottomPad.step
│   ├── Retropad_BottomPad.stl
│   ├── Retropad_DPad.step
│   ├── Retropad_DPad.stl
│   ├── Retropad_button.step
│   ├── Retropad_button.stl
│   ├── Retropad_assembly.step
│   └── Retropad_assembly.stl
├── Retropad_topPad.py
├── Retropad_BottomPad.py
├── Retropad_DPad.py
├── Retropad_button.py
├── Retropad_assembly.py
└── README.md
```

---

## Approach

### 1. Reference Analysis
The original STL files were sourced from the [jtgans/RetroPad GitHub repository](https://github.com/jtgans/RetroPad/tree/master/case). Each STL was visually inspected using the OCP CAD Viewer extension in VS Code to understand the overall geometry, feature layout, and topology of each part.

### 2. Dimension Extraction via Fusion 360
The STL files were imported into **Autodesk Fusion 360**, where the mesh was converted to a BRep solid using the *Mesh to BRep* tool. This allowed precise measurement of:
- Outer profile vertex coordinates
- Hole centre positions and radii
- Extrusion depths and Z-level references
- Taper angles on chamfered edges
- Wall thicknesses and feature offsets

All extracted coordinates and dimensions were then transcribed as named Python constants at the top of each build123d script for clarity and maintainability.

### 3. Modelling Strategy (per part)

#### Top Pad (`Retropad_topPad.py`)
- The outer shell profile is defined as an 8-point polygon in XY at `z = 164.238`.
- A tapered extrusion (`taper = -45°`, `depth = 30 mm`) creates the chamfered top edge.
- A straight downward extrusion forms the main body down to `z = 36.0`.
- An inner cavity (10 mm wall thickness) is subtracted using a 2D inset polygon sketch.
- Feature cutouts — D-pad plus cross, four button holes, rectangular slot, concentric rings, elliptical ring, rail slots, U-channel — are each modelled as dedicated `BuildSketch` + `extrude(mode=Mode.SUBTRACT)` operations on the correct plane.
- Raised bosses (ring posts, ellipse wall, single ring) are added with `mode=Mode.ADD`.

#### Bottom Pad (`Retropad_BottomPad.py`)
- Mirrors the top pad outer profile with a simpler interior.
- Shelled to create the enclosure bottom with appropriate wall thickness.

#### D-Pad (`Retropad_DPad.py`)
- Plus/cross profile polygon extruded to form the directional pad body.
- Centred at its hole position on the top pad surface.

#### Button (`Retropad_button.py`)
- Cylindrical button body with a cap profile.
- Modelled once and duplicated four times in the assembly.

### 4. Assembly (`Retropad_assembly.py`)
- Each part is imported via `import_step()` to load the exact exported solid.
- Top Pad and Bottom Pad are placed at their original world coordinates with no transformation.
- The D-Pad and all four Button instances are raised `+10 mm` in Z to sit above the top pad surface.
- Button copies are placed at the four hole centres extracted from Fusion 360: `(279.988, 0.106)`, `(379.988, 85.106)`, `(479.988, 0.106)`, `(379.988, -84.894)`, using bounding-box centring to align each button's axis with its hole.
- The full assembly is exported as both `.step` and `.stl`.

---

## Volumetric Comparison

| Part | Target Volume (mm³) | Script Volume (mm³) | Difference (mm³) | Symmetric Difference Volume (mm³) |
|------|-------------------|-------------------|-----------------|----------------------------------|
| Top Pad | | | | |
| Bottom Pad | | | | |
| D-Pad | | | | |
| Button | | | | |

> Values to be filled in after measurement.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| [build123d](https://build123d.readthedocs.io/) | Parametric CAD scripting |
| [Autodesk Fusion 360](https://www.autodesk.com/products/fusion-360/) | STL to BRep conversion for dimension extraction |
| [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer) | Visual inspection in VS Code |
| Python 3.9 | Scripting environment |
| VS Code | IDE |

---

## How to Run

### Prerequisites
```bash
pip install build123d ocp-vscode
```

### Generate each part
```bash
python Retropad_topPad.py
python Retropad_BottomPad.py
python Retropad_DPad.py
python Retropad_button.py
```

### Generate assembly
```bash
python Retropad_assembly.py
```

Output files are written to the `CAD_Files/` directory.

---

## References
- Original STL files: https://github.com/jtgans/RetroPad/tree/master/case
- build123d documentation: https://build123d.readthedocs.io/en/latest/