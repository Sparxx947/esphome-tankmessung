🇩🇪 [Deutsche Version](einmessen.md)

# Calibration

The chain in the firmware:

```
Rohwert (HX710B, 24 bit)  →  Druck p [mbar]  →  Füllhöhe h [cm]  →  Inhalt V [l]
```

(Rohwert = raw value, Druck = pressure, Füllhöhe = fill height, Inhalt = contents.)

## 1. Formulas

| Step | Formula | Constant |
|---|---|---|
| Raw value → pressure | `p = (roh − roh_null) / roh_pro_mbar` | `roh_null = −2.788.747`, `roh_pro_mbar = 70.056` |
| Pressure → fill height | `h = p / 0,824` (clamped to 0 … 160 cm) | Heating oil EL ρ ≈ 0.84 kg/l: 0.84 × 9.81 × 0.01 / 100 ≈ 0.824 mbar/cm |
| Fill height → contents | Circular segment `A = r²·acos((r−h)/r) − (r−h)·√(2rh − h²)` with h in dm, `V = A · L · 7000 / (π·r²·L)` | r = 8 dm, L = 37.5 dm (dished ends neglected, scaled to 7,000 l) |
| Water for calibration | 10 cm water column = **9.81 mbar** | ρ water = 1.0 |

(The constants in the formula column use German number formatting: `−2.788.747` = −2,788,747; `0,824` = 0.824.)

## 2. Calibration on the bench (as done on 08.10.2026)

Required: glass of water, ruler, the box with hose connected, HA entity `sensor.oltank_druck_rohwert` (pressure raw value).

1. **Warm-up:** switch on the device and wait **at least 5 minutes**. Measured: the zero point moved by ~38,500 units in the first
   minutes (≈ 0.55 mbar ≈ 7 mm oil), stable afterwards (16:16 → 16:21 Δ ~300). Noise ~100–300.
2. **Seal the gauge branch:** on the bench, the T had a branch "to the old gauge". A check valve used as a plug leaks
   already at ~10 mbar – that was the actual fault on 08.10. Hold the branch shut or seal it firmly.
3. **Zero point:** hose end open to the air, `Messung starten` ("Start measurement"), note the raw value (2 readings) → `roh_null`.
   - 08.10.: **−2,788,747** (warm).
4. **Slope:** hose end vertically **10 cm below the water surface** (measured from the hose mouth), `Messung starten` ("Start measurement"),
   it must bubble; note the raw value.
   - 08.10.: **−2,101,492**.
5. Calculate:
   ```
   roh_pro_mbar = (roh_10cm − roh_null) / 9,81
                = (−2.101.492 − (−2.788.747)) / 9,81
                = 687.255 / 9,81 ≈ 70.056
   ```
6. Enter the values into the `substitutions` of the YAML in the **ESPHome Builder** → OTA. Mirror the change in the local `firmware/tankmessung.yaml`.
7. **Cross-check:** 10 cm of water again → target 9.81 mbar.
   - 08.10. 16:27: **10.01 / 10.02 mbar** (+2 % ≈ 2 mm immersion depth), fill height 12.1 cm oil equivalent, contents 243 l. ✔

Tolerance: the immersion depth by hand varies by a few millimetres (later runs 10.07 … 10.76 mbar). For the tank,
1 mbar ≈ 1.2 cm of oil; in the lower range that is 20–45 l depending on the height.

## 3. Comparison at the tank (after installation)

The bench calibration only calibrates the sensor. At the tank, further factors come in: position of the line end above the tank bottom,
actual tank dimensions and the oil density. Therefore check against an independent measurement:

1. **Dipstick in the manhole** (possibly with water-finding paste, to detect water/sludge at the bottom).
2. Expectation after the delivery of 05.10. (1,500 l into an "empty" tank, old gauge showed 1,900 l afterwards):

   | Contents | Fill height | Pressure (calculated) |
   |---|---|---|
   | 1,500 l | 42.7 cm | 35.2 mbar |
   | 1,700 l | 46.7 cm | 38.5 mbar |
   | 1,900 l | 50.6 cm | 41.7 mbar |

   Since then the burner has been running again – so the current level is somewhat lower.
   **Resolved on 09.10.:** the 1,900 l were wrong – the old gauge is defective (~800 l without pressure).
