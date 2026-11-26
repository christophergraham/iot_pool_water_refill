/*
  Pool auto top-up controller
  ---------------------------
  Reads the distance from a DFRobot SEN0676 80 GHz radar level sensor
  (UART, Modbus-RTU) mounted above the water, and opens a 12 V solenoid
  valve through a low-side MOSFET module when the water is too low.

  "Distance" here is the gap from the radar lens DOWN to the water surface,
  in millimetres. When the pool level DROPS, the distance gets BIGGER.

  Safety behaviour (valve is normally closed, so "off" = safe):
    - Valve only opens after the level has been low for CONFIRM_SECONDS
      (ignores waves, swimmers, a leaf on the surface).
    - Valve closes at STOP_FILL_DISTANCE_MM (hysteresis gap stops chatter).
    - Valve closes and LOCKS OUT if it has been open longer than
      MAX_FILL_MINUTES. Send 'r' over Serial Monitor or press reset to clear.
    - Valve closes if the sensor stops answering or gives nonsense.
    - Minimum rest time between fills.

  Board support (picked automatically):
    - ESP32 DevKit (WROOM-32)       : sensor on Serial2 (GPIO16 = RX2, GPIO17 = TX2),
                                      valve on GPIO26, status LED on GPIO2
    - Arduino Uno R4 WiFi / Minima : sensor on Serial1 (D0 = RX, D1 = TX)
    - Arduino Mega 2560             : sensor on Serial1 (D19 = RX, D18 = TX)
    - Arduino Uno R3 / Nano         : sensor on SoftwareSerial (D2 = RX, D3 = TX)

  Serial Monitor at 115200 baud. Commands for bench testing:
    o = open valve for 10 s (test)    c = close valve
    r = reset a lockout               s = print status now
*/

// ======================= SETTINGS YOU WILL CHANGE =======================

// Water too low -> start filling when distance is MORE than this (mm)
const uint16_t START_FILL_DISTANCE_MM = 450;

// Water high enough -> stop filling when distance is LESS than this (mm)
// Must be smaller than START_FILL_DISTANCE_MM. The difference is your
// hysteresis band. 20-30 mm is a sensible start for a pool.
const uint16_t STOP_FILL_DISTANCE_MM  = 425;

// Level must look low for this long before the valve opens
const uint32_t CONFIRM_SECONDS        = 120;

// Hard safety limit for a single fill. Time a real top-up first and set
// this to about 1.5x what a normal fill takes.
const uint32_t MAX_FILL_MINUTES       = 60;

// Minimum time between the end of one fill and the start of the next
const uint32_t MIN_REST_MINUTES       = 30;

// If no good reading for this long, the valve is forced closed
const uint32_t SENSOR_TIMEOUT_SECONDS = 15;

// Readings outside this window are thrown away (sensor spec: 150 mm - 40 m)
const uint16_t MIN_VALID_MM           = 150;
const uint16_t MAX_VALID_MM           = 5000;

// ============================ PINS ======================================

#if defined(ARDUINO_ARCH_ESP32)
const uint8_t VALVE_PIN = 26;           // D26 -> MOSFET module signal pin
const uint8_t LED_PIN   = 2;            // blue on-board LED on most DevKits
#else
const uint8_t VALVE_PIN = 7;            // D7 -> MOSFET module signal pin
const uint8_t LED_PIN   = LED_BUILTIN;  // on = valve open, fast blink = fault
#endif

// ======================= SENSOR (Modbus-RTU) ============================

const uint32_t SENSOR_BAUD   = 115200;  // factory default per DFRobot wiki
const uint8_t  SENSOR_ADDR   = 0x01;    // factory default
const uint16_t REG_EMPTY_HEIGHT = 0x0001; // "empty height" = lens to water, mm

#if defined(ARDUINO_ARCH_ESP32)
  #define SENSOR_PORT Serial2
  #define SENSOR_BEGIN() Serial2.begin(SENSOR_BAUD, SERIAL_8N1, 16, 17)  // RX2, TX2
#elif defined(ARDUINO_ARCH_RENESAS) || defined(HAVE_HWSERIAL1)
  #define SENSOR_PORT Serial1
