🇩🇪 [Deutsche Version](verlauf.md)

# Project history

| Date | Event |
|---|---|
| 03/04.10.2026 | Viessmann fault D1 (burner fault) – tank empty, nobody noticed. The old pneumatic gauge nevertheless stood at ~800 l, even after pumping → measuring line probably silted up. |
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
| 10.10. (planned) | Installation at the tank, first run, dipstick comparison. |
