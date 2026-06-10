from build123d import *
from ocp_vscode import show

POINTS_3D = [
    (-645.0,  -158.2843, 164.238),
    (-645.0,   138.2843, 164.238),
    (-558.2843, 225.0,   164.238),
    ( 558.2843, 225.0,   164.238),
    ( 645.0,   138.2843, 164.238),
    ( 645.0,  -158.2843, 164.238),
    ( 558.2843,-245.0,   164.238),
    (-558.2843,-245.0,   164.238),
]
rect_pts = [
    (185.194, 255.0, 164.238),
    (-185.194, 255.0, 164.238),
    (-185.194, 255.0, 36.0),
    (185.194, 255.0, 36.0),
]
circle_pts = [
        ( 379.988,  85.106, 164.238),
        ( 279.988,   0.106, 164.238),
        ( 379.988, -84.894, 164.238),
        ( 479.988,   0.106, 164.238),
    ]
plus_pts = [
        (-430.0,  135.0,   164.238),
        (-330.012, 135.0,  164.238),
        (-330.012,  50.106, 164.238),
        (-230.012,  50.106, 164.238),
        (-230.012, -50.106, 164.238),
        (-330.012, -50.106, 164.238),
        (-330.012, -135.0,  164.238),
        (-430.0,  -135.0,  164.238),
        (-430.0,  -50.106, 164.238),
        (-530.0,  -50.106, 164.238),
        (-530.0,   50.106, 164.238),
        (-430.0,   50.106, 164.238),
    ]
u_pts = [
        ( 176.194, 225.0,    134.238),
        ( 176.194,  15.4704, 134.238),
        (-176.194,  15.4704, 134.238),
        (-176.194, 225.0,    134.238),
        (-156.194, 225.0,    134.238),
        (-156.194,  35.4704, 134.238),
        ( 156.194,  35.4704, 134.238),
        ( 156.194, 225.0,    134.238),
    ]
ring_pts = [
        (-525.0, -125.0, 134.238),
        (-525.0,  125.0, 134.238),
        ( 525.0,  125.0, 134.238),
        ( 525.0, -125.0, 134.238),
    ]
concentric_pts = [
        (279.988,   0.106, 134.238),
        (379.988,  85.106, 134.238),
        (479.988,   0.106, 134.238),
        (379.988, -84.894, 134.238),
    ]
rect_sets = [
        [
            ( 389.988,  145.2668, 59.5),
            ( 369.988,  145.2668, 59.5),
            ( 369.988, -145.0548, 59.5),
            ( 389.988, -145.0548, 59.5),
        ],
        [
            ( 540.1488,  10.106, 59.5),
            ( 540.1488,  -9.894, 59.5),
            ( 219.8272,  -9.894, 59.5),
            ( 219.8272,  10.106, 59.5),
        ],
        [
            (289.988, 60.2668, 59.5),
            (269.988, 60.2668, 59.5),
            (269.988, -60.0548, 59.5),
            (289.988, -60.0548, 59.5),
        ],
        [
            (489.988, 60.2668, 59.5),
            (469.988, 60.2668, 59.5),
            (469.988, -60.0548, 59.5),
            (489.988, -60.0548, 59.5),
        ],
        [
            (440.1488, 95.106, 59.5),
            (440.1488, 75.106, 59.5),
            (319.8272, 75.106, 59.5),
            (319.8272, 95.106, 59.5),
        ],
        [
            (440.1488, -74.894, 59.5),
            (440.1488, -94.894, 59.5),
            (319.8272, -94.894, 59.5),
            (319.8272, -74.894, 59.5),
        ],
    ]

profile_pts   = [(p[0], p[1]) for p in POINTS_3D]
sketch_z      = POINTS_3D[0][2]
extrude_depth = 30
taper_angle   = -45.0