#else
  #include <SoftwareSerial.h>
  SoftwareSerial sensorSerial(2, 3);    // RX = D2 (from sensor TX), TX = D3 (to sensor RX)
  #define SENSOR_PORT sensorSerial
#endif
#ifndef SENSOR_BEGIN
  #define SENSOR_BEGIN() SENSOR_PORT.begin(SENSOR_BAUD)
#endif

// ========================================================================

enum State { IDLE, CONFIRMING, FILLING, RESTING, LOCKED_OUT };
State state = IDLE;

uint32_t stateSince   = 0;   // millis() when we entered the current state
uint32_t lastGoodRead = 0;
uint32_t lastPoll     = 0;
uint32_t testOpenUntil = 0;
bool     valveOpen    = false;

const uint8_t N_SAMPLES = 5;
uint16_t samples[N_SAMPLES];
uint8_t  nSamples = 0, sampleIdx = 0;
int32_t  filteredMm = -1;    // median of recent good readings, -1 = none yet

const char* stateName(State s) {
  switch (s) {
    case IDLE: return "IDLE";
    case CONFIRMING: return "CONFIRMING";
    case FILLING: return "FILLING";
    case RESTING: return "RESTING";
    default: return "LOCKED_OUT";
  }
}

uint16_t modbusCrc(const uint8_t* buf, uint8_t len) {
  uint16_t crc = 0xFFFF;
  for (uint8_t i = 0; i < len; i++) {
    crc ^= buf[i];
    for (uint8_t b = 0; b < 8; b++) crc = (crc & 1) ? (crc >> 1) ^ 0xA001 : crc >> 1;
  }
  return crc;
}

// Reads one 16-bit holding register. Returns true and fills 'value' on success.
bool readRegister(uint16_t reg, uint16_t& value) {
  uint8_t req[8] = { SENSOR_ADDR, 0x03, (uint8_t)(reg >> 8), (uint8_t)reg, 0x00, 0x01, 0, 0 };
  uint16_t crc = modbusCrc(req, 6);
  req[6] = crc & 0xFF;   // Modbus sends CRC low byte first
  req[7] = crc >> 8;

  while (SENSOR_PORT.available()) SENSOR_PORT.read();   // drop stale bytes
  SENSOR_PORT.write(req, 8);
  SENSOR_PORT.flush();

  // Expected reply: addr, 0x03, byteCount=2, hi, lo, crcLo, crcHi
  uint8_t resp[7];
  uint8_t got = 0;
  uint32_t t0 = millis();
  while (got < 7 && millis() - t0 < 300) {
    if (SENSOR_PORT.available()) {
      uint8_t c = SENSOR_PORT.read();
      if (got == 0 && c != SENSOR_ADDR) continue;      // resync on address byte
      resp[got++] = c;
    }
  }
  if (got < 7 || resp[1] != 0x03 || resp[2] != 2) return false;
  uint16_t rc = modbusCrc(resp, 5);
  if (resp[5] != (rc & 0xFF) || resp[6] != (rc >> 8)) return false;
  value = ((uint16_t)resp[3] << 8) | resp[4];
  return true;
}

int32_t medianOfSamples() {
  uint16_t tmp[N_SAMPLES];
  for (uint8_t i = 0; i < nSamples; i++) tmp[i] = samples[i];
  for (uint8_t i = 1; i < nSamples; i++) {           // insertion sort, tiny array
    uint16_t v = tmp[i]; int8_t j = i - 1;
    while (j >= 0 && tmp[j] > v) { tmp[j + 1] = tmp[j]; j--; }
    tmp[j + 1] = v;
  }
  return tmp[nSamples / 2];
}

void setValve(bool open) {
  if (open != valveOpen) {
    Serial.print(F(">> Valve "));
    Serial.println(open ? F("OPEN") : F("CLOSED"));
  }
  valveOpen = open;
  digitalWrite(VALVE_PIN, open ? HIGH : LOW);
}

void enter(State s) {
  if (s != state) {
    Serial.print(F(">> State "));
    Serial.print(stateName(state));
    Serial.print(F(" -> "));
    Serial.println(stateName(s));
  }
  state = s;
  stateSince = millis();
}

