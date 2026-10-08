🇩🇪 [Deutsche Version](einbau.md)

# Installation at the tank

Planned: **Saturday 10.10.2026, 10:00** (Jens, first run together with Claude).

## Prerequisite: the measuring line must be clear

With the tank empty (fault D1 on 03/04.10.) the old gauge was stuck at ~800 l, even after pumping. After the delivery
of 1,500 l on 05.10. it showed 1,900 l – so it responds again, the line is **not completely blocked**, but probably
silted up. At the bottom of the clear cup (separator in the measuring line below the gauge) there was something dark/reddish –
possibly oil in the measuring line (unconfirmed).

**Sign of a clear line on the first run:** the pressure rises to the oil column (~40 mbar at ~50 cm) and stays there.
**Above ~150 mbar = line blocked → abort immediately** (sensor limit 40 kPa, pump manages 80–120 kPa).

### AwSV: who may do what

> The AwSV (*Verordnung über Anlagen zum Umgang mit wassergefährdenden Stoffen*, German ordinance on facilities handling
> substances hazardous to water) applies to Germany only; other countries have their own rules.

Research 08.10.2026 (not legal advice):

- The installation is **doubly subject to the specialist-company requirement** under § 45 (1) AwSV: underground (no. 1) and heating-oil consumer installation
  level B (no. 4; 7 m³, WGK 2 – water hazard class 2). Subject to the requirement: erecting, cleaning the inside, **repairing**, decommissioning.
- **Making a silted-up line work again** = "restoring" (§ 2 (29)) = repairing → subject to the requirement, unless under
  § 45 (2) (no direct significance for the safety of the installation). **No** source classifies level indicators.
  → Blowing it clear yourself: **unclear, more likely subject to the requirement**.
- **T-piece in the basement:** unclear, lower risk. Sensor/ESP: electrical exemption under TRwS 791 no. 9.1.
- **Replacing the level-limit sensor (Grenzwertgeber):** definitely subject to the requirement.
- Violation: administrative offence (§ 65 no. 25 AwSV / § 103 WHG); according to the NRW FAQ (2019), if executed technically
  correctly, only a formal deficiency. Insurance terms (water damage) not checked.
- **Recommendation:** a specialist company blows the line clear and fits the T at the same time (ideally together with tank cleaning and replacement of the
  level-limit sensor with perforated sleeve). Otherwise a written enquiry to the responsible lower water authority (untere Wasserbehörde).

### If it is blown clear yourself after all (advice from 08.10., decision lies with Jens)

1. **Heating off** and leave it off for 2–3 h afterwards – the end of the line sits in the bottom sludge; stirring it up otherwise leads to a burner fault (filter).
2. **Unscrew** the old gauge and the cup.
3. First use a **bicycle or ball pump** on the 6 mm copper.
4. Compressor only with a **pressure reducer ≤ ~0.5 bar**, in 1–2 s bursts.
5. Someone listens at the manhole/vent: **bubbling = clear**.
6. Afterwards keep an eye on the oil filter at the burner.

## Procedure

1. **Brass T 6×4×6** into the copper measuring line between the cup and the old gauge: cut the vertical copper section
   in the middle, 6 mm silicone hose onto both ends and the barbs, hose clamps. Operating pressure max. ~0.2 bar.
   (Note: silicone swells in mineral oil – fine as long as there is only air/vapour in the line; with oil better use PU/PA hose.)
2. Connect the **branch to the old gauge permanently sealed**. No check valve as a plug – it leaks (test 08.10.).
3. **Box on the wall** (4 tabs, Ø 4.5 mm), 4 mm hose from the T branch into the right wall of the box, USB power supply ≥ 1 A.
4. Wait ≥ 5 min (sensor warm).
5. **First run** with caution: if the line state is unclear, *suggestion (not tested):* first set the flush time to 5 s and look at the pressure
   before pumping for 30 s. Result above 150 mbar → abort, the line is blocked.
6. **Leak test:** set `number.oltank_beruhigungszeit` (settling time) to **60 s**, `Messung starten` ("Start measurement"). The pressure after 60 s must match the one after 10 s.
   On the bench: 10.07 → 10.07 mbar and 10.76 / 10.74 mbar = tight.
7. **Dipstick comparison** in the manhole (expectation see [einmessen.en.md](einmessen.en.md#3-comparison-at-the-tank-after-installation)).
8. Settling time **back to 10 s**.
9. Only now **switch on** `switch.oltank_automatische_messung` (automatic measurement; measurement every 6 h).

## Do not touch

- **AFRISO leak detector** above the gauge (tank is double-walled) – the leak lamp was off.
- The old gauge remains in operation (read after pumping with the black knob).
