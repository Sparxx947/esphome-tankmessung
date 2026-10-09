🇩🇪 [Deutsche Version](README.md)

# Tankmessung – pneumatic level measurement on the oil tank

An ESP32 running ESPHome measures the level of the underground heating-oil tank via the **existing pneumatic measuring line**
and reports pressure, fill height and contents in litres to Home Assistant (device `Öltank` – "oil tank").

> Status: **09.10.2026**. Installed at the tank and in operation: measuring line clear, leak-tight, automatic measurement every 6 h on.
> Level provisionally matched via the delivery balance (dipstick not reachable); exact comparison at the next delivery.

> **Rebuilding this project?** The values in this repo belong to *this* tank and *this* sensor:
> - Create your own `secrets.yaml` from [`firmware/secrets.example.yaml`](firmware/secrets.example.yaml) (Wi-Fi, API key, fallback hotspot password).
> - Adjust the tank geometry substitutions `tank_radius_dm`, `tank_laenge_dm` (length) and `tank_nenn_l` (nominal volume) as well as the oil density (`oel_mbar_pro_cm`) to your tank.
> - Calibrate `roh_null` and `roh_pro_mbar` yourself (see [docs/einmessen.en.md](docs/einmessen.en.md)) – the values in the firmware are specific to this individual HX710B sensor and will not fit yours.

---

## 1. Summary

| | |
|---|---|
| **What** | Level of the heating-oil tank (pressure in mbar → fill height in cm → contents in litres) |
| **Tank** | Steel underground tank, outdoors, **7,000 l**, DIN 6608-D, built 1967, double-walled with leak detector. Dimensions according to the DIN 6608 table (current standard): **Ø 1,600 mm × 3,750 mm** – the 1967 edition of the standard has not been cross-checked. |
| **Where** | Boiler room, on the wall next to the old pneumatic gauge (scale 0–7,000 l with hand pump). Tap point: vertical copper section (6 mm) between the separator cup and the old gauge. |
| **Principle** | Like the old gauge ("pump before reading"): a mini pump pushes air into the measuring line until it bubbles out at the end of the line. After switching off, a check valve holds the air in the line; the remaining pressure equals the oil column above the end of the line. A pressure sensor (HX710B, 0–40 kPa) measures it – also **while** pumping, with an overpressure cut-off. The end of the line sits above the tank bottom; the height below it is added as an adjustable correction. |
| **Physics** | Heating oil EL ρ ≈ 0.84 kg/l → **1 cm oil ≈ 0.824 mbar**, full tank (160 cm) ≈ **132 mbar**, 1 m oil ≈ 82 mbar. |
| **Volume** | Horizontal cylinder (circular segment), dished ends neglected, scaled to 7,000 l (formula in [docs/einmessen.en.md](docs/einmessen.en.md)). |

The old gauge stays connected but is **defective** (shows ~800 l without pressure, just under 1,900 l when pumped, with ~1,500 l actually in the tank). In addition there is the project "Heating via Optolink"
(second ESP32, `heizung-optolink`, .193) for burner hours and fault messages – not part of this repo.

---

## 2. Status (as of 09.10.2026)

