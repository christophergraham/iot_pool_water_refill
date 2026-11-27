# Parts and tools

Codes are the shop's own product codes. **Core** = Core Electronics, **Jaycar** = Jaycar Electronics, **Bunnings** = any Bunnings.

Prices are in **AUD including GST**. Prices in **bold** were checked on the shop's site in November 2026. The rest are typical prices (marked ~), so expect them to vary a little. Postage isn't included.

## Cost summary

| Section | Cost (AUD) |
|---|---|
| Electronics | $243.21 |
| Boxes and mounting | $72.45 |
| Plumbing | $52.00 |
| Consumables | $42.00 |
| **Total parts** | **$409.66** |
| Tools, if you don't already own them | $146.00 |
| **Total with tools** | **$555.66** |

If you already have a garden hose, take about $30 off.

## Electronics

| Qty | Part | Where / code | Notes | Price |
|---|---|---|---|---|
| 1 | ESP32 DevKit (ESP-WROOM-32, 30-pin) | Core / Jaycar | Runs ESPHome | ~$15.00 |
| 1 | DFRobot 80 GHz radar level sensor | Core **SEN0676** | UART Modbus, 5V | **$114.51** |
| 1 | 12V solenoid valve, 3/4" BSP, normally closed | Core **ROB-10456** | 330 mA coil | **$22.55** |
| 1 | Dual MOSFET switch module (HW-517) | Core **CE09733** | Switches the valve | **$1.35** |
| 1 | DC-DC buck converter, 5V output | Core **DFR1015** | Uses the factory 5V pad | **$9.95** |
| 1 | 1N4001 diode (spare in the pack is handy) | Core | Across the valve coil | ~$1.00 |
| 1 | 12V 2A plugpack | Core **AM8936** | The only power supply | **$26.35** |
| 1 | DC barrel to screw terminal adapter | Core **CE08698** | Inside the box | ~$3.00 |
| 1 | Perfboard, about 7 × 9 cm | Core / Jaycar | | ~$5.00 |
| 3 | Female header strip, 1 × 20 | Core **CE07759** | Sockets for the ESP32, buck and MOSFET | ~$4.50 |
| 1 | Male header strip, 1 × 40 | Core **CE07828** | Pins for the buck and MOSFET | ~$1.00 |
| 3 | 2-pin 5 mm screw terminal (interlocking) | Core **CE08311** | 1 for 12V in, 2 clipped together for the radar | ~$3.00 |
| 1 | Hook-up wire kit (red, black, green, blue, purple/any) | Core **CE09603** | Silicone wire is easiest | ~$20.00 |
| 1 | Bare tinned copper wire, about 0.6 mm | Jaycar | For the buses (or strip a solid-core wire) | ~$6.00 |
| 2–5 m | 4-core cable (alarm/security cable is fine) | Jaycar / Bunnings | Radar box to main box | ~$10.00 |
| | **Electronics subtotal** | | | **$243.21** |

## Boxes and mounting

| Qty | Part | Where / code | Notes | Price |
|---|---|---|---|---|
| 1 | Sealed ABS enclosure 171 × 121 × 55, dark grey | Jaycar **HB6128** | Board and valve coil | **$22.95** |
| 1 | Enclosure with mounting flange 115 × 90 × 55, dark grey | Jaycar **HB6127** | Radar | **$18.50** |
| 1 pack | PG7 cable glands (need 3) | Core **FIT0728** | Two on the main box, one on the radar box | ~$6.00 |
| 4 | M3 × 8 mm nylon or brass standoffs + M3 screws | Jaycar | Hold the perfboard | ~$6.00 |
| 2 | P-clips to suit the valve body + stainless screws | Bunnings | Clamp the valve upright to the outside of the box | ~$6.00 |
| 1 | Offcut of 90 × 45 timber, about 150 mm | Bunnings / shed | The 45° wedge | $0 (offcut) |
| 1 | Outdoor double-sided mounting tape (3M or similar) | Bunnings | Holds the MOSFET flat on the board | ~$5.00 |
| 6 | Exterior screws + wall plugs to suit your wall | Bunnings | 4 for the main box, 2 for the wedge | ~$8.00 |
| | **Boxes and mounting subtotal** | | | **$72.45** |

## Plumbing

The valve body is outside the box, so no fittings go through the box. Check the thread on your valve before buying. The ROB-10456 is 3/4" BSP.

| Qty | Part | Where | Notes | Price |
|---|---|---|---|---|
| 1 | 3/4" BSP to garden-hose tap adaptor or hose tail | Bunnings | Inlet, on the bottom of the valve | ~$8.00 |
| 1 | 3/4" BSP hose tail | Bunnings | Outlet, on the top of the valve | ~$6.00 |
| 1 | 90° hose elbow | Bunnings | At the top of the riser, turns the hose out from the wall | ~$5.00 |
| — | Garden hose or 13 mm poly pipe + clamps/saddles | Bunnings | Tap → valve, and valve → outlet | ~$30.00 |
| 1 | Thread tape | Bunnings | All threaded joints | ~$3.00 |
| | **Plumbing subtotal** | | | **$52.00** |

## Consumables

| Part | Notes | Price |
|---|---|---|
| 60/40 tin-lead rosin-core solder, 0.8 mm | Much easier than lead-free | ~$15.00 |
| Heatshrink tubing, assorted | Valve joints and the rejoined power lead | ~$10.00 |
| Neutral-cure silicone (outdoor) | Seal the coil cut-out. Neutral-cure won't corrode the electronics | ~$12.00 |
| Cable ties | Tidy cables, hold the radar box to the wedge if needed | ~$5.00 |
| **Consumables subtotal** | | **$42.00** |

## Tools

| Tool | Why | Price |
|---|---|---|
| Temperature-controlled soldering iron (about 330°C) with stand | All the board work | ~$60.00 |
| Multimeter | Polarity, 12V and 5V checks, and checking for shorts (continuity beep) | already owned |
| Side cutters and wire strippers | Cutting header strips and wire | ~$25.00 |
| Helping hands or a small vice | Holds the board while soldering (optional, but it helps) | ~$20.00 |
| Drill, 3 mm bit, step drill (to 13 mm) and a small file | Drain and gland holes, coil cut-out | ~$25.00 (step drill) |
| Saw and mitre box | Cutting the 45° wedge | already owned |
| Screwdrivers (small flat for terminals, Phillips) | Terminals and mounting | already owned |
| Heat gun or lighter | Heatshrink | already owned |
| Phone with a level app | Setting 45° | already owned |
| Safety glasses | Drilling and soldering | ~$8.00 |
| USB data cable for the ESP32 | First firmware install | ~$8.00 |
| **Tools subtotal** (items you don't own) | | **$146.00** |
