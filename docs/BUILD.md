# Build instructions

Work through these in order. Don't connect the 12V plugpack until step 5 says so.

## Tools

- Soldering iron (temperature-controlled, about 330°C), stand, and 0.8 mm 60/40 rosin-core solder
- Multimeter
- Drill with a 12.5 mm bit (for the PG7 glands) and a 3 mm bit (for the drain hole)
- Small screwdrivers, side cutters, wire strippers, heatshrink and a lighter or heat gun
- Saw for the 45° timber wedge

## 1. Prepare the modules

1. **Buck converter:** check that the 5V output pad is the one bridged (it is from the factory). Solder 4 male header pins into its IN+, IN−, OUT+ and OUT− holes, pointing down.
2. **MOSFET (HW-517):** solder 2 male header pins into its PWM and GND holes, pointing down.
3. **ESP32:** leave as is. It plugs into female sockets.

## 2. Build the perfboard

Follow [`wiring/one-board-layout.png`](../wiring/one-board-layout.png). The top half shows the parts side and the bottom half shows the solder side (flipped left to right).

1. **ESP32 sockets:** cut two 15-pin strips from the 1x20 female header. Plug them onto the ESP32, sit the ESP32 on the board at columns 10 and 20, rows C to Q, and solder the sockets. Then unplug the ESP32. Doing it this way means the spacing always matches.
2. **Buck sockets:** cut two 2-pin female strips. Plug them onto the buck's pins, place the buck at the left of the board, and solder the sockets.
3. **MOSFET socket:** cut one 2-pin female strip. Plug it onto the MOSFET's PWM/GND pins and solder it at columns 24–25, row N.
4. **Screw terminals:** solder a 2-pin 5 mm terminal for 12V IN at the top left. Clip two 2-pin terminals together into a 4-way and solder it along the bottom edge for the radar.
5. **Buses:** on the underside, run bare wire along row S for the 5V bus and along column 1 and row U for the GND bus. Keep them apart.
6. **Wires:** solder each coloured wire as shown. Where a wire meets a pin, push it through the hole next to the pin and join the two with solder underneath.
7. Inspect the underside for solder bridges, especially between the 5V and GND buses.

## 3. Check the board before plugging anything in

With nothing plugged into the sockets:

1. Set the multimeter to continuity (beep).
2. Probe the 5V bus and the GND bus. **It must not beep.** If it does, find the bridge.
3. Probe 12V IN + and GND. It must not beep.

## 4. Prepare the boxes

See [`mounting/main-box-inside.png`](../mounting/main-box-inside.png) and [`mounting/mounting.png`](../mounting/mounting.png).

**Main box (HB6128):**
1. Drill two 12.5 mm holes in the **bottom** wall and fit the PG7 glands. One is for 12V, one for the radar cable.
2. Drill the holes for the valve's pipes through the side walls, at valve height. Seal them with sealed fittings or a bead of neutral-cure silicone.
3. Drill a 3 mm drain hole at the lowest corner.
4. Fit 4 × M3 standoffs (8 mm) for the perfboard near the top. Mount the valve along the bottom with P-clips or cable-tie mounts.

**Radar box (HB6127):**
1. Drill one 12.5 mm hole in a side or the bottom and fit a PG7 gland for the 4-core cable.
2. Mount the radar inside so its lens sits flat against the inside of the **lid**. There's no hole for the lens, because the radar reads through the plastic.

## 5. Wire it up and power on

1. **Valve:** connect MOSFET OUT+ to valve terminal A and OUT− to terminal B. Solder the 1N4001 diode across A and B with the **stripe on A** (the OUT+ side). A diode fitted backwards shorts the 12V.
2. **Radar cable:** connect 5V, GND, RX and TX at the radar box end to the matching screws on the board's radar terminal.
3. **Power lead:** cut the plugpack's DC lead about 10 cm from the plug. Feed the long end in through the 12V gland. Rejoin the wires stripe to stripe, solder them, and heatshrink each one. Plug the barrel into the barrel-to-screw adapter, then run the adapter to 12V IN on the board. Use the multimeter to confirm + is on +.
4. With the ESP32, buck and MOSFET **unplugged**, switch on the 12V. Measure about 12V across 12V IN. Switch off.
5. Plug in the buck only. Switch on and measure **5V** between the 5V bus and the GND bus. Switch off.
6. Plug in the ESP32 and MOSFET and switch on. The ESP32's red power LED should light.

## 6. Flash the firmware

Follow [`docs/ESPHOME.md`](ESPHOME.md).

## 7. Mount and set the angle

1. Screw the main box to the wall through the holes in its base. These sit under the lid screws, outside the seal.
2. Cut a 45° wedge from scrap timber and screw it to the wall under the main box. Leave about 110 mm below the box.
3. Screw or cable-tie the radar box's flange to the sloped face, with the lid facing the pool.
4. Lay your phone on the lid and use a level app to confirm 45°.
5. Give both cables a drip loop: the cable should dip below the gland before it rises.
6. Fix the outlet pipe so it sprays into the pool from about 1 m up and can never fall into the water. That air gap is the backflow protection.

## 8. Test

1. In Home Assistant, check that **Distance** gives a sensible, steady reading.
2. Turn on **Fill Valve** manually and confirm water flows. Turn it off again.
3. Set the fill levels as described in [`docs/ESPHOME.md`](ESPHOME.md), then turn on **Auto Top-Up**.
4. Watch the first automatic fill from start to finish.