| Area | Status | Date / note |
|---|---|---|
| Firmware flashed, in HA, in the ESPHome Builder | ✅ done | 06.10.2026 ~20:00 |
| Static IP in the FRITZ!Box (.194) | ✅ done | 06.10.2026 |
| MOSFET module: D4184 identified as unsuitable, replaced by CQUANZX dual MOSFET | ✅ done | identified 06.10., delivered 07.10. |
| Enclosure corrected (standoffs, SMA position, tabs, HX710B standoffs, inner height 40) | ✅ done | 08.10.2026 |
| Enclosure printed and assembled, assembly plan printed | ✅ done | 08.10.2026 |
| First pump test | ✅ runs (after re-tightening terminals) | 08.10.2026 15:27 |
| **Bench calibration** (water column 10 cm) | ✅ done | 08.10.2026 16:25, cross-check 16:27 |
| Function + leak test in the box (60 s) | ✅ tight (2 of 3 runs, one drop unexplained) | 08.10.2026 18:07–18:15 |
| Brass T 6×4×6 | ✅ delivered, installed | 09.10.2026 |
| **Measuring line clear?** | ✅ clear | 09.10.2026: pressure stays flat at the oil column while pumping (air bubbles out) – blowing clear was not needed |
| Installation at the tank, first run, leak test | ✅ done | 09.10.2026 15:44–16:07 (one leak at the new connections found and sealed) |
| Overpressure cut-off + line-end correction (firmware) | ✅ flashed | 09.10.2026 15:52 / 16:06 – cut-off **never triggered yet**, untested in a real fault |
| Level comparison | ⚠️ provisional | dipstick not reachable → delivery balance, correction 6.5 cm (minimum); exact at the next delivery |
| Automatic measurement (every 6 h) | ✅ on | since 09.10.2026 16:07 |
| HA automations (warning, forecast) | ❌ open | none created yet (checked 08.10.: no automation/script uses the device) |

---

## 3. Bill of materials

Source: project notes and workshop book. Prices at time of ordering (October 2026, Amazon.de).
The first basket for the pneumatics (8 items, €54.62) was ordered on 04.10.2026.

### Electronics

| Part | Qty | Description / type | Source, ASIN, price | Status |
|---|---|---|---|---|
| Microcontroller | 1 | ESP32-WROOM-32U DevKitC V4, USB-C, with antenna kit (U.FL→SMA pigtail + 2.4 GHz antenna), board `esp32dev`, CP2102 | Amazon B0F6567LB5, €13.99 each (2 ordered; the second one is in the Optolink project) | ✅ available, flashed |
| Pressure sensor | 1 (of 3) | Pressure sensor module 0–40 kPa with HX710B (24 bit), hose barb for 2.5 mm hose | Amazon B0B1TZH7RR, €10.99 (3 pcs) | ✅ available, installed |
| Air pump | 1 | Mini diaphragm pump "M20", DC 3–3.7 V, 80–120 kPa; flattened N20 motor, 9.95 mm (flat sides) × 38 mm, 2 ports at the front, solder tabs at the back | Amazon B0GQ3MWP3R, €6.89 (only 2 reviews) | ✅ available, installed |
| MOSFET module | 1 (of 5) | Dual MOSFET trigger module 15 A / 400 W ("XY-MOS", 2× AOD4184A in parallel, **without** optocoupler), trigger 3.3–20 V, load 5–36 V, PWM 0–20 kHz, 35 × 17.2 × 14.2 mm | Amazon CQUANZX B07VRCXGFY, €8.49 (5 pcs) | ✅ delivered 07.10., installed |
| Flyback diode | 1 | Schottky 1N5819 | Diode assortment BOJACK B07YK3XMQQ, €10.99 | ✅ delivered 07.10., installed |
| ~~MOSFET module D4184~~ | – | DollaTek "D4184 MOSFET module" (PC817 optocoupler, gate driven from the load voltage) – **wrong purchase, does not switch at 5 V** | Amazon B07HBVTWMY, €5.99 (5 pcs) | ⚠️ unused; cancel or keep: Jens decides |
| Cables | approx. 8 | Dupont jumpers F2F/M2F (ELEGOO set, 20 cm) | available (bought 2023) | ✅ available |
| Power supply | 1 | USB-C power supply **≥ 1 A**, 5 V | not recorded in the notes | ❓ unclear |

### Pneumatics

