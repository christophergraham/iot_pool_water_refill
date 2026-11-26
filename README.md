# IoT pool water refill

An automatic pool top-up controller. An 80 GHz radar measures the distance to the water. When the level drops, an ESP32 running ESPHome opens a 12V solenoid valve until the pool is back up. Everything is visible and adjustable in Home Assistant.

![Board layout](wiring/one-board-layout.png)

## How it works

- The radar is mounted above the pool, tilted at 45°, and reports the distance to the water every 10 seconds over Modbus-RTU.
- Readings are median-filtered to ignore splashes and ripples.
- When the distance stays above **Start Fill Above** for 2 minutes, the valve opens.
- The valve closes when the distance drops below **Stop Fill Below**.
- Safety:
  - The valve is forced closed after **Max Fill Time** (default 60 min) and the system locks out until you press **Reset Fill Lockout** in Home Assistant.
  - The valve closes if the radar stops reporting for 60 seconds.
  - There is a 30-minute rest between fills.
  - The valve always starts closed after a power cut.
- The outlet sprays from about 1 m above the pool. That air gap is the backflow protection, so the outlet must never be able to end up in the water.

## Parts

| Part | Notes |
|---|---|
| ESP32 DevKit (WROOM-32, 30-pin) | runs ESPHome |
| DFRobot SEN0676 80 GHz radar level sensor | UART Modbus-RTU, 115200 8N1, address 0x01, 3.5–5V |
| 12V solenoid valve, 3/4" BSP, normally closed (SparkFun ROB-10456) | 330 mA coil |
| HW-517 dual MOSFET module | low-side switch for the valve |
| DFRobot DFR1015 buck converter | 12V → 5V (factory 5V pad) |
| 1N4001 diode | across the valve coil |
| 12V 2A plugpack + barrel-to-screw adapter | the only power input |
| 7 × 9 cm perfboard | |
| 3 × 1x20 female header, 1 × 1x40 male header | so every module plugs in and can be removed |
| 3 × 2-pin 5 mm screw terminals | 12V in, plus two clipped together for the radar |
| PG7 cable glands | power and radar cables |
| Jaycar HB6128 sealed ABS box, 171 × 121 × 55 | board and valve |
| Jaycar HB6127 flanged box, 115 × 90 × 55 | radar, which reads through the lid; no lens hole |

## Wiring

See [`wiring/one-board-layout.png`](wiring/one-board-layout.png) for the top view and the solder side. In summary:

| From | To |
|---|---|
| 12V + | buck IN+, MOSFET VIN+ |
| 12V − | GND bus, buck IN−, MOSFET VIN− |
| Buck OUT+ (5V) | 5V bus → ESP32 VIN, radar 5V |
| Buck OUT− | GND bus |
| ESP32 GPIO16 (RX2) | radar TX |
| ESP32 GPIO17 (TX2) | radar RX |
| ESP32 GPIO23 (D23) | MOSFET PWM |
| MOSFET OUT+ / OUT− | valve terminals A / B |
| 1N4001 | across the valve, stripe on A (OUT+ side) |

12V only goes to the buck and the MOSFET, never to the ESP32. A diode fitted backwards shorts the 12V, so check the stripe before powering up.

Power-up order: confirm the buck's 5V pad is bridged and measure 5V on its output, then plug in the ESP32 and the radar.

## Firmware

1. Copy [`esphome/pool-level.yaml`](esphome/pool-level.yaml) into your ESPHome folder.
2. Copy `esphome/secrets.yaml.example` to `secrets.yaml` and fill in your WiFi details.
3. Flash it, then adopt the device in Home Assistant.
4. Set **Start Fill Above** and **Stop Fill Below** from the **Distance** reading, then turn on **Auto Top-Up**.

## Enclosure and mounting

- The main box goes on a wall, with the valve at the bottom and the board above it. The pipes and cables come in through the bottom wall, and there is a small drain hole at the lowest corner.
- Power comes in through a PG7 gland. Cut the DC lead about 10 cm from the plug, feed it through the gland, and rejoin it stripe to stripe so the polarity stays the same. The plugpack itself must be plugged in under cover or into a weatherproof outlet.
- The radar box hangs about 110 mm below the main box on a tilt bracket set to 45°. Check the angle with a phone level app. A 45° timber wedge is enough for testing.
- Before sealing the radar box, bench-test that the reading through the lid matches a tape measure.

## Legacy

`legacy/` holds earlier versions: a 3D-printable enclosure (manifold3d model and STLs), the first Arduino sketch, and the earlier wiring drawings. They're kept for reference only. The current build uses the Jaycar boxes and ESPHome.
