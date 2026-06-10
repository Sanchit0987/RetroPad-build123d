from build123d import *
from ocp_vscode import show

# ---------------------------------------------------------------------------
# 1.  Define the base 8 corner points (all lie on z = -60.0)
# ---------------------------------------------------------------------------
points_2d = [
    (-675.0,   -170.7107),
    (-570.7107, -275.0),
    ( 570.7107, -275.0),
    ( 675.0,   -170.7107),
    ( 675.0,    150.7107),
    ( 570.7107,  255.0),
    (-570.7107,  255.0),
    (-675.0,    150.7107),
]

# Second profile points on the top face (z = 134.238)
points_top = [
    (-562.4264,  235.0,    134.238),
    (-655.0,     142.4264, 134.238),
    (-655.0,    -162.4264, 134.238),
    (-562.4264, -255.0,    134.238),
    ( 562.4264, -255.0,    134.238),
    ( 655.0,   -162.4264,  134.238),
    ( 655.0,    142.4264,  134.238),
    ( 562.4264,  235.0,    134.238),
]

# Cylinder base positions (set 1)
cyl_points = [
    (-525.0,  125.0, -30.0),
    (-525.0, -125.0, -30.0),
    ( 525.0, -125.0, -30.0),
    ( 525.0,  125.0, -30.0),
]

Z_BASE          = -60.0
EXTRUDE_H       =  194.23    # mm, upward (+Z)
INSET           =   10.0     # mm, inside offset on top face (ring cut)
CUT_DEPTH       =   98.745   # mm, ring cut depth downward
BOTTOM_CHAMFER  =   30.0     # mm, chamfer on bottom face edges
CUT_DEPTH_2     =  164.237   # mm, second profile cut depth downward
CYL_RADIUS      =   25.0     # mm  (set 1)
CYL_HEIGHT      =   30.0     # mm  (set 1)

# ---------------------------------------------------------------------------
# 2.  Build the closed 2-D wire on the XY plane, then make a face
# ---------------------------------------------------------------------------
with BuildSketch(Plane.XY.offset(Z_BASE)) as sk:
    with BuildLine() as bl:
        pts = [Vector(x, y) for x, y in points_2d]
        Polyline(*pts, close=True)
    make_face()