| Part | Qty | Description / type | Source, ASIN, price | Status |
|---|---|---|---|---|
| T-piece measuring line | 1 | Brass hose-barb T **6 × 4 × 6 mm** (6 mm through, 4 mm branch) | Amazon B0GHMXRYNT, €5.99 (2 pcs) | ✅ installed 09.10. |
| Silicone hose 6 mm ID | 1 m | Silicone hose 6 mm ID (onto the cut 6 mm copper line) | Amazon B0CYGQD96H, €5.59 | ordered 04.10. (delivery not explicitly noted) |
| Hose clamps | 10 | Stainless-steel hose clamps 6–12 mm (Leryati) | Amazon B0C24792WR, €4.99 | ordered 04.10. (delivery not explicitly noted) |
| Aquarium set | 1 | 48 pieces: 6 m silicone hose 4 mm, check valves, T and L connectors | Amazon B0C2PYBDGJ, €9.99 | ✅ available, used in the box (check valve + T) |
| Silicone hose 2.5 mm | 1 m | Silicone hose 2.5 mm ID × 4 mm OD – fits the sensor barb and sits tightly in the 4 mm aquarium hose | Amazon B0CXPW74GZ, €4.19 | ordered 04.10. (delivery not explicitly noted) |
| Measuring line | – | existing copper line **6 mm OD** (Jens measured 6.1 mm) from the tank into the basement | existing | ✅ clear (09.10.) |

Fallback if the brass T fails again: push-fit T 6-4-6 POM (B0GLGCTVRH) or PA (B0CB8V2NXD).
Unverified whether push-fit connectors hold tight and pull-proof on 6.1 mm copper – before installation do a pull test + pressure-hold test.

### Enclosure and small parts

| Part | Qty | Description / type | Source | Status |
|---|---|---|---|---|
| Filament | approx. 1 box + lid | PETG or PLA (room temperature, wall mounting) | existing | ✅ box printed 08.10. (material not noted) |
| Cable ties | 4 | narrow, fitting slots 3.5 × 1.8 mm (2× pump, 1× MOSFET, 1× valve) | existing | ✅ (stock not explicitly noted) |
| Hot glue | – | HX710B onto its 2 standoffs | existing | ✅ |
| Wall screws + plugs | 4 | for tabs Ø 4.5 mm (so screws ≤ 4 mm) | – | ❓ not in the notes |
| Magnets | 0 | – (the 10 × 3 mm magnets belong to the Optolink enclosure) | – | – |
| Resistors | 0 | The circuit needs none (HX710B module and MOSFET module are fully assembled). | – | – |

### Tools / aids

Calipers, multimeter, soldering iron, 3D printer, glass of water + ruler (calibration),
dipstick for the manhole (possibly with water-finding paste) – **not reachable on 09.10.**, comparison therefore via the delivery balance.

---

## 4. Pin assignment and wiring

Schematic: [`plaene/tankmessung-schaltplan.pdf`](plaene/tankmessung-schaltplan.pdf)
(source `plaene/tank_plan.py`, preview `plaene/tank_plan.svg`).
Box assembly: [`plaene/tank-bestueckung.pdf`](plaene/tank-bestueckung.pdf) (source `plaene/tank_bestueckung_plan.py`).

> The schematic PDF reflects the state of **2026-10-08** (85 % PWM, calibrated values). The SVG `tank_plan.svg` still shows the state of 2026-10-06; the wiring is identical.

| From | To | Note |
|---|---|---|
| HX710B **VCC** | ESP32 **3V3** | **not** to 5 V – otherwise 5 V levels on GPIO19 |
| HX710B **GND** | ESP32 GND | common ground |
| HX710B **OUT** | **GPIO19** | ESPHome platform `hx711` (`dout_pin`) |
| HX710B **SCK** | **GPIO18** | `clk_pin`, gain 128 |
| MOSFET **TRIG/PWM** | **GPIO25** | LEDC PWM 20 kHz |
| MOSFET **GND** (control side) | ESP32 GND | |
| MOSFET **VIN+** | ESP32 **5V** | 5 V from the DevKit (from USB, power supply ≥ 1 A) |
| MOSFET **VIN−** | ESP32 GND | |
| MOSFET **OUT+** | Pump **+ (red)** | |
| MOSFET **OUT−** | Pump **− (black)** | Module switches **minus** – pump only on OUT+/OUT−, never between VIN− and GND |
| 1N5819 | parallel to the pump | **Stripe (cathode) to OUT+**; clamped into the terminals too |
| Antenna | U.FL on the module → pigtail → SMA socket in the front wall | The WROOM-**32U** has no PCB antenna |