3. If the dipstick reading differs:
   - **constant offset in cm** → line end does not sit on the bottom, or sludge; correction via
     `number.oltank_leitungsende_uber_boden` (in the firmware since 09.10., added to the fill height).
   - **proportional deviation** → oil density/tank dimensions; adjust `oel_mbar_pro_cm`.
4. Later, additionally cross-check with every **delivered quantity** (increase in litres before/after the delivery).

### Comparison without a dipstick: delivery balance (09.10.2026)

The dipstick could not be reached. Instead:

- 05.10.: **1,500 l** into an "empty" tank (the burner got no more oil = level at the end of the suction pipe).
- Consumption until 09.10. ~35 l (estimated, ~7 l/day in October) → now **at least ~1,465 l** + the remainder below the suction pipe.
- Measured **without** correction: 30.95–31.1 mbar while pumping, ≈ 30 mbar after 10 s → 36.1 cm ≈ **1,184 l** – less than
  the delivery alone. → The line end sits **above the tank bottom**.

The remainder below the suction pipe stays unknown. Depending on it:

| Suction pipe ends … above bottom | Remainder before delivery | Contents now | Line end above bottom |
|---|---|---|---|
| 3 cm | 30 l | ≈ 1,495 l | **6.5 cm** (set) |
| 5 cm | 65 l | ≈ 1,530 l | 7.2 cm |
| 10 cm | 182 l | ≈ 1,647 l | 9.6 cm |
| 15 cm | 331 l | ≈ 1,796 l | 12.5 cm |
| 20 cm | 505 l | ≈ 1,970 l | 15.8 cm |

The **minimum of 6.5 cm** is set: contents are shown rather too low – the safe side for warnings.
Check run 09.10. 16:07: **43.0 cm ≈ 1,516 l**.

**Exact comparison at the next delivery:** one measurement directly before and one directly after, quantity from the delivery
note. Because the tank is round, each centimetre corresponds to a different number of litres depending on the height – two
heights plus the known litre difference give the correction unambiguously.

## 4. Dipstick table (from the firmware formula)

Calculated with r = 8 dm, L = 37.5 dm, scaled to 7,000 l, 0.824 mbar/cm. The expected raw value applies to the
calibration of 08.10. Pressure and raw value apply **without** the line-end correction; with the correction, a pressure
belongs to the fill height "table height + correction".

| Fill height | Contents | Pressure | Raw value (expected) |
|---|---|---|---|
| 10 cm | 182 l | 8.2 mbar | −2,211,000 |
| 20 cm | 505 l | 16.5 mbar | −1,634,000 |
| 28 cm | 823 l | 23.1 mbar | −1,172,000 |
| 30 cm | 909 l | 24.7 mbar | −1,057,000 |
| 40 cm | 1,369 l | 33.0 mbar | −480,000 |
| 50 cm | 1,869 l | 41.2 mbar | +98,000 |
| 60 cm | 2,398 l | 49.4 mbar | +675,000 |
| 70 cm | 2,944 l | 57.7 mbar | +1,252,000 |
| 80 cm | 3,500 l | 65.9 mbar | +1,829,000 |
| 100 cm | 4,602 l | 82.4 mbar | +2,984,000 |
| 120 cm | 5,631 l | 98.9 mbar | +4,138,000 |
| 140 cm | 6,495 l | 115.4 mbar | +5,293,000 |
| 160 cm | 7,000 l | 131.8 mbar | +6,447,000 |

Warning thresholds (planned): 1,500 l ≈ 42.7 cm, 800 l ≈ 27.5 cm.

> Note (calculated, not verified on the device): the HX710B delivers 24-bit values up to +8,388,607. With this calibration
> that would be reached at around **160 mbar**. A full tank (132 mbar) still fits; values above that are not a fill level,
> but pump pressure in a blocked line.

## 5. Settings after calibration

| Entity | Normal operation | Leak test |
|---|---|---|
| `number.oltank_spulzeit_pumpe` (pump flush time) | 30 s | 30 s |
| `number.oltank_beruhigungszeit` (settling time) | **10 s** | 60 s |
| `number.oltank_uberdruck_grenze` (overpressure limit) | 150 mbar | 150 mbar (first run on a new line: 50 mbar) |
| `number.oltank_leitungsende_uber_boden` (line end above bottom) | 6.5 cm (provisional, see above) | – |
| `switch.oltank_automatische_messung` (automatic measurement) | **on** only after the comparison at the tank (on since 09.10.) | off |