# ---------------------------------------------------------------------------
# 3.  Extrude upward
# ---------------------------------------------------------------------------
with BuildPart() as part:
    add(sk.sketch)
    extrude(amount=EXTRUDE_H)

    # -----------------------------------------------------------------------
    # 4.  Annular ring cut on top face (outer band, 10 mm inset, 98.745 deep)
    # -----------------------------------------------------------------------
    z_top = Z_BASE + EXTRUDE_H          # = 134.23 mm

    with BuildSketch(Plane.XY.offset(z_top)) as sk_outer:
        with BuildLine():
            Polyline(*[Vector(x, y) for x, y in points_2d], close=True)
        make_face()

    with BuildSketch(Plane.XY.offset(z_top)) as sk_inner:
        with BuildLine():
            Polyline(*[Vector(x, y) for x, y in points_2d], close=True)
        make_face()
        offset(amount=-INSET)

    ring_face = sk_outer.sketch - sk_inner.sketch
    extrude(ring_face, amount=-CUT_DEPTH, mode=Mode.SUBTRACT)

    # -----------------------------------------------------------------------
    # 5.  Second profile cut — new 8-point shape, 164.237 mm deep
    # -----------------------------------------------------------------------
    z_top2 = points_top[0][2]           # 134.238 mm

    with BuildSketch(Plane.XY.offset(z_top2)) as sk_cut2:
        with BuildLine():
            Polyline(
                *[Vector(x, y) for x, y, z in points_top],
                close=True,
            )
        make_face()

    extrude(sk_cut2.sketch, amount=-CUT_DEPTH_2, mode=Mode.SUBTRACT)

    # -----------------------------------------------------------------------
    # 6.  Chamfer all edges on the bottom face by 30 mm
    # -----------------------------------------------------------------------
    bottom_edges = part.edges().filter_by(
        lambda e: abs(e.center().Z - Z_BASE) < 1e-3
    )
    chamfer(bottom_edges, length=BOTTOM_CHAMFER)

    # -----------------------------------------------------------------------
    # 7.  Add 4 cylinders (r=25 mm, h=30 mm) at cyl_points, upward
    # -----------------------------------------------------------------------
    for cx, cy, cz in cyl_points:
        cyl_plane = Plane(origin=(cx, cy, cz), x_dir=(1,0,0), z_dir=(0,0,1))
        with BuildSketch(cyl_plane) as sk_cyl:
            Circle(CYL_RADIUS)
        extrude(sk_cyl.sketch, amount=CYL_HEIGHT, mode=Mode.ADD)

    # -----------------------------------------------------------------------
    # 8.  Add 4 cylinders (r=10 mm, h=134.237 mm) from z=0.0 upward
    # -----------------------------------------------------------------------
    cyl_points_2 = [
        (-525.0,  125.0, 0.0),
        (-525.0, -125.0, 0.0),
        ( 525.0, -125.0, 0.0),
        ( 525.0,  125.0, 0.0),
    ]
    for cx, cy, cz in cyl_points_2:
        cyl_plane = Plane(origin=(cx, cy, cz), x_dir=(1,0,0), z_dir=(0,0,1))
        with BuildSketch(cyl_plane) as sk_cyl2:
            Circle(10.0)
        extrude(sk_cyl2.sketch, amount=134.237, mode=Mode.ADD)

    # -----------------------------------------------------------------------
    # 9.  Single cylinder: r=40 mm, h=30 mm at (0, -125, -30)
    # -----------------------------------------------------------------------
    cyl_plane_a = Plane(origin=(0.0, -125.0, -30.0), x_dir=(1,0,0), z_dir=(0,0,1))
    with BuildSketch(cyl_plane_a) as sk_cyl_a:
        Circle(40.0)
    extrude(sk_cyl_a.sketch, amount=30.0, mode=Mode.ADD)

    # -----------------------------------------------------------------------
    # 10. Single cylinder: r=25 mm, h=134.237 mm at (0, -125, 0)
    # -----------------------------------------------------------------------
    cyl_plane_b = Plane(origin=(0.0, -125.0, 0.0), x_dir=(1,0,0), z_dir=(0,0,1))
    with BuildSketch(cyl_plane_b) as sk_cyl_b:
        Circle(25.0)
    extrude(sk_cyl_b.sketch, amount=134.237, mode=Mode.ADD)

    # -----------------------------------------------------------------------
    # 11. Ellipse rings at 2 points — SINGLE definition, no duplication.
    #     Outer ellipse: semi_x=105.453, semi_y=90.0155
    #     Inner ellipse: semi_x -= 10, semi_y -= 10  → guaranteed 10 mm wall
    #     Ring extruded 30 mm upward from z=-30.
    #
    #     Using explicit inner semi-axes instead of offset() to ensure
    #     the wall is exactly 10 mm thick rather than a near-zero surface.
    # -----------------------------------------------------------------------
    ellipse_points = [
        ( 379.993,  0.1036, -30.0),
        (-380.2534, 0.0408, -30.0),
    ]
    ELLIPSE_SEMI_X       = 210.906 / 2        # 105.453 mm — semi-axis along X
    ELLIPSE_SEMI_Y       = 180.031 / 2        #  90.0155 mm — semi-axis along Y
    ELLIPSE_WALL         =  10.0              # mm wall thickness
    ELLIPSE_INNER_SEMI_X = ELLIPSE_SEMI_X - ELLIPSE_WALL   # 95.453 mm
    ELLIPSE_INNER_SEMI_Y = ELLIPSE_SEMI_Y - ELLIPSE_WALL   # 80.0155 mm
    ELLIPSE_H            =  30.0              # mm extrusion height

    for ex, ey, ez in ellipse_points:
        e_plane = Plane(origin=(ex, ey, ez), x_dir=(1,0,0), z_dir=(0,0,1))

        # outer ellipse face
        with BuildSketch(e_plane) as sk_ell_outer:
            Ellipse(ELLIPSE_SEMI_X, ELLIPSE_SEMI_Y)

        # inner ellipse face — explicitly smaller semi-axes = exact 10 mm wall
        with BuildSketch(e_plane) as sk_ell_inner:
            Ellipse(ELLIPSE_INNER_SEMI_X, ELLIPSE_INNER_SEMI_Y)

        # annular ring = outer minus inner → solid 10 mm thick wall
        ellipse_ring = sk_ell_outer.sketch - sk_ell_inner.sketch

        # extrude the 10 mm ring band upward 30 mm
        extrude(ellipse_ring, amount=ELLIPSE_H, mode=Mode.ADD)

    # -----------------------------------------------------------------------
    # 12. Rectangle on the vertical plane Y=235.0, cut 20.1 mm into body
    #     Points span X: -185.194 to 185.194, Z: -14.0 to 134.238
    #     Sketch plane: XZ plane at y=235.0, cutting inward (-Y direction)
    # -----------------------------------------------------------------------
    # Plane at y=235, normal pointing in +Y, so extrude negative = cut inward
    rect_plane = Plane(
        origin=(0.0, 235.0, 0.0),   # centred in X, at y=235, z=0 (arbitrary origin on plane)
        x_dir=(1, 0, 0),            # X axis along world X
        z_dir=(0, 1, 0),            # normal pointing +Y → extrude in -Y to cut inward
    )

    # Rectangle dimensions derived from the 4 points:
    #   width  (X): 185.194 - (-185.194) = 370.388 mm
    #   height (Z): 134.238 - (-14.0)    = 148.238 mm
    #   centre (X): 0.0
    #   centre (Z): (-14.0 + 134.238) / 2 = 60.119 mm  → offset origin to match
    rect_plane_centred = Plane(
        origin=(0.0, 235.0, (-14.0 + 134.238) / 2),
        x_dir=(1, 0, 0),
        z_dir=(0, 1, 0),
    )
    RECT_W     = 185.194 * 2          # 370.388 mm
    RECT_H     = 134.238 - (-14.0)    # 148.238 mm
    RECT_CUT   = 20.1                 # mm, cut inward (-Y)

    with BuildSketch(rect_plane_centred) as sk_rect:
        Rectangle(RECT_W, RECT_H)

    extrude(sk_rect.sketch, amount=RECT_CUT, mode=Mode.SUBTRACT)

solid = part.part

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
export_step(solid, "CAD_Files/Retropad_Bottompad.step")
export_stl(solid, "CAD_Files/Retropad_Bottompad.stl")

show(solid, names=["Retropad_Bottompad"])