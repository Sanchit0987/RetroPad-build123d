from build123d import *
from ocp_vscode import show, show_all

# ─────────────────────────────────────────────────────────────────────────────
# Retropad Assembly
# All parts at their original world XY positions.
# DPad and Buttons shifted +10 mm in Z only.
# TopPad and BottomPad stay exactly as built.
# ─────────────────────────────────────────────────────────────────────────────

STEP_DIR = "CAD_Files"
Z_LIFT   = 10   # mm

HOLES = [
    (279.988,   0.106),
    (379.988,  85.106),
    (479.988,   0.106),
    (379.988, -84.894),
]

# ── Import ────────────────────────────────────────────────────────────────────
top_pad    = import_step(f"{STEP_DIR}/Retropad_topPad.step")
bottom_pad = import_step(f"{STEP_DIR}/Retropad_BottomPad.step")
dpad       = import_step(f"{STEP_DIR}/Retropad_DPad.step")
button     = import_step(f"{STEP_DIR}/Retropad_button.step")

# ── DPad: +10 Z only ─────────────────────────────────────────────────────────
dpad_placed = dpad.moved(Location((0, 0, Z_LIFT)))

# ── Buttons: move each to its hole XY (absolute), same Z as original +10 ──────
# Get the button's original Z bottom so we only offset Z by 10
bb     = button.bounding_box()
btn_cx = (bb.min.X + bb.max.X) / 2
btn_cy = (bb.min.Y + bb.max.Y) / 2

button_instances = {}
for i, (hx, hy) in enumerate(HOLES):
    dx = hx - btn_cx   # centre button over hole
    dy = hy - btn_cy
    dz = Z_LIFT        # only 10 mm up, preserve original Z
    button_instances[f"Button_{i}"] = button.moved(Location((dx, dy, dz)))

# ── Assemble ──────────────────────────────────────────────────────────────────
assembly = Compound(
    label="Retropad_Assembly",
    children=[
        Compound(label="TopPad",    children=[top_pad]),
        Compound(label="BottomPad", children=[bottom_pad]),
        Compound(label="DPad",      children=[dpad_placed]),
        *[Compound(label=lbl, children=[part])
          for lbl, part in button_instances.items()],
    ],
)

# ── Export ────────────────────────────────────────────────────────────────────
export_step(assembly, "CAD_Files/Retropad_assembly.step")
export_stl( assembly, "CAD_Files/Retropad_assembly.stl")

# ── Visualise ─────────────────────────────────────────────────────────────────
show_all({
    "TopPad"    : top_pad,
    "BottomPad" : bottom_pad,
    "DPad"      : dpad_placed,
    **button_instances,
})