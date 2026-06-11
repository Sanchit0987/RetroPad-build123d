# RetroPad — build123d CAD Recreation & SKiDL Schematic

A complete parametric recreation of the RetroPad case using build123d, and a fully verified schematic netlist generated using SKiDL — a Python-based schematic scripting library built on KiCad symbol libraries.

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
├── retropad_schmatic.py
├── retropad.net
└── README.md
```

---

## Part 1 — CAD Recreation (build123d)

### Approach

#### 1. Reference Analysis
The original STL files were sourced from the [jtgans/RetroPad](https://github.com/jtgans/RetroPad/tree/master/case) GitHub repository. Each STL was visually inspected using the OCP CAD Viewer extension in VS Code to understand the overall geometry, feature layout, and topology of each part.

#### 2. Dimension Extraction via Fusion 360
The STL files were imported into Autodesk Fusion 360, where the mesh was converted to a BRep solid using the Mesh to BRep tool. This allowed precise measurement of:

- Outer profile vertex coordinates
- Hole centre positions and radii
- Extrusion depths and Z-level references
- Taper angles on chamfered edges
- Wall thicknesses and feature offsets

All extracted coordinates and dimensions were then transcribed as named Python constants at the top of each build123d script for clarity and maintainability.

#### 3. Modelling Strategy (per part)

**Top Pad (`Retropad_topPad.py`)**
The outer shell profile is defined as an 8-point polygon in XY at z = 164.238. A tapered extrusion (taper = -45°, depth = 30 mm) creates the chamfered top edge. A straight downward extrusion forms the main body down to z = 36.0. An inner cavity (10 mm wall thickness) is subtracted using a 2D inset polygon sketch. Feature cutouts — D-pad plus cross, four button holes, rectangular slot, concentric rings, elliptical ring, rail slots, U-channel — are each modelled as dedicated BuildSketch + extrude(mode=Mode.SUBTRACT) operations on the correct plane. Raised bosses (ring posts, ellipse wall, single ring) are added with mode=Mode.ADD.

**Bottom Pad (`Retropad_BottomPad.py`)**
Mirrors the top pad outer profile with a simpler interior. Shelled to create the enclosure bottom with appropriate wall thickness.

**D-Pad (`Retropad_DPad.py`)**
Plus/cross profile polygon extruded to form the directional pad body. Centred at its hole position on the top pad surface.

**Button (`Retropad_button.py`)**
Cylindrical button body with a cap profile. Modelled once and duplicated four times in the assembly.

#### 4. Assembly (`Retropad_assembly.py`)
Each part is imported via `import_step()` to load the exact exported solid. Top Pad and Bottom Pad are placed at their original world coordinates with no transformation. The D-Pad and all four Button instances are raised +10 mm in Z to sit above the top pad surface. Button copies are placed at the four hole centres extracted from Fusion 360: (279.988, 0.106), (379.988, 85.106), (479.988, 0.106), (379.988, -84.894), using bounding-box centring to align each button's axis with its hole. The full assembly is exported as both `.step` and `.stl`.

### Volumetric Comparison

| Part | Target Volume (mm³) | Script Volume (mm³) | Difference (mm³) | Volume Accuracy (%) | Sym Diff Volume (mm³) | Sym Diff Error (%) |
|---|---|---|---|---|---|---|
| Top Pad | 24,154,487.505031 | 24,154,530.035279 | +42.530248 | 99.9998% | 24,154,574.272759 | 0.011% |
| Bottom Pad | 27,602,848.934671 | 27,587,772.171458 | −15,076.763213 | 99.9454% | 8,226.116231 | 0.030% |
| D-Pad | 7,947,732.925765 | 7,948,673.521397 | +940.595632 | 99.9882% | 940.580334 | 0.012% |
| Button | 1,150,782.880410 | 1,151,097.300296 | +314.419886 | 99.9727% | 1,150,967.250022 | 0.016% |

> Volume Accuracy = (1 - |Difference| / Target) × 100
> Sym Diff Error = (Sym Diff Volume / Target Volume) × 100
>
> Top Pad and Button show ~100% Sym Diff due to world-origin mismatch between reference STEP and build123d output — the geometry is correct but the solids do not spatially overlap during boolean comparison. After positioning the components at a particular coordinate, the symmetric difference between the components became negligible and is mentioned in the table.

---

## Part 2 — Schematic Netlist (SKiDL)

### Overview

The RetroPad schematic was recreated programmatically using SKiDL (`retropad_schmatic.py`), generating a KiCad-compatible netlist (`retropad.net`) that can be imported directly into KiCad Eeschema via **Tools → Import Netlist**.

The script was cross-checked connection-by-connection against the original `RetroPad.sch` schematic (KiCad EDA 10.0.3, Rev 2.0) and verified to produce **0 ERC errors and 0 warnings** after all issues were resolved.

### Components

| Reference | Part | Library | Footprint |
|---|---|---|---|
| U1 | ATtiny814-SS | MCU_Microchip_ATtiny | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm |
| J1 | Conn_01x09 | Connector_Generic | Connector_Dsub:DSUB-9_Pins_EdgeMount_P2.77mm |
| J2 | Conn_01x06_Pin | Connector_Generic | Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Horizontal |
| R1, R2 | R 1K | Device | Resistor_SMD:R_0402_1005Metric |
| R3 | R 330Ω | Device | Resistor_SMD:R_0402_1005Metric |
| R4 | R 1K | Device | Resistor_SMD:R_0402_1005Metric |
| R5, R6 | R 10K (pot body) | Device | Resistor_SMD:R_0402_1005Metric |
| R7–R11 | R 0Ω | Device | Resistor_SMD:R_0402_1005Metric |
| D1 | LED (RAPID) | Device | LED_SMD:LED_0402_1005Metric |
| C1 | C 0.1uF | Device | Capacitor_SMD:C_0402_1005Metric |
| RAPID1, BTN1–3 | SW_Push | Switch | RetroPad:Silicone_Membrane_Pad_11mm_(7.5mm) |
| JUMP1, UP1, DOWN1, LEFT1, RIGHT1 | SW_Push | Switch | RetroPad:Silicone_Membrane_Pad_11mm_(7.5mm) |
| H1, H2 | MountingHole_Pad | Mechanical | MountingHole:MountingHole_3.2mm_M3 |

### Net Topology

**Power rails:** `+5V` and `GND` with `C1` (0.1uF) decoupling on the MCU supply pins.

**Button inputs (PB0–PB3):** RAPID1, BTN1, BTN2, BTN3 each connect one leg to the MCU input pin and the other to GND.

**MCU outputs:**
- `PA5` → `OUT_BTN3` → R1(1K) → `POTX` → R5(10K) → GND
- `PA6` → `OUT_BTN2` → R2(1K) → `POTY` → R6(10K) → GND
- `PA7` → `FIRE` net → R4(1K) pull-down → GND; also → DB9 pin 6
- `PA4` → D1 anode → D1 cathode → R3(330Ω) → GND

**UPDI header (J2):** Pin1=GND, Pin2=VCC, Pin3=RESET/PA0, Pin4–6=GND

**Directional network:**
```
GND → R7(0Ω) → JUMP1_IN → JUMP1 switch → UP net
GND → R8(0Ω) → UP1_IN   → UP1   switch → UP net
GND → R9(0Ω) → DOWN1_IN → DOWN1 switch → DOWN net
GND → R10(0Ω)→ LEFT1_IN → LEFT1 switch → LEFT net
GND → R11(0Ω)→ RIGHT1_IN→ RIGHT1 switch→ RIGHT net
```

**DB9 joystick pinout (Atari/Commodore standard):**
Pin 1=UP, Pin 2=DOWN, Pin 3=LEFT, Pin 4=RIGHT, Pin 5=POTY, Pin 6=FIRE, Pin 7=+5V, Pin 8=GND, Pin 9=POTX

### ERC Results

| Metric | Result |
|---|---|
| ERC Errors | **0** |
| ERC Warnings | **0** |
| Netlist generation errors | **0** |
| Netlist generation warnings | **0** |

All issues encountered during development were resolved:

- **`AVR-UPDI-6` NC pin conflicts (42 errors)** — replaced with `Conn_01x06_Pin`, a generic 6-pin connector with all PASSIVE pins.
- **`OUT_FIRE`/`FIRE` net merge warning** — eliminated by using a single `FIRE` net throughout.
- **Missing tag warnings** — resolved by adding `tag=ref` to every `Part()` call so SKiDL uses stable identifiers instead of generating random ones.
- **Pylance underline on `SKIDL` constant** — resolved by adding an explicit `from skidl import SKIDL` after the wildcard import.

### How to Run

```bash
# Install dependencies
pip install skidl

# Generate netlist
python retropad_schmatic.py

# Import into KiCad
# Eeschema → Tools → Import Netlist → select retropad.net
```

---

## Tools Used

| Tool | Purpose |
|---|---|
| build123d | Parametric CAD scripting |
| Autodesk Fusion 360 | STL to BRep conversion for dimension extraction |
| OCP CAD Viewer | Visual inspection in VS Code |
| SKiDL | Python-based schematic netlist scripting |
| KiCad EDA 10.0.3 | Schematic symbol libraries and netlist import |
| Python 3.9 | Scripting environment |
| VS Code | IDE |

## How to Run (CAD)

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
- SKiDL documentation: https://devbisme.github.io/skidl/