On the underside of the module (XY-MOS, according to photo 08.10.): OUT+ bottom, OUT− top, VIN right. The marking on the module takes precedence.

**Hose routing:**

```
Tankboden ── Kupfer 6 mm ── Messing-T 6×4×6 ──(6-mm-Silikon + Schellen)── alte Anzeige  (dauerhaft DICHT)
                                 │
                            4-mm-Schlauch
                                 │
                       (rechte Wand der Box)
                                 │
                          Aquarium-T 4 mm ──── HX710B-Stutzen (2,5-mm-Silikon)
                                 │
                       Rückschlagventil  (Pfeil zeigt zum T / zur Leitung)
                                 │
                       Pumpe, blasender Stutzen   (Ansaugstutzen OFFEN lassen)
```

(Diagram legend: Tankboden = tank bottom; Kupfer = copper; Messing-T = brass T; Silikon + Schellen = silicone + clamps;
alte Anzeige (dauerhaft DICHT) = old gauge (permanently SEALED); 4-mm-Schlauch = 4 mm hose; rechte Wand der Box = right wall of the box;
HX710B-Stutzen = HX710B hose barb; Rückschlagventil (Pfeil zeigt zum T / zur Leitung) = check valve (arrow points to the T / to the line);
Pumpe, blasender Stutzen (Ansaugstutzen OFFEN lassen) = pump, outlet port (leave the inlet port OPEN).)

---

## 5. Enclosure

Source: [`gehaeuse/tankmessung-gehaeuse.scad`](gehaeuse/tankmessung-gehaeuse.scad) (OpenSCAD, variable `TEIL = "box" | "deckel" | "alle"` – part = box | lid | all).

| File | Purpose | Dimensions |
|---|---|---|
| `gehaeuse/tank_box.stl` | Box with ESP compartment, standoffs, cable-tie slots, 4 wall tabs | outside 114 × 68 × 42 mm (+ tabs to 84 mm width), inside 110 × 64 × 40 mm |
| `gehaeuse/tank_deckel.stl` | Push-on lid with 3 mm rim and Ø 3 mm hole above the ESP status LED | 114 × 68 × 4.8 mm |
| `gehaeuse/vorschau_tank.png`, `vorschau_tank_oben.png` | Preview images | – |

**Material/printing:** PETG or PLA, 0.2 mm layer, **no supports**, bottom on the bed (the lettering "TANKMESSUNG" is mirrored and recessed into the bottom).

**Layout (top view, front = wall with SMA socket):**

| Area | Component | Fixing |
|---|---|---|
| left (x 2–53) | ESP32 DevKitC, USB-C through the left wall | rests on **4 standoffs** (17 mm high, each ~4.9 mm wide), pins + Dupont pointing **down** |
| divider x ~53 | 6 mm low stop, cables run over it | – |
| front, x 62 | SMA socket Ø 6.6 mm, 8 mm above the bottom | nut |
| front right (x 74–109) | MOSFET module, terminals towards the middle | 1 cable tie |
| middle (x ~71–89) | HX710B, pin header to the front/down, barb upward | **hot glue** on 2 standoffs (17 mm) under the ears |
| back (x 57–95) | pump lengthwise, solder tabs left, ports right | 2 cable ties |
| right | check valve, aquarium T below it | 1 cable tie |
| right wall | hose Ø 6.6 mm at the bottom, optional cable entry Ø 5 mm at the top | – |
| back wall | 8 ventilation slots | – |

**Lessons from building the enclosure** (all corrected before printing on 08.10.):

