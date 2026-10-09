🇩🇪 [Deutsche Version](verlauf.md)

# Project history

| Date | Event |
|---|---|
| 03/04.10.2026 | Viessmann fault D1 (burner fault) – tank empty, nobody noticed. The old pneumatic gauge nevertheless stood at ~800 l, even after pumping → at the time taken as a silted-up line (disproved on 09.10.: ~800 l is the rest position of the defective gauge). |
| 04.10. | Tank data from the TÜV documents: 7,000 l, DIN 6608-D, built 1967, steel, underground, double wall + leak detector, level-limit sensor (Grenzwertgeber); inspections 2019 and 2024 without defects, next 01/2029. Dimensions Ø 1.6 × 3.75 m from the DIN table. |
| 04.10. | Decision for route B (direct pneumatic measurement on the existing line) with ESP32 + HX710B + mini pump; budget variant with brass barb T instead of compression-fitting parts. Basket ordered. YAML and enclosure (inner height 30) prepared. |
| 05.10. | 1,500 l of heating oil delivered, old gauge showed 1,900 l afterwards. Burner runs again after bleeding. Brass T "could not be shipped". |
| 06.10. ~20:00 | Second ESP32 flashed (115200 baud, 460800 aborted), .194, in HA as `Öltank` (oil tank) (12 entities), static IP, online in the ESPHome Builder. |
| 06.10. evening | D4184 MOSFET module identified as unsuitable for 5 V → CQUANZX dual MOSFET + 1N5819 ordered. Schematic redrawn and printed. |
| 07.10. | Delivery: CQUANZX module, diode assortment. |
| 08.10. ~14:30 | Enclosure corrected before printing: ESP standoffs between the pin rows, SMA next to the ESP compartment, tabs according to measured dimensions (MOSFET 35 × 17.2 × 14.2, pump Ø 9.95 × 38), HX710B on 2 standoffs, inner height 40. Brass T reordered. |
| 08.10. ~14:55 | Box printed. |
| 08.10. 15:21–15:35 | First pump test: pump did not run (terminal contact suspected), runs after re-tightening. Zero point drifted. |
| 08.10. ~16:25 | **Calibrated** with 10 cm water column: `roh_null` −2,788,747, `roh_pro_mbar` 70,056, pump 70 → 85 %. The fault was a leak at the gauge branch. OTA via the Builder. |
| 08.10. 16:27 | Cross-check 10.01/10.02 mbar ✔. |
| 08.10. ~17:40 | Assembly plan created and printed. |
| 08.10. 18:07–18:15 | Box assembled: function ✔, leak test 60 s – one drop (unexplained), two runs tight. Settling time back to 10 s. |
| 08.10. ~18:30 | Question of blowing the line clear yourself; AwSV research: more likely subject to the specialist-company requirement, recommendation: specialist company. |
| 09.10. ~15:44 | **Installation at the tank** (brought forward from 10.10.). Box on the wall, Wi-Fi −61 dBm (later −50 dBm). Brass T fitted, branch to the old gauge sealed. Line not blown clear. |
| 09.10. 15:52 | Firmware: pressure is read **while** pumping every 0.5 s, **overpressure cut-off** (adjustable limit, default 150 mbar), max pressure + abort indicator. Reason: previously the pump ran a fixed 30 s – against a blocked line that would have overloaded the sensor. |
| 09.10. 15:53 | **Run 1** (limit 50 mbar for safety): linear rise ~7 mbar/s, from 15:53:43 a **plateau of 30.95 mbar, flat over 25 s of pumping** = air bubbles out → **line clear**, blowing clear not needed. After the pump stopped: drop 30.9 → 21.4 (10 s) → 19.95 mbar (12 s) = **leak at the new connections**. |
| 09.10. 15:59 | Resealed. **Run 2** (settling 60 s): plateau 31.02–31.05 mbar, after 60 s 29.75 mbar → **practically tight** (~1 mbar drops right after the pump stops = flow component, then almost nothing). |
| 09.10. ~16:00 | **Dipstick not reachable.** Delivery balance instead: 1,500 l into an "empty" tank (burner had stopped), ~35 l consumption → at least ~1,465 l. Measured without correction only 36.1 cm ≈ 1,184 l → **the line end sits above the tank bottom**. |
| 09.10. 16:06 | Firmware: adjustable correction **"line end above bottom"**, default **6.5 cm** = minimum (suction pipe assumed 3 cm above the bottom). |
| 09.10. 16:07 | **Automatic measurement switched on.** Check run: plateau 31.10, after 10 s 30.09 mbar → **43.0 cm ≈ 1,516 l**. |
| 09.10. 19:35 | Firmware: **median of 15 readings** + *measurement spread* sensor. Chip noise 0.04–0.07 mbar; run to run up to ~18 l (19:38–19:43: 1,538.6 / 1,545.7 / 1,529.2 / 1,528.0 l) → smoothing in HA over 4 measurements. |
| 09.10. | **Old gauge defective:** ~800 l without pressure, just under 1,900 l when pumped, with ~1,500 l actually in the tank. |
