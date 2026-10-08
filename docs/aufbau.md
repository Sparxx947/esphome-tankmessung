🇬🇧 [English version](aufbau.en.md)

# Aufbau und Inbetriebnahme (am Tisch)

Grundlage: [`plaene/tank-bestueckung.pdf`](../plaene/tank-bestueckung.pdf) (Draufsicht 2:1) und
[`plaene/tankmessung-schaltplan.pdf`](../plaene/tankmessung-schaltplan.pdf). Pinbelegung: [README, Abschnitt 4](../README.md#4-pinbelegung-und-verdrahtung).

## 1. Vorbereiten

1. Box und Deckel drucken (`gehaeuse/tank_box.stl`, `tank_deckel.stl`; PETG oder PLA, 0,2 mm, ohne Stützen).
2. Pumpe: rote und schwarze Litze an die Lötfahnen löten (rot = +).
3. Freilaufdiode 1N5819 bereitlegen – sie kommt **mit in die OUT-Klemmen** des MOSFET-Moduls, Strich (Kathode) an OUT+.
4. Firmware vorher flashen (siehe README, Abschnitt 6) – im eingebauten Zustand ist der USB-Port zwar erreichbar, aber eng.

## 2. Bestücken (Reihenfolge laut Bestückungsplan)

1. **Dupont-Kabel zuerst** an ESP32 und HX710B stecken – unter den Platinen ist später kein Platz für Finger.
2. **ESP32** auf die 4 Stützen legen, USB-C links in die Wandöffnung. Pigtail an U.FL, SMA-Buchse in die vordere Wand rechts neben dem Trennsteg.
3. **HX710B** mit Heißkleber auf seine 2 Stützen, Stiftleiste nach **vorn**, Stutzen nach **oben**.
4. **MOSFET-Modul** vorn rechts mit 1 Kabelbinder, Klemmen zur Mitte. Diode 1N5819: Strich an OUT+.
5. **Pumpe** hinten mit 2 Kabelbindern, Stutzen nach rechts. Blasender Stutzen → Rückschlagventil (Pfeil zum T), **Ansaugstutzen offen** lassen.
6. **Rückschlagventil** rechts mit 1 Kabelbinder, darunter das Aquarium-T: ein Abgang zum HX710B-Stutzen (2,5-mm-Silikon), einer durch die rechte Wand zur Messleitung.
7. Kabel aufräumen, Deckel aufstecken.

## 3. Inbetriebnahme

| Schritt | Erwartung | Wenn nicht |
|---|---|---|
| USB-Netzteil (≥ 1 A) anstecken | Gerät „Öltank“ in HA online, `sensor.oltank_wlan_signal` hat einen Wert | Fallback-Hotspot `Tank-Fallback` → Captive Portal |
| ≥ 5 min warten | Sensor warm (Nullpunkt driftet in den ersten Minuten ~0,5 mbar) | – |
| Schlauchende offen, `button.oltank_messung_starten` | Pumpe läuft 30 s hörbar, am Schlauchende bläst es; danach `sensor.oltank_druck` ≈ 0 mbar | Fehlerbild „Pumpe läuft nicht“ in [fehlersuche.md](fehlersuche.md) |
| Schlauchende 10 cm in ein Wasserglas | perlt; Druck ≈ 9,8–10,5 mbar | siehe [einmessen.md](einmessen.md) |

> ⚠️ **Nie mit geschlossenen Schlauchenden pumpen.** Die Pumpe schafft 80–120 kPa, der Sensor verträgt nur 0–40 kPa.
> Beim Testen immer ein offenes Ende oder eine Wassersäule, in die es ausperlen kann.

Ergebnis am 08.10.2026: in der Box Funktion ✔ (10,44/10,53 mbar bei 10 cm Wasser, 10 s Ruhe, 3,5 min nach dem Einschalten).