- **Pin headers run along the whole board length** (19 × 2.54 mm). Continuous end supports would have sat on the pins at both ends → 4 individual standoffs, 3.2 mm from the long edge, middle 12 mm left free (USB solder tabs).
- **SMA nut hit the pins**: the hole under the board (x 39.5) collided with the front pin header → moved to x 62, right next to the ESP compartment.
- **Pump tabs were crosswise** to the pump and the MOSFET module protruded 4 mm over the wall → tabs re-placed according to Jens' measurements, bounding-box collision check.
- **HX710B has its pin header pointing down** → stands on standoffs, inner height 30 → 40 mm (room for barb + hose bend); Dupont ↔ standoffs 1.1/1.4 mm clearance.
- General: **check for collisions before every STL export** (pins, nuts, connectors), measure parts with calipers beforehand.
- The hole line of the HX710B ears is only estimated from a photo – hence hot glue instead of screws.

Older versions are kept locally as `*.vor-stuetzen-20261008`, `*.vor-laschen-20261008` (excluded from the repo via `.gitignore`).

---

## 6. Firmware

File: [`firmware/tankmessung.yaml`](firmware/tankmessung.yaml) – state from the ESPHome Builder (09.10.2026).
**The version in the ESPHome Builder is authoritative**; mirror changes here.

| Setting | Value |
|---|---|
| Device name / hostname | `tankmessung` / `tankmessung.local` |
| Display name in HA | **Öltank** (oil tank) |
| IP | **192.168.178.194** (static assignment in the FRITZ!Box by MAC) |
| Board / framework | `esp32dev`, **esp-idf** |
| Logger | INFO |
| API | encrypted (`!secret tank_api_key`), OTA without its own password |
| Fallback hotspot | `Tank-Fallback` + captive portal (password `!secret tank_ap_password`) |

**Substitutions:**

| Name | Value | Meaning |
|---|---|---|
| `roh_null` | `-2788747.0` | HX710B raw value at 0 mbar (calibrated 08.10., sensor warm) |
| `roh_pro_mbar` | `70056.0` | Raw value increase per mbar |
| `oel_mbar_pro_cm` | `0.824` | Heating oil EL, ρ ≈ 0.84 |
| `tank_radius_dm` | `8.0` | Ø 1.6 m |
| `tank_laenge_dm` | `37.5` | 3.75 m (tank length) |
| `tank_nenn_l` | `7000` | Scaling to nominal volume |

**Pump:** `ledc` on GPIO25, 20 kHz, `max_power: 85%` (≈ 4.05 V at 4.77 V VIN; previously 70 %).
The pump is built for 3–3.7 V and runs on 5 V – hence the limit.
**Safety:** script `pumpe_sicherung` (pump safety) always switches the pump off after **60 s**, even in manual mode.

**Measurement sequence (script `messung` – measurement):** pump 100 % (= 85 % PWM) for the *flush time* (default 30 s). **While
pumping** the HX710B is read every 0.5 s; if the pressure rises above the *overpressure limit* (default 150 mbar), the pump switches
off immediately and the measurement is discarded (`binary_sensor.oltank_uberdruck_abbruch` = on). Fill height and contents are **not**
calculated while pumping. Otherwise: pump off → *settling time* (default 10 s) → read → 2 s → read again. The sensor is read **only**
in this script (`update_interval: never`). The highest pressure while pumping goes to `sensor.oltank_hochstdruck_beim_pumpen`.

**Fill height** = pressure / 0.824 + *line end above bottom* (default 6.5 cm). The measuring line ends above the tank bottom; oil
below it is invisible to the measurement (derivation in [docs/einmessen.en.md](docs/einmessen.en.md)).

> The overpressure cut-off has **never triggered** so far (the line is clear) – untested in a real fault.

### Entities in Home Assistant (16, checked 09.10.2026)

