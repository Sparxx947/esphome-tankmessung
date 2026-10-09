🇬🇧 [English version](fehlersuche.en.md)

# Fehlersuche

Bekannte Fehlerbilder aus dem Projektverlauf (04.–09.10.2026).

| Fehlerbild | Ursache | Lösung | belegt? |
|---|---|---|---|
| Pumpe läuft nicht, am Modul-Ausgang nur ~0,86 V (VIN 4,77 V) | vermutlich **Klemmkontakt** am MOSFET-Modul | Litzen und Diode neu in die Klemmen, nachziehen; danach lief sie bei 70 % | Ursache **nicht** belegt (08.10. 15:21–15:33) |
| MOSFET-Modul schaltet an 5 V nicht / nur halb | **D4184-Modul mit PC817-Optokoppler**: Gate wird aus der Lastspannung über 2 × 4,7 kΩ versorgt → Gate = 50 % der Versorgung, schaltet erst ab ~6 V; PC817 zu langsam für 20 kHz; keine Freilaufdiode | Dual-MOSFET-Modul **ohne** Optokoppler (CQUANZX B07VRCXGFY) + 1N5819 | belegt (Datenblatt-Analyse + Rezensionen, 06.10.) |
| Druck baut sich nicht auf / Wert zu niedrig, sinkt | **Leck am Abzweig zur alten Anzeige**: Rückschlagventil als Verschluss leckt ab ~10 mbar | Abzweig fest verschließen; Dichtprobe mit 60 s Beruhigungszeit | belegt (08.10., zugehalten → perlt, Wert stimmt) |
| Einmaliger Abfall in der Dichtprobe (10,44 → 6,65/6,47 mbar nach 60 s) | ungeklärt – vermutlich Steckverbindungen haben sich nach dem Einbau gesetzt | Lauf wiederholen; zwei Folgeläufe waren dicht | **nicht** belegt |
| Nullpunkt wandert in den ersten Minuten (~38.500 Rohwert ≈ 0,55 mbar ≈ 7 mm Öl) | Aufwärmen des Sensors (vermutet) | vor dem Einmessen ≥ 5 min warten | Drift gemessen, Ursache vermutet |
| `binary_sensor.oltank_uberdruck_abbruch` an / Druck > Überdruck-Grenze | Messleitung zu; Pumpe drückt gegen geschlossene Leitung | Firmware schaltet die Pumpe selbst ab (seit 09.10.; Sensor nur 0–40 kPa, Pumpe 80–120 kPa); Leitung freiblasen lassen | Grenzwert aus Rechnung; Abschaltung **noch nie ausgelöst** |
| Druck fällt nach Pumpenstopp deutlich (09.10.: 30,9 → 21,4 mbar in 10 s) | **Leck an den neuen Anschlüssen** (T, Silikonschlauch, Schellen, Abzweig zur alten Anzeige) | neu abdichten; Dichtprobe mit 60 s – danach 1,3 mbar in 60 s | belegt (09.10.) |
| ~1 mbar Abfall direkt nach Pumpenstopp, danach fast nichts | kein Leck: Strömungsanteil (Druck, den die strömende Luft zusätzlich braucht) | keine | belegt (09.10.) |
| Inhalt deutlich unter der gelieferten Menge | Messleitung endet **über dem Tankboden** – Öl darunter sieht die Messung nicht | `number.oltank_leitungsende_uber_boden` setzen (siehe [einmessen.md](einmessen.md#3-abgleich-am-tank-nach-dem-einbau)) | belegt per Lieferbilanz (09.10.) |
| Pumpe gegen geschlossene Schlauchenden | Bedienfehler beim Testen | nie ohne offenes Ende / Wassersäule pumpen | Regel |
| Gegenprobe zeigt etwas über 9,81 mbar (z. B. 10,0–10,8) | Eintauchtiefe von Hand ungenau (+1 mm ≈ +0,1 mbar) | keine – Toleranz des Verfahrens | belegt |
| Flash bricht ab mit „No more data to read“ | dieses Board verträgt 460800 Baud nicht | `esptool … --baud 115200` mit `firmware.factory.bin` | belegt (06.10.) |
| Fallback-Hotspot nimmt Passwort nicht an / API-Schlüssel falsch | Prüf-Build mit Dummy-Secrets geflasht (beim Schwestergerät 06.10.) | nur `esphome run` mit echten Secrets; `esphome upload` übersetzt **nicht** neu | belegt |
| USB-Port nach Umstecken gesperrt (Linux) | `/dev/ttyUSB0` wird neu angelegt, Freigabe ist weg | `setfacl -m u:$USER:rw /dev/ttyUSB0` wiederholen oder Gruppe `dialout` | belegt |
| Werte ändern sich nicht | Sensor wird nur in der Messung gelesen (`update_interval: never`), Automatik ab Werk aus | „Messung starten“ drücken bzw. Automatik einschalten | Konfiguration |
| Alte Anzeige stand bei leerem Tank fest auf ~800 l | **Manometer defekt:** ~800 l ist seine Ruhestellung ohne Druck (nicht Schlamm – die Leitung war frei); gepumpt zeigt es knapp 1.900 l bei ~1.500 l | alte Anzeige nicht mehr verwenden; die Box ist der Maßstab | belegt (09.10.: drucklos ~800 l, Leitung frei) |

## Prüfschritte bei unplausiblen Werten

1. `sensor.oltank_druck_rohwert` ansehen: Zwei Lesungen je Messung liegen normal ~100–300 auseinander.
2. Schlauch an der Box abziehen, „Messung starten“ → Druck muss ~0 mbar sein (sonst Nullpunkt neu, siehe [einmessen.md](einmessen.md)).
3. Glas-Test mit 10 cm Wasser → ~9,8–10,5 mbar.
4. Dichtprobe mit 60 s Beruhigungszeit.
5. Erst dann die Leitung zum Tank verdächtigen.