with BuildPart() as part:
    with BuildSketch(Plane(origin=(0, 0, sketch_z), z_dir=(0, 0, 1))):
        Polygon(*profile_pts, align=None)

    extrude(amount=-extrude_depth, taper=taper_angle)

    # First bottom face (after taper extrusion)
    bottom_face = part.faces().sort_by(Axis.Z)[0]
    extrude(to_extrude=bottom_face, amount=98.237996101,mode=Mode.ADD)

    # Offset the bottom face inward by 10 mm
    new_bottom_face = part.faces().sort_by(Axis.Z)[0]
    inner_face = offset(new_bottom_face, amount=-10.0)

    # Extrude the inner face upward to cut into the second body
    extrude(to_extrude=inner_face, amount=-98.237996101, mode=Mode.SUBTRACT)
    rect_2d = [(p[0], p[2]) for p in rect_pts]  # (x, z) pairs
    cut_plane = Plane(origin=(0, 255.0, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))

    with BuildSketch(cut_plane) as rect_sketch:
        Polygon(*rect_2d, align=None)

    extrude(to_extrude=rect_sketch.sketch, amount=30.0, mode=Mode.SUBTRACT)
    circle_plane = Plane(origin=(0, 0, 164.238), z_dir=(0, 0, 1))

    with BuildSketch(circle_plane) as circle_sketch:
        for pt in circle_pts:
            with Locations((pt[0], pt[1])):
                Circle(radius=50.0)

    extrude(to_extrude=circle_sketch.sketch, amount=-30.0, mode=Mode.SUBTRACT)
    plus_2d = [(p[0], p[1]) for p in plus_pts]  # (x, y) pairs

    plus_plane = Plane(origin=(0, 0, 164.238), z_dir=(0, 0, 1))

    with BuildSketch(plus_plane) as plus_sketch:
        Polygon(*plus_2d, align=None)

    extrude(to_extrude=plus_sketch.sketch, amount=-30.0, mode=Mode.SUBTRACT)

    u_2d = [(p[0], p[1]) for p in u_pts]  # (x, y) pairs

    u_plane = Plane(origin=(0, 0, 134.238), z_dir=(0, 0, 1))

    with BuildSketch(u_plane) as u_sketch:
        Polygon(*u_2d, align=None)

    extrude(to_extrude=u_sketch.sketch, amount=-118.237996101)
    ring_plane = Plane(origin=(0, 0, 134.238), z_dir=(0, 0, 1))

    with BuildSketch(ring_plane) as ring_sketch:
        for pt in ring_pts:
            with Locations((pt[0], pt[1])):
                Circle(radius=25.0)          # outer circle
                Circle(radius=11.0, mode=Mode.SUBTRACT)  # inner hole → creates ring

    extrude(to_extrude=ring_sketch.sketch, amount=-118.237996101)
    concentric_plane = Plane(origin=(0, 0, 164.238), z_dir=(0, 0, 1))

    with BuildSketch(concentric_plane) as concentric_sketch:
        for pt in concentric_pts:
            with Locations((pt[0], pt[1])):
                Circle(radius=60.0)                          # outer circle
                Circle(radius=50.0, mode=Mode.SUBTRACT)      # inner hole → creates ring

    extrude(to_extrude=concentric_sketch.sketch, amount=-104.737992287)
    rect_plane = Plane(origin=(0, 0, 59.5), z_dir=(0, 0, 1))

    with BuildSketch(rect_plane) as rect_sketches:
        for pts in rect_sets:
            pts_2d = [(p[0], p[1]) for p in pts]
            Polygon(*pts_2d, align=None)

    extrude(to_extrude=rect_sketches.sketch, amount=74.737992287,mode=Mode.SUBTRACT)

    ellipse_center = (-379.9262, 0.2528)
    ellipse_plane  = Plane(origin=(0, 0, 134.238), z_dir=(0, 0, 1))

    with BuildSketch(ellipse_plane) as ellipse_sketch:
        with Locations(ellipse_center):
            Ellipse(x_radius=344.8175 / 2, y_radius=308.0723 / 2)              # outer ellipse
            Ellipse(x_radius=(344.8175 / 2) - 10.0,
                    y_radius=(308.0723 / 2) - 10.0,
                    mode=Mode.SUBTRACT)                                          # inner ellipse → ring

    extrude(to_extrude=ellipse_sketch.sketch, amount=-74.737992287)
    single_ring_center = (0.0, -125.0)

    single_ring_plane = Plane(origin=(0, 0, 134.238), z_dir=(0, 0, 1))

    with BuildSketch(single_ring_plane) as single_ring_sketch2:
        with Locations(single_ring_center):
            Circle(radius=40.0)                        # outer circle
            Circle(radius=26.0, mode=Mode.SUBTRACT)    # inner hole → creates ring

    extrude(to_extrude=single_ring_sketch2.sketch, amount=-118.237996101)

shape = part.part

export_step(shape, "CAD_Files/Retropad_topPad.step")
export_stl( shape, "CAD_Files/Retropad_topPad.stl")


show(shape, names=["Retropad_topPad"])