| Entity | Type | Purpose |
|---|---|---|
| `button.oltank_messung_starten` (start measurement) | Button | trigger a measurement |
| `switch.oltank_automatische_messung` (automatic measurement) | Switch (config) | measurement every 6 h – **OFF by default** (`RESTORE_DEFAULT_OFF`), on here since 09.10. |
| `number.oltank_spulzeit_pumpe` (pump flush time) | Number 5–60 s | pumping duration per measurement (30 s) |
| `number.oltank_beruhigungszeit` (settling time) | Number 2–60 s | waiting time before reading (10 s; 60 s for leak tests) |
| `number.oltank_uberdruck_grenze` (overpressure limit) | Number 50–300 mbar | overpressure cut-off while pumping (150 mbar) |
| `number.oltank_leitungsende_uber_boden` (line end above bottom) | Number 0–30 cm | correction: height of the line end above the tank bottom (6.5 cm) |
| `fan.oltank_pumpe` (pump) | Fan (diagnostic) | pump by hand, max. 60 s |
| `sensor.oltank_druck_rohwert` (pressure raw value) | Diagnostic | HX710B raw value (for calibration) |
| `sensor.oltank_druck` (pressure) | mbar | pressure = oil column |
| `sensor.oltank_fullhohe` (fill height) | cm | fill height incl. correction (clamped to 0–160 cm) |
| `sensor.oltank_inhalt` (contents) | L | contents, `device_class: volume_storage` |
| `sensor.oltank_hochstdruck_beim_pumpen` (max pressure while pumping) | mbar (diagnostic) | highest pressure while pumping (clear line ≈ oil column) |
| `binary_sensor.oltank_uberdruck_abbruch` (overpressure abort) | Problem | on = last measurement aborted due to overpressure (line blocked?) |
| `sensor.oltank_wlan_signal` (Wi-Fi signal) | dBm | −42 dBm on the bench, −50 to −61 dBm at the tank |
| `sensor.oltank_laufzeit` (uptime) | s | uptime |
| `button.oltank_neustart` (restart) | Button (diagnostic) | restart the ESP |

### Secrets

`firmware/secrets.example.yaml` is only a template with placeholders. The real values (`wifi_ssid`, `wifi_password`,
`tank_api_key`, `tank_ap_password`) are stored **only in the ESPHome Builder** (and locally outside the repo, permissions 600).
`.gitignore` excludes `secrets.yaml` and `secrets.*.yaml`. To generate a new API key: `openssl rand -base64 32`.

### Flashing

| Method | When | How |
|---|---|---|
| **OTA via the ESPHome Builder** (normal case) | every change | Edit the YAML in the Builder → *Install* → *Wirelessly*. The device has been online in the Builder since 06.10. ~20:05. |
| **Initial flash via USB** | new board / broken firmware | `esphome run tankmessung.yaml --no-logs --device /dev/ttyUSB0` with the **real** secrets. Grant access to the port first (`setfacl -m u:$USER:rw /dev/ttyUSB0`, again after every re-plug) or use group `dialout`. |
| **Emergency route on abort** | "No more data to read" | This board could not cope with 460800 baud: write the finished `firmware.factory.bin` with `esptool … --baud 115200`. |

> ⚠️ **Pitfall:** Never flash a test build with dummy secrets (happened on 06.10. with the sister device: wrong
> hotspot password, wrong API key). `esphome upload` **does not recompile** and blindly uploads the last build –
> for real firmware always use `esphome run` and watch for "Successfully compiled". Afterwards verify via the API with the real key.

---

## 7. Guides

| Guide | Content |
|---|---|
| [docs/aufbau.en.md](docs/aufbau.en.md) | Assembly and commissioning on the bench |
| [docs/einmessen.en.md](docs/einmessen.en.md) | **Calibration** with a water column, formulas, dipstick table, comparison at the tank |
| [docs/einbau.en.md](docs/einbau.en.md) | Installation at the tank, blowing the measuring line clear, AwSV, first run, leak test |
| [docs/fehlersuche.en.md](docs/fehlersuche.en.md) | known fault patterns with cause and solution |
| [docs/verlauf.en.md](docs/verlauf.en.md) | Project history 04.–09.10.2026 |

Short version:

