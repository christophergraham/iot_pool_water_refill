"""
Pool top-up unit: parametric 3D-printable enclosure
====================================================
Parts (one STL each):
  1. controller_box.stl   wall-mounted box: perfboard standoffs, 2 cable glands,
                          valve coil window + P-clip holes on the right-hand side,
                          4 corner wall-mount lugs, ribs for the tilt yoke
  2. controller_lid.stl   front lid with locating lip (add foam gasket tape)
  3. tilt_yoke.stl        bolts under the box; two ears with a pivot hole and
                          a curved lock slot (tilt -60..+60 degrees)
  4. radar_pod.stl        sealed pod: lens window in the base, blind pivot and
                          lock bosses (heat-set inserts, no holes into the pod)
  5. radar_pod_lid.stl    pod lid with M12 cable gland hole

Change the numbers in PARAMETERS, then run:
    pip install manifold3d trimesh numpy
    python pool_unit_model.py
All sizes in millimetres. Coordinates: x = left-right along the wall,
y = out from the wall (0 = wall), z = up (0 = underside of the box).
Facing the box, x = 0 is its RIGHT-hand side (x runs to your left).
"""
import math, os, sys
import numpy as np
import manifold3d as m3
import trimesh

# =============================== PARAMETERS ===============================
# --- Controller box (outside size) ---
BOX_W, BOX_D, BOX_H = 160.0, 80.0, 120.0   # width, depth from wall, height
WALL = 3.0                                  # wall thickness
BOSS = 10.0                                 # corner lid-screw column size
LID_SCREW_PILOT = 3.3                       # M4 self-tapping pilot (5.6 for M4 heat-set insert)
LUG_HOLE = 5.0                              # wall-mount screw holes in the lugs

# --- Cable glands in the box bottom (M16 gland needs a 16.5 mm hole) ---
GLAND_HOLE = 16.5
GLAND_X = (24.0, BOX_W - 24.0)              # radar cable (valve side), 12 V power in

# --- Solenoid valve on the right-hand wall as you face the box (x = 0) (MEASURE YOUR VALVE) ---
COIL_WIN_W = 30.0      # window width (front-back, y) for the coil's terminal end
COIL_WIN_H = 30.0      # window height (z)
COIL_WIN_Y = BOX_D / 2 # window centre, distance from wall
COIL_WIN_Z = 60.0      # window centre, height above box underside
PCLIP_HOLE = 5.5       # M5 bolts for the two P-clips
PCLIP_SPACING = 70.0   # distance between the two P-clip holes (vertical)

# --- Perfboard (7 x 9 cm) standoffs on the back wall (MEASURE YOUR HOLE SPACING) ---
# Board stands upright, 70 wide x 90 tall, on the LEFT as you face the box (high x),
# leaving the right side free for the HW-517 MOSFET module and the valve coil.
PERF_W, PERF_H = 70.0, 90.0
PERF_HOLE_DX, PERF_HOLE_DZ = 64.0, 84.0     # centre-to-centre of the corner holes
PERF_X = BOX_W - WALL - BOSS - 4.0 - PERF_W  # board's low-x edge
PERF_Z = (BOX_H - PERF_H) / 2                # centred vertically
UNO_X, UNO_Z = PERF_X + (PERF_W - PERF_HOLE_DX) / 2, PERF_Z + (PERF_H - PERF_HOLE_DZ) / 2
UNO_HOLES = [(0.0, 0.0), (PERF_HOLE_DX, 0.0), (0.0, PERF_HOLE_DZ), (PERF_HOLE_DX, PERF_HOLE_DZ)]
STANDOFF_H, STANDOFF_R, STANDOFF_PILOT = 8.0, 3.5, 2.6  # M3 self-tap; 8 mm clears solder joints

# --- Radar (DFRobot SEN0676 board is 35 x 35 mm; MEASURE THE LENS) ---
LENS_D = 40.0          # lens diameter at the point it passes through the pod base
POD_IN = 48.0          # pod inside width/depth (board 35 + room for the lens body)
POD_IN_H = 26.0        # pod inside height
POD_WALL = 3.0
POD_POST = 5.0         # corner posts for the pod lid screws
POD_SCREW_PILOT = 2.5  # M3 self-tap
POD_GLAND_HOLE = 12.5  # M12 cable gland in the pod lid

