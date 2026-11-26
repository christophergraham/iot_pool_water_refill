# Parts and tools

Codes are the shop's own product codes. **Core** = Core Electronics, **Jaycar** = Jaycar Electronics, **Bunnings** = any Bunnings.

## Electronics

| Qty | Part | Where / code | Notes |
|---|---|---|---|
| 1 | ESP32 DevKit (ESP-WROOM-32, 30-pin) | Core / Jaycar | Runs ESPHome |
| 1 | DFRobot 80 GHz radar level sensor | Core **SEN0676** | UART Modbus, 5V |
| 1 | 12V solenoid valve, 3/4" BSP, normally closed | Core **ROB-10456** | 330 mA coil |
| 1 | Dual MOSFET switch module (HW-517) | Core **CE09733** | Switches the valve |
| 1 | DC-DC buck converter, 5V output | Core **DFR1015** | Uses the factory 5V pad |
| 1 | 1N4001 diode (spare in the pack is handy) | Core | Across the valve coil |
| 1 | 12V 2A plugpack | Core **AM8936** | The only power supply |
| 1 | DC barrel to screw terminal adapter | Core **CE08698** | Inside the box |
| 1 | Perfboard, about 7 × 9 cm | Core / Jaycar | |
| 3 | Female header strip, 1 × 20 | Core **CE07759** | Sockets for the ESP32, buck and MOSFET |
| 1 | Male header strip, 1 × 40 | Core **CE07828** | Pins for the buck and MOSFET |
| 3 | 2-pin 5 mm screw terminal (interlocking) | Core **CE08311** | 1 for 12V in, 2 clipped together for the radar |
| 1 | Hook-up wire kit (red, black, green, blue, purple/any) | Core **CE09603** | Silicone wire is easiest |
| 1 | Bare tinned copper wire, about 0.6 mm | Jaycar | For the buses (or strip a solid-core wire) |
| 2–5 m | 4-core cable (alarm/security cable is fine) | Jaycar / Bunnings | Radar box to main box |

## Boxes and mounting

| Qty | Part | Where / code | Notes |
|---|---|---|---|
| 1 | Sealed ABS enclosure 171 × 121 × 55, dark grey | Jaycar **HB6128** | Board and valve (about $23) |
| 1 | Enclosure with mounting flange 115 × 90 × 55, dark grey | Jaycar **HB6127** | Radar (about $19) |
| 1 pack | PG7 cable glands (need 3) | Core **FIT0728** | Two on the main box, one on the radar box |
| 4 | M3 × 8 mm nylon or brass standoffs + M3 screws | Jaycar | Hold the perfboard |
| 2 | P-clips to suit the valve body + stainless screws | Bunnings | Clamp the valve upright to the outside of the box |
| 1 | Offcut of 90 × 45 timber, about 150 mm | Bunnings / shed | The 45° wedge |
| 1 | Velcro or double-sided foam pad | Bunnings | Under the MOSFET's free end |
| 6 | Exterior screws + wall plugs to suit your wall | Bunnings | 4 for the main box, 2 for the wedge |

## Plumbing

The valve body is outside the box, so no fittings go through the box. Check the thread on your valve before buying. The ROB-10456 is 3/4" BSP.

| Qty | Part | Where | Notes |
|---|---|---|---|
| 1 | 3/4" BSP to garden-hose tap adaptor or hose tail | Bunnings | Inlet, on the bottom of the valve |
| 1 | 3/4" BSP hose tail | Bunnings | Outlet, on the top of the valve |
| 1 | 90° hose elbow | Bunnings | At the top of the riser, turns the hose out from the wall |
| — | Garden hose or 13 mm poly pipe + clamps/saddles | Bunnings | Tap → valve, and valve → outlet |
| 1 | Thread tape | Bunnings | All threaded joints |

## Consumables

| Part | Notes |
|---|---|
| 60/40 tin-lead rosin-core solder, 0.8 mm | Much easier than lead-free |
| Heatshrink tubing, assorted | Valve joints and the rejoined power lead |
| Neutral-cure silicone (outdoor) | Seal the coil cut-out. Neutral-cure won't corrode the electronics |
| Cable ties | Tidy cables, hold the radar box to the wedge if needed |

## Tools

| Tool | Why |
|---|---|
| Temperature-controlled soldering iron (about 330°C) with stand | All the board work |
| Multimeter | Polarity, 12V and 5V checks, and checking for shorts (continuity beep) |
| Side cutters and wire strippers | Cutting header strips and wire |
| Helping hands or a small vice | Holds the board while soldering (optional, but it helps) |
| Drill, 3 mm bit, step drill (to 13 mm) and a small file | Drain and gland holes, coil cut-out |
| Saw and mitre box | Cutting the 45° wedge |
| Screwdrivers (small flat for terminals, Phillips) | Terminals and mounting |
| Heat gun or lighter | Heatshrink |
| Phone with a level app | Setting 45° |
| Safety glasses | Drilling and soldering |
| USB data cable for the ESP32 | First firmware install |
