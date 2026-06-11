
import os, sys, glob

def find_sym_dir():
    candidates = [
        "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols",
        "/Applications/KiCad/kicad.app/Contents/SharedSupport/symbols",
        "/usr/local/share/kicad/symbols",
        "/opt/homebrew/share/kicad/symbols",
        "/usr/share/kicad/symbols",
    ]
    candidates += glob.glob("/Applications/KiCad*/KiCad.app/Contents/SharedSupport/symbols")
    for p in candidates:
        if os.path.isfile(os.path.join(p, "Device.kicad_sym")):
            return p
    return None

sym_dir = find_sym_dir()
if not sym_dir:
    sys.exit("ERROR: KiCad symbol libraries not found.\n"
             "Run: find /Applications -name Device.kicad_sym")

print(f"Symbols : {sym_dir}")
for v in ("KICAD_SYMBOL_DIR","KICAD6_SYMBOL_DIR","KICAD7_SYMBOL_DIR",
          "KICAD8_SYMBOL_DIR","KICAD9_SYMBOL_DIR"):
    os.environ[v] = sym_dir

for fp in [
    os.path.expanduser("~/Library/Preferences/kicad/9.0/fp-lib-table"),
    os.path.expanduser("~/Library/Preferences/kicad/8.0/fp-lib-table"),
    os.path.expanduser("~/Library/Preferences/kicad/fp-lib-table"),
    os.path.expanduser("~/.config/kicad/9.0/fp-lib-table"),
    os.path.expanduser("~/.config/kicad/fp-lib-table"),
]:
    if os.path.isfile(fp):
        os.environ["KICAD_FP_LIB_TABLE"] = fp
        print(f"fp-lib  : {fp}")
        break

from skidl import *
from skidl import SKIDL  # explicit import so Pylance resolves it

# ────────────────────────────────────────────────────────────
#  POWER RAILS
# ────────────────────────────────────────────────────────────
vcc = Net('+5V');  vcc.drive = POWER
gnd = Net('GND');  gnd.drive = POWER

# ────────────────────────────────────────────────────────────
#  PARTS
# ────────────────────────────────────────────────────────────

U1 = Part('MCU_Microchip_ATtiny', 'ATtiny814-SS',
          footprint='Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',
          tool=SKIDL, tag='U1')
U1.ref = 'U1'

J1 = Part('Connector_Generic', 'Conn_01x09',
          footprint='Connector_Dsub:DSUB-9_Pins_EdgeMount_P2.77mm',
          tool=SKIDL, tag='J1')
J1.ref = 'J1'

J2 = Part('Connector_Generic', 'Conn_01x06',
          footprint='Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Horizontal',
          tool=SKIDL, tag='J2')
J2.ref = 'J2'

# ── Resistors ────────────────────────────────────────────────
def R(val, ref):
    r = Part('Device', 'R', value=val,
             footprint='Resistor_SMD:R_0402_1005Metric',
             tool=SKIDL, tag=ref)
    r.ref = ref
    return r

# POT divider upper legs
R1 = R('1K',  'R1')   # OUT_BTN3 → POTX
R2 = R('1K',  'R2')   # OUT_BTN2 → POTY

# LED + FIRE
R3 = R('330', 'R3')   # LED series
R4 = R('1K',  'R4')   # FIRE pull-down

# POT divider lower legs (pot body symbols in schematic)
R5 = R('10K', 'R5')   # POTX → GND  (potentiometer body)
R6 = R('10K', 'R6')   # POTY → GND  (potentiometer body)

# Directional 0Ω pull-down resistors — pin[1]=GND, pin[2]=switch input
R7  = R('0', 'R7')    # GND → JUMP1 switch input → UP
R8  = R('0', 'R8')    # GND → UP1   switch input → UP
R9  = R('0', 'R9')    # GND → DOWN1 switch input → DOWN
R10 = R('0', 'R10')   # GND → LEFT1 switch input → LEFT
R11 = R('0', 'R11')   # GND → RIGHT1 switch input → RIGHT

# ── LED & cap ────────────────────────────────────────────────
D1 = Part('Device', 'LED', value='RAPID',
          footprint='LED_SMD:LED_0402_1005Metric',
          tool=SKIDL, tag='D1')
D1.ref = 'D1'

C1 = Part('Device', 'C', value='0.1uF',
          footprint='Capacitor_SMD:C_0402_1005Metric',
          tool=SKIDL, tag='C1')
C1.ref = 'C1'

# ── Buttons ──────────────────────────────────────────────────
def BTN(ref):
    b = Part('Switch', 'SW_Push',
             footprint='RetroPad:Silicone_Membrane_Pad_11mm_(7.5mm)',
             tool=SKIDL, tag=ref)
    b.ref = ref
    return b

# Action buttons (left side of schematic) → MCU PB0–PB3
RAPID1 = BTN('RAPID1')
BTN1   = BTN('BTN1')
BTN2   = BTN('BTN2')
BTN3   = BTN('BTN3')

# Directional buttons (bottom-right of schematic)
JUMP1  = BTN('JUMP1')
UP1    = BTN('UP1')
DOWN1  = BTN('DOWN1')
LEFT1  = BTN('LEFT1')
RIGHT1 = BTN('RIGHT1')

# ── Mounting holes ───────────────────────────────────────────
def HOLE(ref):
    h = Part('Mechanical', 'MountingHole_Pad',
             footprint='MountingHole:MountingHole_3.2mm_M3',
             tool=SKIDL, tag=ref)
    h.ref = ref
    return h