void printStatus() {
  Serial.print(F("dist="));
  if (filteredMm < 0) Serial.print(F("--")); else Serial.print(filteredMm);
  Serial.print(F("mm  state="));
  Serial.print(stateName(state));
  Serial.print(F("  valve="));
  Serial.print(valveOpen ? F("OPEN") : F("closed"));
  Serial.print(F("  inState="));
  Serial.print((millis() - stateSince) / 1000);
  Serial.println(F("s"));
}

void handleCommands() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == 'o') { testOpenUntil = millis() + 10000UL; Serial.println(F("Test open 10 s")); }
    if (c == 'c') { testOpenUntil = 0; setValve(false); if (state == FILLING) enter(RESTING); }
    if (c == 'r' && state == LOCKED_OUT) { Serial.println(F("Lockout cleared")); enter(IDLE); }
    if (c == 's') printStatus();
  }
}

void setup() {
  pinMode(VALVE_PIN, OUTPUT);
  digitalWrite(VALVE_PIN, LOW);           // closed before anything else happens
  pinMode(LED_PIN, OUTPUT);

  Serial.begin(115200);
  SENSOR_BEGIN();
  delay(500);                             // sensor start-up time is ~100 ms
  Serial.println(F("\nPool top-up controller starting"));
  Serial.print(F("Start fill above ")); Serial.print(START_FILL_DISTANCE_MM);
  Serial.print(F(" mm, stop below ")); Serial.print(STOP_FILL_DISTANCE_MM); Serial.println(F(" mm"));
  if (STOP_FILL_DISTANCE_MM >= START_FILL_DISTANCE_MM) {
    Serial.println(F("CONFIG ERROR: STOP must be less than START. Valve disabled."));
    enter(LOCKED_OUT);
  }
  lastGoodRead = millis();
  stateSince = millis();
}

void loop() {
  uint32_t now = millis();
  handleCommands();

  // ---- 1. Poll the sensor once a second ----
  if (now - lastPoll >= 1000) {
    lastPoll = now;
    uint16_t mm;
    if (readRegister(REG_EMPTY_HEIGHT, mm) && mm >= MIN_VALID_MM && mm <= MAX_VALID_MM) {
      samples[sampleIdx] = mm;
      sampleIdx = (sampleIdx + 1) % N_SAMPLES;
      if (nSamples < N_SAMPLES) nSamples++;
      filteredMm = medianOfSamples();
      lastGoodRead = now;
    } else {
      Serial.println(F("! sensor read failed or out of range"));
    }
    printStatus();
  }

  bool sensorOk = (now - lastGoodRead) < SENSOR_TIMEOUT_SECONDS * 1000UL && filteredMm >= 0;
  bool tooLow   = sensorOk && filteredMm > START_FILL_DISTANCE_MM;
  bool fullEnough = sensorOk && filteredMm < STOP_FILL_DISTANCE_MM;
  uint32_t inState = now - stateSince;

  // ---- 2. State machine ----
  switch (state) {
    case IDLE:
      if (tooLow) enter(CONFIRMING);
      break;

    case CONFIRMING:
      if (!tooLow) enter(IDLE);
      else if (inState >= CONFIRM_SECONDS * 1000UL) enter(FILLING);
      break;

    case FILLING:
      if (!sensorOk) {
        Serial.println(F("! sensor lost while filling - closing"));
        enter(RESTING);
      } else if (fullEnough) {
        enter(RESTING);
      } else if (inState >= MAX_FILL_MINUTES * 60000UL) {
        Serial.println(F("!! MAX FILL TIME REACHED - LOCKED OUT. Check for leaks/sensor, then send 'r'."));
        enter(LOCKED_OUT);
      }
      break;

    case RESTING:
      if (inState >= MIN_REST_MINUTES * 60000UL) enter(IDLE);
      break;

    case LOCKED_OUT:
      break;
  }

  // ---- 3. Drive the valve ----
  bool testOpen = testOpenUntil && (int32_t)(testOpenUntil - now) > 0;
  if (!testOpen) testOpenUntil = 0;
  setValve(state == FILLING || testOpen);

  // ---- 4. Status LED ----
  if (state == LOCKED_OUT)      digitalWrite(LED_PIN, (now / 150) % 2);   // fast blink
  else if (!sensorOk)           digitalWrite(LED_PIN, (now / 1000) % 2);  // slow blink
  else                          digitalWrite(LED_PIN, valveOpen);
}