# --- Tilt hinge ---
PIVOT_DROP = 44.0      # pivot axis, distance below the box underside
PIVOT_Y = 50.0         # pivot axis, distance out from the wall
INSERT_HOLE = 6.4      # M5 heat-set insert hole (blind) in the pod bosses
INSERT_DEPTH = 9.0
PIVOT_HOLE = 5.5       # clearance hole for M5 in the ears
BOSS_R, BOSS_OUT = 9.0, 8.0   # pivot boss radius and how far it stands out
LOCK_R = 16.0          # lock bolt distance from the pivot (toward the wall)
TILT_MIN, TILT_MAX = -60.0, 60.0
EAR_T = 6.0            # ear thickness
YOKE_PLATE_T = 5.0
YOKE_PLATE_Y = 50.0    # plate size front-back
YOKE_SCREW_PILOT = 5.6 # M4 heat-set insert holes in the box bottom ribs
CLEAR = 0.5            # side clearance between pod bosses and ears

PREVIEW_TILT = 45.0    # tilt used for the assembly preview
SEG = 64
# ===========================================================================

m3.set_circular_segments(SEG)
M = m3.Manifold

def box(x, y, z, sx, sy, sz):
    return M.cube([sx, sy, sz]).translate([x, y, z])

def cyl_x(x0, length, y, z, r):   # cylinder along +x starting at x0
    return M.cylinder(length, r).rotate([0, 90, 0]).translate([x0, y, z])

def cyl_y(y0, length, x, z, r):   # cylinder along +y starting at y0
    return M.cylinder(length, r).rotate([-90, 0, 0]).translate([x, y0, z])

def cyl_z(z0, length, x, y, r):
    return M.cylinder(length, r).translate([x, y, z0])

def union(parts):
    return M.batch_boolean(parts, m3.OpType.Add)

# ---------------------------------------------------------------- box
POD_OUT = POD_IN + 2 * POD_WALL
EAR_GAP = POD_OUT + 2 * BOSS_OUT + 2 * CLEAR          # inside distance between ears
YOKE_W = EAR_GAP + 2 * EAR_T
YOKE_X0 = BOX_W / 2 - YOKE_W / 2
# four M4 screws hold the yoke plate to the ribs in the box bottom
YOKE_SCREWS = [(BOX_W / 2 + sx * (EAR_GAP / 2 - 6), PIVOT_Y + sy * (YOKE_PLATE_Y / 2 - 7))
               for sx in (-1, 1) for sy in (-1, 1)]

def controller_box():
    b = box(0, 0, 0, BOX_W, BOX_D, BOX_H)
    b = b - box(WALL, WALL, WALL, BOX_W - 2 * WALL, BOX_D, BOX_H - 2 * WALL)
    adds = []
    # corner columns for lid screws (run from the back wall to the front rim)
    for cx in (WALL, BOX_W - WALL - BOSS):
        for cz in (WALL, BOX_H - WALL - BOSS):
            adds.append(box(cx, WALL, cz, BOSS, BOX_D - WALL, BOSS))
    # ribs inside the bottom for the yoke inserts (full depth, printable)
    for x in sorted(set(round(sx, 3) for sx, _ in YOKE_SCREWS)):
        adds.append(box(x - 6, WALL, WALL, 12, BOX_D - WALL - 2, 7))
    # perfboard standoffs on the back wall
    for hx, hz in UNO_HOLES:
        adds.append(cyl_y(WALL, STANDOFF_H, UNO_X + hx, UNO_Z + hz, STANDOFF_R))
    # wall-mount lugs at the four corners, flush with the back face
    for lx in (-16, BOX_W):
        for lz in (8, BOX_H - 24):
            adds.append(box(lx, 0, lz, 16, 5, 16))
    b = union([b] + adds)

    cuts = []
    for cx in (WALL + BOSS / 2, BOX_W - WALL - BOSS / 2):
        for cz in (WALL + BOSS / 2, BOX_H - WALL - BOSS / 2):
            cuts.append(cyl_y(BOX_D - 16, 17, cx, cz, LID_SCREW_PILOT / 2))
    for hx, hz in UNO_HOLES:
        cuts.append(cyl_y(WALL + 0.5, STANDOFF_H + 1, UNO_X + hx, UNO_Z + hz, STANDOFF_PILOT / 2))
    for lx in (-8, BOX_W + 8):
        for lz in (16, BOX_H - 16):
            cuts.append(cyl_y(-1, 7, lx, lz, LUG_HOLE / 2))
    for gx in GLAND_X:
        cuts.append(cyl_z(-1, WALL + 2, gx, BOX_D / 2, GLAND_HOLE / 2))
    for sx, sy in YOKE_SCREWS:   # blind insert holes from underneath
        cuts.append(cyl_z(-1, 8.5, sx, sy, YOKE_SCREW_PILOT / 2))
    # valve coil window + P-clip holes in the right-hand wall (x = 0)
    cuts.append(box(-1, COIL_WIN_Y - COIL_WIN_W / 2, COIL_WIN_Z - COIL_WIN_H / 2,
                    WALL + 2, COIL_WIN_W, COIL_WIN_H))
    for dz in (-PCLIP_SPACING / 2, PCLIP_SPACING / 2):
        cuts.append(cyl_x(-1, WALL + 2, COIL_WIN_Y, COIL_WIN_Z + dz, PCLIP_HOLE / 2))
    return b - union(cuts)

