# Adding it to Home Assistant with ESPHome

## 1. Install the ESPHome add-on

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store**.
2. Search for **ESPHome Device Builder**, open it and press **Install**.
3. Press **Start**, turn on **Show in sidebar**, then open **ESPHome** from the sidebar.

## 2. Add your WiFi details

1. In ESPHome, press **Secrets** (top right).
2. Make sure it contains your WiFi name and password:

   ```yaml
   wifi_ssid: "your-wifi-name"
   wifi_password: "your-wifi-password"
   ```

3. Press **Save**.

## 3. Create the device

1. Press **+ New Device**, then **Continue**.
2. Name it `pool-level` and press **Next**.
3. Choose **ESP32**. If it shows an encryption key, you can skip it.
4. On the new **pool-level** card, press **Edit**.
5. Delete everything in the editor and paste in the whole of [`esphome/pool-level.yaml`](../esphome/pool-level.yaml).
6. Press **Save**.

## 4. First install (over USB)

The first install has to go over a USB cable. After that, updates go over WiFi.

1. Plug the ESP32 into the computer you're using Home Assistant on, with a USB data cable rather than a charge-only one.
2. On the **pool-level** card, press **⋮ → Install → Plug into this computer**. This needs Chrome or Edge.
3. Pick the ESP32's port and wait for it to compile and upload. The first compile takes a few minutes.

If **Plug into this computer** isn't offered, choose **Manual download**, save the file, then go to https://web.esphome.io in Chrome, press **Connect**, pick the port and choose **Install**.

Unplug the ESP32 from the computer and put it back on the perfboard.

## 5. Add it to Home Assistant

1. Power the board from the 12V plugpack.
2. Go to **Settings → Devices & services**. Home Assistant should show **Discovered: pool-level**.
3. Press **Configure**, then **Submit**.

You'll then have these entities:

| Entity | What it does |
|---|---|
| **Distance** | radar to water, in cm. It goes UP as the pool drops |
| **Water Level** | the radar's own level reading. Ignore it at 45° |
| **Fill Valve** | switch to open or close the valve by hand |
| **Auto Top-Up** | switch to turn the automatic filling on or off |
| **Start Fill Above** | the valve opens when Distance stays above this for 2 minutes |
| **Stop Fill Below** | the valve closes when Distance drops below this |
| **Max Fill Time** | safety cut-off, in minutes |
| **Fill Lockout** | on if the safety cut-off fired |
| **Reset Fill Lockout** | button that clears the lockout |
| **Installation Height** | radar setting. Leave it alone |

## 6. Set the fill levels

Because the radar looks at the water at 45°, the **Distance** changes by about 1.4 cm for every 1 cm the water level moves. Use the readings you actually see rather than tape measurements:

1. With the pool at the level you want, note **Distance**. Say it reads 60.0.
2. Set **Stop Fill Below** to that number (60.0).
3. Set **Start Fill Above** about 3 cm higher (63.0). That's roughly a 2 cm drop in the water.
4. Set **Max Fill Time** to a bit longer than a normal top-up takes. 60 minutes is the default.
5. Turn on **Auto Top-Up**.

## 7. Updates later

Change the YAML in ESPHome, press **Save**, then **⋮ → Install → Wirelessly**.

## Optional: get a notification if the safety cut-off fires

Go to **Settings → Automations → Create → Edit in YAML** and paste this. Change `notify.mobile_app_your_phone` to your phone's notify service.

```yaml
alias: Pool top-up lockout
triggers:
  - trigger: state
    entity_id: binary_sensor.pool_level_fill_lockout
    to: "on"
actions:
  - action: notify.mobile_app_your_phone
    data:
      message: "Pool top-up hit the max fill time and locked out. Check for a leak, then press Reset Fill Lockout."
```