H1 = HOLE('H1')
H2 = HOLE('H2')

# ────────────────────────────────────────────────────────────
#  NETS
# ────────────────────────────────────────────────────────────
rapid_net = Net('RAPID')
btn1_net  = Net('BTN1')
btn2_net  = Net('BTN2')
btn3_net  = Net('BTN3')
out_btn3  = Net('OUT_BTN3')
out_btn2  = Net('OUT_BTN2')
fire_net  = Net('FIRE')
rapid_led = Net('RAPID_LED')
led_k     = Net('LED_K')
reset_net = Net('RESET')
potx_net  = Net('POTX')
poty_net  = Net('POTY')
up_net    = Net('UP')
down_net  = Net('DOWN')
left_net  = Net('LEFT')
right_net = Net('RIGHT')

# Intermediate nets between 0Ω resistor pin[2] and switch pin[1]
jump1_in  = Net('JUMP1_IN')
up1_in    = Net('UP1_IN')
down1_in  = Net('DOWN1_IN')
left1_in  = Net('LEFT1_IN')
right1_in = Net('RIGHT1_IN')

# ────────────────────────────────────────────────────────────
#  CONNECTIONS
# ────────────────────────────────────────────────────────────

# ── Power + decoupling ───────────────────────────────────────
U1['VCC'] += vcc;  U1['GND'] += gnd
C1[1]     += vcc;  C1[2]     += gnd

# ── Action buttons → PB0–PB3 ─────────────────────────────────
RAPID1[1] += rapid_net;  RAPID1[2] += gnd;  U1['PB0'] += rapid_net
BTN1[1]   += btn1_net;   BTN1[2]   += gnd;  U1['PB1'] += btn1_net
BTN2[1]   += btn2_net;   BTN2[2]   += gnd;  U1['PB2'] += btn2_net
BTN3[1]   += btn3_net;   BTN3[2]   += gnd;  U1['PB3'] += btn3_net

# ── MCU outputs ──────────────────────────────────────────────
U1['PA5'] += out_btn3
U1['PA6'] += out_btn2
U1['PA7'] += fire_net

# ── POT voltage dividers ─────────────────────────────────────
# OUT_BTN3 ──R1(1K)──► POTX ──R5(10K pot body)──► GND
# OUT_BTN2 ──R2(1K)──► POTY ──R6(10K pot body)──► GND
R1[1] += out_btn3;  R1[2] += potx_net
R5[1] += potx_net;  R5[2] += gnd

R2[1] += out_btn2;  R2[2] += poty_net
R6[1] += poty_net;  R6[2] += gnd

# ── LED chain: PA4 → D1(A→K) → R3(330Ω) → GND ──────────────
U1['PA4'] += rapid_led
D1['A']   += rapid_led
D1['K']   += led_k
R3[1]     += led_k;  R3[2] += gnd

# ── FIRE: PA7 → fire_net; R4(1K) pull-down → GND ────────────
R4[1] += fire_net;  R4[2] += gnd

# ── UPDI header J2 ───────────────────────────────────────────
# Pin1=GND  Pin2=VCC  Pin3=RESET(UPDI)  Pin4–6=GND
U1['~{RESET}/PA0'] += reset_net
J2[1] += gnd;  J2[2] += vcc;  J2[3] += reset_net
J2[4] += gnd;  J2[5] += gnd;  J2[6] += gnd

# Unused MCU pins
U1['PA1'] += NC
U1['PA2'] += NC
U1['PA3'] += NC

# ── Directional network ──────────────────────────────────────
# GND ── R7(0Ω)  ── JUMP1_IN ── JUMP1 ── UP
# GND ── R8(0Ω)  ── UP1_IN   ── UP1   ── UP
# GND ── R9(0Ω)  ── DOWN1_IN ── DOWN1 ── DOWN
# GND ── R10(0Ω) ── LEFT1_IN ── LEFT1 ── LEFT
# GND ── R11(0Ω) ── RIGHT1_IN── RIGHT1── RIGHT

R7[1]     += gnd;       R7[2]     += jump1_in
JUMP1[1]  += jump1_in;  JUMP1[2]  += up_net

R8[1]     += gnd;       R8[2]     += up1_in
UP1[1]    += up1_in;    UP1[2]    += up_net

R9[1]     += gnd;       R9[2]     += down1_in
DOWN1[1]  += down1_in;  DOWN1[2]  += down_net

R10[1]    += gnd;       R10[2]    += left1_in
LEFT1[1]  += left1_in;  LEFT1[2]  += left_net

R11[1]    += gnd;       R11[2]    += right1_in
RIGHT1[1] += right1_in; RIGHT1[2] += right_net

# ── DB9 — Atari/Commodore joystick pinout ────────────────────
# 1=UP  2=DOWN  3=LEFT  4=RIGHT  5=POTY  6=FIRE  7=+5V  8=GND  9=POTX
J1['1'] += up_net;    J1['2'] += down_net
J1['3'] += left_net;  J1['4'] += right_net
J1['5'] += poty_net;  J1['6'] += fire_net
J1['7'] += vcc;       J1['8'] += gnd
J1['9'] += potx_net

# ── Mounting holes ───────────────────────────────────────────
H1[1] += gnd;  H2[1] += gnd

# ────────────────────────────────────────────────────────────
#  ERC + OUTPUT
# ────────────────────────────────────────────────────────────
print("\nRunning ERC...")
ERC()
print("Generating netlist...")
generate_netlist(file_='retropad.net')
print("\nDone!  Import retropad.net via KiCad > Tools > Import Netlist")