def controller_lid():
    """Printed flat. Lid frame: x = box x, y = box z, z = thickness (0 = outside face)."""
    t = 3.0
    lid = box(0, 0, 0, BOX_W, BOX_H, t)
    c = 0.4
    ring = box(WALL + c, WALL + c, t, BOX_W - 2 * (WALL + c), BOX_H - 2 * (WALL + c), 5) - \
           box(WALL + c + 2, WALL + c + 2, t - 1, BOX_W - 2 * (WALL + c + 2), BOX_H - 2 * (WALL + c + 2), 7)
    notch = []
    for cx in (WALL, BOX_W - WALL - BOSS):
        for cz in (WALL, BOX_H - WALL - BOSS):
            notch.append(box(cx - c, cz - c, t - 1, BOSS + 2 * c, BOSS + 2 * c, 7))
    lid = lid + (ring - union(notch))
    holes = []
    for cx in (WALL + BOSS / 2, BOX_W - WALL - BOSS / 2):
        for cz in (WALL + BOSS / 2, BOX_H - WALL - BOSS / 2):
            holes.append(cyl_z(-1, t + 2, cx, cz, 4.5 / 2))
    return lid - union(holes)

# ---------------------------------------------------------------- yoke
def ear(x0):
    top = box(x0, -YOKE_PLATE_Y / 2, -YOKE_PLATE_T - 1, EAR_T, YOKE_PLATE_Y, 1)
    disc = cyl_x(x0, EAR_T, 0, -PIVOT_DROP, LOCK_R + 9)
    e = M.batch_hull([top, disc])
    cuts = [cyl_x(x0 - 1, EAR_T + 2, 0, -PIVOT_DROP, PIVOT_HOLE / 2)]
    # curved lock slot: lock point sits at angle 180 deg (toward the wall) when level
    steps = 24
    pts = []
    for i in range(steps + 1):
        a = math.radians(180 + TILT_MIN + (TILT_MAX - TILT_MIN) * i / steps)
        pts.append(cyl_x(x0 - 1, EAR_T + 2, LOCK_R * math.cos(a), -PIVOT_DROP + LOCK_R * math.sin(a), PIVOT_HOLE / 2))
    for p, q in zip(pts, pts[1:]):
        cuts.append(M.batch_hull([p, q]))
    return e - union(cuts)

def tilt_yoke():
    """Yoke frame: x centred on the pod, y = 0 at the pivot, z = 0 at box underside."""
    plate = box(-YOKE_W / 2, -YOKE_PLATE_Y / 2, -YOKE_PLATE_T, YOKE_W, YOKE_PLATE_Y, YOKE_PLATE_T)
    y = union([plate, ear(-YOKE_W / 2), ear(EAR_GAP / 2)])
    holes = []
    for sx, sy in YOKE_SCREWS:
        holes.append(cyl_z(-YOKE_PLATE_T - 1, YOKE_PLATE_T + 2, sx - BOX_W / 2, sy - PIVOT_Y, 4.5 / 2))
    return y - union(holes)

# ---------------------------------------------------------------- pod
POD_H = POD_WALL + POD_IN_H
PIV_Z = POD_H / 2 + 1.5      # pivot height on the pod (pod frame, z = 0 at pod base)