1. **Assembly** according to `plaene/tank-bestueckung.pdf` (plug in the Dupont cables first, then the ESP onto the standoffs).
2. **Commissioning:** plug in the USB power supply, is the device online in HA? `Messung starten` ("Start measurement") with the hose open → pump runs, blows.
3. **Calibration:** zero point with the hose open (sensor warm, ≥ 5 min after switching on), then 10 cm water column = 9.81 mbar →
   `roh_pro_mbar = (roh_10cm − roh_null) / 9,81`. The cross-check must give ~10 mbar.
4. **Installation:** branch to the old gauge permanently sealed. Whether the line is clear shows in the first run (set the overpressure limit low beforehand, e.g. 50 mbar).
5. **Test:** first run with 60 s settling time (leak test), then comparison (dipstick or delivery balance), then settling time 10 s.
6. Only then switch on `Automatische Messung` ("Automatic measurement").

---

## 8. Home Assistant integration

- Integration: **ESPHome**, device `Öltank` (oil tank), 16 entities (table above).
- There is **no `ha/` folder yet** and no automations/scripts that use the device (search in HA on 08.10.2026).
- Planned (from the notes):
  - **Low-level warning:** early warning at 1,500 l, urgent at 800 l (push notification to the household members).
  - **Tank forecast** from consumption; comparison with oil consumption from burner hours × nozzle throughput (≤ 2.4 l/h) from the Optolink project.
  - Plausibility check against delivered quantities (reference: 3,000 l lasted ~14 months).
- Note for automations: the sensors only change after a measurement; with automatic measurement switched off, the last value stays.

---

## 9. Open items / next steps / dates

| Item | Who | Date |
|---|---|---|
| **Exact comparison of the line-end correction:** one measurement directly before and after the next delivery, delivered quantity from the delivery note → correction unambiguous | Jens + Claude | next oil delivery |
| Overpressure cut-off still untested in a real fault | – | watch |
| Old gauge defective (~800 l without pressure) – keep it or seal the branch | Jens | – |
| HA: warning 1,500 / 800 l, forecast | Claude | afterwards |
| Cancel or keep the D4184 wrong purchase | Jens | – |
| Level-limit sensor (Grenzwertgeber) with perforated sleeve: annual inspection by a specialist company or replacement with a slotted sleeve (TÜV note 2019 + 2024) | Jens | with the tank cleaning |
| Next AwSV inspection | Jens | 01/2029 (register from 11/2028) |

---

## 10. File overview

```
esphome-tankmessung/
├── README.md                         this file (German)
├── README.en.md                      this file (English)
├── .gitignore                        excludes secrets, build folders, backup versions
├── docs/
│   ├── aufbau.md / .en.md            assembly + commissioning on the bench
│   ├── einmessen.md / .en.md         calibration, formulas, dipstick table
│   ├── einbau.md / .en.md            installation at the tank, blowing clear, AwSV, leak test
│   ├── fehlersuche.md / .en.md       fault patterns (troubleshooting)
│   └── verlauf.md / .en.md           chronicle (project history)
├── firmware/
│   ├── tankmessung.yaml              ESPHome configuration (Builder state 09.10.2026)
│   └── secrets.example.yaml          template, no real values
├── gehaeuse/
│   ├── tankmessung-gehaeuse.scad     OpenSCAD source (box + lid)
│   ├── tank_box.stl                  box, inner height 40 (printed 08.10.)
│   ├── tank_deckel.stl               push-on lid
│   ├── vorschau_tank.png             preview
│   └── vorschau_tank_oben.png        preview from above
└── plaene/
    ├── tankmessung-schaltplan.pdf    schematic + hose routing (state 08.10.)
    ├── tank_plan.py                  generator of the schematic (matplotlib)
    ├── tank_plan.svg                 schematic as SVG (state 06.10.)
    ├── tank-bestueckung.pdf          assembly plan of the box, scale 2:1 (state 08.10.)
    └── tank_bestueckung_plan.py      generator of the assembly plan
```

The generator scripts still write to fixed paths outside the repo (`~/esphome/…` or a scratchpad) – adjust the output path
before running them again.