def radar_pod():
    """Pod frame: x, y centred, z = 0 at the lens face. Printed lens-face down."""
    h = POD_OUT / 2
    p = box(-h, -h, 0, POD_OUT, POD_OUT, POD_H)
    p = p - box(-POD_IN / 2, -POD_IN / 2, POD_WALL, POD_IN, POD_IN, POD_H)
    adds = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            adds.append(box(sx * POD_IN / 2 - (POD_POST if sx > 0 else 0), sy * POD_IN / 2 - (POD_POST if sy > 0 else 0),
                            POD_WALL, POD_POST, POD_POST, POD_IN_H))
    # pivot and lock bosses, buttressed down to the print bed (no overhang)
    for side in (-1, 1):
        x0 = h if side > 0 else -h - BOSS_OUT
        for (by, br) in ((0.0, BOSS_R), (-LOCK_R, 7.0)):
            c = cyl_x(x0, BOSS_OUT, by, PIV_Z, br)
            foot = box(x0, by - br, 0, BOSS_OUT, 2 * br, 1)
            adds.append(M.batch_hull([c, foot]))
    p = union([p] + adds)
    cuts = [cyl_z(-1, POD_WALL + 2, 0, 0, (LENS_D + 0.6) / 2)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            cuts.append(cyl_z(POD_H - 10, 11, sx * (POD_IN / 2 - POD_POST / 2), sy * (POD_IN / 2 - POD_POST / 2), POD_SCREW_PILOT / 2))
    for side in (-1, 1):
        face = h + BOSS_OUT
        for by in (0.0, -LOCK_R):
            if side > 0:
                cuts.append(cyl_x(face - INSERT_DEPTH, INSERT_DEPTH + 1, by, PIV_Z, INSERT_HOLE / 2))
            else:
                cuts.append(cyl_x(-face - 1, INSERT_DEPTH + 1, by, PIV_Z, INSERT_HOLE / 2))
    return p - union(cuts)

def radar_pod_lid():
    t = 3.0
    lid = box(-POD_OUT / 2, -POD_OUT / 2, 0, POD_OUT, POD_OUT, t)
    c = 0.4
    a = POD_IN / 2 - c
    ring = box(-a, -a, t, 2 * a, 2 * a, 4) - box(-a + 1.6, -a + 1.6, t - 1, 2 * (a - 1.6), 2 * (a - 1.6), 6)
    notch = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * (POD_IN / 2 - POD_POST / 2), sy * (POD_IN / 2 - POD_POST / 2)
            notch.append(box(cx - POD_POST / 2 - c, cy - POD_POST / 2 - c, t - 1, POD_POST + 2 * c, POD_POST + 2 * c, 6))
    lid = lid + (ring - union(notch))
    holes = [cyl_z(-1, t + 6, 0, 0, POD_GLAND_HOLE / 2)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            holes.append(cyl_z(-1, t + 2, sx * (POD_IN / 2 - POD_POST / 2), sy * (POD_IN / 2 - POD_POST / 2), 3.4 / 2))
    return lid - union(holes)

# ---------------------------------------------------------------- output
def to_trimesh(man):
    mesh = man.to_mesh()
    return trimesh.Trimesh(vertices=np.array(mesh.vert_properties)[:, :3], faces=np.array(mesh.tri_verts), process=True)

def assembly(tilt=PREVIEW_TILT):
    """Everything placed in wall coordinates, pod tilted (positive = lens swings away from the wall)."""
    parts = {}
    parts["controller_box"] = controller_box()
    parts["controller_lid"] = controller_lid().rotate([90, 0, 0]).translate([0, BOX_D + 3, 0])
    parts["tilt_yoke"] = tilt_yoke().translate([BOX_W / 2, PIVOT_Y, 0])
    pod = radar_pod() + radar_pod_lid().rotate([180, 0, 0]).translate([0, 0, POD_H + 3])
    # move the pod so its pivot is at the origin, tilt, then place under the box
    pod = pod.translate([0, 0, -PIV_Z]).rotate([tilt, 0, 0]).translate([BOX_W / 2, PIVOT_Y, -PIVOT_DROP])
    parts["radar_pod"] = pod
    return parts

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
    os.makedirs(out, exist_ok=True)
    printable = {
        "controller_box": controller_box(),
        "controller_lid": controller_lid(),
        "tilt_yoke": tilt_yoke().rotate([180, 0, 0]),       # plate on the bed, ears up
        "radar_pod": radar_pod(),                            # lens face on the bed
        "radar_pod_lid": radar_pod_lid(),                    # outside face on the bed
    }
    # box prints with its back (wall side) on the bed
    printable["controller_box"] = printable["controller_box"].rotate([90, 0, 0])
    for name, part in printable.items():
        tm = to_trimesh(part)
        tm.apply_translation(-tm.bounds[0])                 # sit on the bed at the origin
        tm.export(os.path.join(out, name + ".stl"))
        print(f"{name:16s} {tm.extents.round(1)} mm  watertight={tm.is_watertight}  vol={tm.volume/1000:.0f} cm3")
