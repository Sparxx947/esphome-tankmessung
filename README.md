🇬🇧 [English version](README.en.md)

# Tankmessung – pneumatische Füllstandsmessung am Öltank

ESP32 + ESPHome misst den Füllstand des Heizöl-Erdtanks über die **vorhandene pneumatische Messleitung**
und meldet Druck, Füllhöhe und Literinhalt an Home Assistant (Gerät „Öltank“).

> Stand: **08.10.2026 abends**. Am Tisch eingemessen, Box gedruckt, bestückt und dicht.
> Der Einbau am Tank ist für das Wochenende 10./11.10.2026 geplant und hängt daran, dass die Messleitung frei ist.

> **Nachbauen?** Die Werte in diesem Repo gehören zu *diesem* Tank und *diesem* Sensor:
> - Eigene `secrets.yaml` aus [`firmware/secrets.example.yaml`](firmware/secrets.example.yaml) anlegen (WLAN, API-Schlüssel, Passwort des Fallback-Hotspots).
> - Die Tankgeometrie-Substitutions `tank_radius_dm`, `tank_laenge_dm` und `tank_nenn_l` sowie die Öldichte (`oel_mbar_pro_cm`) an den eigenen Tank anpassen.
> - `roh_null` und `roh_pro_mbar` selbst einmessen (siehe [docs/einmessen.md](docs/einmessen.md)) – die Werte in der Firmware gelten nur für genau diesen HX710B-Sensor.

---

## 1. Kurzbeschreibung

| | |
|---|---|
| **Was** | Füllstand des Heizöltanks (Druck in mbar → Füllhöhe in cm → Inhalt in Litern) |
| **Tank** | Stahl-Erdtank, draußen unterirdisch, **7.000 l**, DIN 6608-D, Baujahr 1967, doppelwandig mit Leckanzeiger. Maße laut DIN-6608-Tabelle (heutige Norm): **Ø 1.600 mm × 3.750 mm** – die Normfassung von 1967 ist nicht gegengeprüft. |
| **Wo** | Heizungskeller, an der Wand neben der alten pneumatischen Anzeige (Skala 0–7.000 l mit Zugpumpe). Abgriff: senkrechtes Kupferstück (6 mm) zwischen Abscheiderbecher und alter Anzeige. |
| **Prinzip** | Wie die alte Anzeige („Vor dem Ablesen pumpen“): Eine Mini-Pumpe drückt Luft in die Messleitung, bis sie am Tankboden ausperlt. Nach dem Abschalten hält ein Rückschlagventil die Luft in der Leitung; der Restdruck entspricht der Ölsäule über dem Leitungsende. Ein Drucksensor (HX710B, 0–40 kPa) misst ihn. |
| **Physik** | Heizöl EL ρ ≈ 0,84 kg/l → **1 cm Öl ≈ 0,824 mbar**, voller Tank (160 cm) ≈ **132 mbar**, 1 m Öl ≈ 82 mbar. |
| **Volumen** | Liegender Zylinder (Kreisabschnitt), Böden vernachlässigt, auf 7.000 l skaliert (Formel in [docs/einmessen.md](docs/einmessen.md)). |

Die alte Anzeige bleibt erhalten und funktionsfähig. Ergänzend gibt es das Projekt „Heizung über Optolink“
(zweiter ESP32, `heizung-optolink`, .193) für Brennerstunden und Störmeldungen – nicht Teil dieses Repos.

---

## 2. Status (Stand 08.10.2026)

| Bereich | Status | Datum / Hinweis |
|---|---|---|
| Firmware geflasht, in HA, im ESPHome Builder | ✅ fertig | 06.10.2026 ~20:00 |
| Feste IP in der FRITZ!Box (.194) | ✅ fertig | 06.10.2026 |
| MOSFET-Modul: D4184 als untauglich erkannt, durch CQUANZX Dual-MOSFET ersetzt | ✅ fertig | erkannt 06.10., geliefert 07.10. |
| Gehäuse korrigiert (Stützen, SMA-Lage, Laschen, HX710B-Stützen, Innenhöhe 40) | ✅ fertig | 08.10.2026 |
| Gehäuse gedruckt und bestückt, Bestückungsplan gedruckt | ✅ fertig | 08.10.2026 |
| Erster Pumpentest | ✅ läuft (nach Nachklemmen) | 08.10.2026 15:27 |
| **Einmessen am Tisch** (Wassersäule 10 cm) | ✅ fertig | 08.10.2026 16:25, Gegenprobe 16:27 |
| Funktion + Dichtprobe in der Box (60 s) | ✅ dicht (2 von 3 Läufen, ein Abfall ungeklärt) | 08.10.2026 18:07–18:15 |
| Messing-T 6×4×6 | ⏳ nachbestellt | 08.10.2026 (erste Lieferung wurde nicht versandt) |
| **Messleitung frei?** | ❌ offen – vermutlich verschlammt | Freiblasen: Fachbetrieb empfohlen (AwSV, siehe [docs/einbau.md](docs/einbau.md#awsv-wer-darf-was)) |
| Einbau am Tank, erster Lauf, Peilstab-Abgleich | ⏳ geplant | Termin Sa 10.10.2026 10:00 (Jens, zusammen mit Claude) |
| Automatische Messung (alle 6 h) | ⏸ aus | erst nach Einbau + Abgleich einschalten |
| HA-Automationen (Warnung, Prognose) | ❌ offen | noch keine angelegt (geprüft 08.10.: keine Automation/kein Skript nutzt das Gerät) |

---

## 3. Stückliste

Quelle: Projektnotizen und Werkstattbuch. Preise zum Bestellzeitpunkt (Oktober 2026, Amazon.de).
Der erste Warenkorb für die Pneumatik (8 Artikel, 54,62 €) wurde am 04.10.2026 bestellt.

### Elektronik

| Teil | Menge | Bezeichnung / Typ | Bezugsquelle, ASIN, Preis | Status |
|---|---|---|---|---|
| Mikrocontroller | 1 | ESP32-WROOM-32U DevKitC V4, USB-C, mit Antennen-Kit (U.FL→SMA-Pigtail + 2,4-GHz-Antenne), Board `esp32dev`, CP2102 | Amazon B0F6567LB5, 13,99 € je Stück (2 bestellt; das zweite steckt im Optolink-Projekt) | ✅ vorhanden, geflasht |
| Drucksensor | 1 (von 3) | Drucksensor-Modul 0–40 kPa mit HX710B (24 bit), Schlauchstutzen für 2,5-mm-Schlauch | Amazon B0B1TZH7RR, 10,99 € (3 Stück) | ✅ vorhanden, eingebaut |
| Luftpumpe | 1 | Mini-Membranpumpe „M20“, DC 3–3,7 V, 80–120 kPa; abgeflachter N20-Motor, 9,95 mm (flache Seiten) × 38 mm, 2 Stutzen stirnseitig, Lötfahnen hinten | Amazon B0GQ3MWP3R, 6,89 € (nur 2 Bewertungen) | ✅ vorhanden, eingebaut |
| MOSFET-Modul | 1 (von 5) | Dual-MOSFET-Triggermodul 15 A / 400 W („XY-MOS“, 2× AOD4184A parallel, **ohne** Optokoppler), Trigger 3,3–20 V, Last 5–36 V, PWM 0–20 kHz, 35 × 17,2 × 14,2 mm | Amazon CQUANZX B07VRCXGFY, 8,49 € (5 Stück) | ✅ geliefert 07.10., eingebaut |
| Freilaufdiode | 1 | Schottky 1N5819 | Diodensortiment BOJACK B07YK3XMQQ, 10,99 € | ✅ geliefert 07.10., eingebaut |
| ~~MOSFET-Modul D4184~~ | – | DollaTek „D4184 MOSFET-Modul“ (PC817-Optokoppler, Gate aus der Lastspannung) – **Fehlkauf, schaltet an 5 V nicht** | Amazon B07HBVTWMY, 5,99 € (5 Stück) | ⚠️ ungenutzt; stornieren oder behalten: Jens entscheidet |
| Kabel | ca. 8 | Dupont-Jumper F2F/M2F (ELEGOO-Set, 20 cm) | vorhanden (gekauft 2023) | ✅ vorhanden |
| Netzteil | 1 | USB-C-Netzteil **≥ 1 A**, 5 V | in den Notizen nicht festgehalten | ❓ ungeklärt |

### Pneumatik

| Teil | Menge | Bezeichnung / Typ | Bezugsquelle, ASIN, Preis | Status |
|---|---|---|---|---|
| T-Stück Messleitung | 1 | Messing-Schlauchtülle-T **6 × 4 × 6 mm** (6 mm Durchgang, 4 mm Abzweig) | Amazon B0GHMXRYNT, 5,99 € (2 Stück) | ⏳ erste Bestellung 04.10. nicht versandt; **nachbestellt 08.10.** |
| Silikonschlauch 6 mm innen | 1 m | Silikonschlauch 6 mm ID (auf die durchtrennte 6-mm-Kupferleitung) | Amazon B0CYGQD96H, 5,59 € | bestellt 04.10. (Lieferung nicht ausdrücklich notiert) |
| Schlauchschellen | 10 | Edelstahl-Schlauchschellen 6–12 mm (Leryati) | Amazon B0C24792WR, 4,99 € | bestellt 04.10. (Lieferung nicht ausdrücklich notiert) |
| Aquarium-Set | 1 | 48-teilig: 6 m Silikonschlauch 4 mm, Rückschlagventile, T- und L-Verbinder | Amazon B0C2PYBDGJ, 9,99 € | ✅ vorhanden, in der Box verbaut (Rückschlagventil + T) |
| Silikonschlauch 2,5 mm | 1 m | Silikonschlauch 2,5 mm ID × 4 mm AD – passt auf den Sensorstutzen und stramm in den 4-mm-Aquariumschlauch | Amazon B0CXPW74GZ, 4,19 € | bestellt 04.10. (Lieferung nicht ausdrücklich notiert) |
| Messleitung | – | vorhandene Kupferleitung **6 mm außen** (Jens gemessen 6,1 mm) vom Tankboden in den Keller | Bestand | ⚠️ vermutlich verschlammt |

Fallback, falls das Messing-T wieder ausfällt: Steckverbinder-T 6-4-6 POM (B0GLGCTVRH) oder PA (B0CB8V2NXD).
Ungeprüft, ob Steckverbinder auf 6,1-mm-Kupfer dicht und zugfest halten – vor dem Einbau Zugtest + Druckhaltetest.

### Gehäuse und Kleinteile

| Teil | Menge | Bezeichnung / Typ | Bezugsquelle | Status |
|---|---|---|---|---|
| Filament | ca. 1 Box + Deckel | PETG oder PLA (Raumtemperatur, Wandmontage) | Bestand | ✅ Box gedruckt 08.10. (Material nicht notiert) |
| Kabelbinder | 4 | schmal, passend für Schlitze 3,5 × 1,8 mm (2× Pumpe, 1× MOSFET, 1× Ventil) | Bestand | ✅ (Bestand nicht ausdrücklich notiert) |
| Heißkleber | – | HX710B auf seine 2 Stützen | Bestand | ✅ |
| Wandschrauben + Dübel | 4 | für Laschen Ø 4,5 mm (also Schrauben ≤ 4 mm) | – | ❓ nicht in den Notizen |
| Magnete | 0 | – (die 10 × 3-mm-Magnete gehören zum Optolink-Gehäuse) | – | – |
| Widerstände | 0 | Die Schaltung braucht keine (HX710B-Modul und MOSFET-Modul sind fertig bestückt). | – | – |

### Werkzeug / Hilfsmittel

Messschieber, Multimeter, Lötkolben, 3D-Drucker, Glas mit Wasser + Lineal (Einmessen),
Peilstab für den Domschacht (ggf. mit Wasserfindungspaste) – **Peilstab noch offen**.

---

## 4. Pinbelegung und Verdrahtung

Schaltplan: [`plaene/tankmessung-schaltplan.pdf`](plaene/tankmessung-schaltplan.pdf)
(Quelle `plaene/tank_plan.py`, Vorschau `plaene/tank_plan.svg`).
Bestückung der Box: [`plaene/tank-bestueckung.pdf`](plaene/tank-bestueckung.pdf) (Quelle `plaene/tank_bestueckung_plan.py`).

> Der Schaltplan-PDF ist auf Stand **08.10.2026** (85 % PWM, eingemessene Werte). Die SVG-Fassung `tank_plan.svg` zeigt noch den Stand 06.10.; die Verdrahtung ist identisch.

| Von | Nach | Hinweis |
|---|---|---|
| HX710B **VCC** | ESP32 **3V3** | **nicht** an 5 V – sonst 5-V-Pegel an GPIO19 |
| HX710B **GND** | ESP32 GND | gemeinsame Masse |
| HX710B **OUT** | **GPIO19** | ESPHome-Plattform `hx711` (`dout_pin`) |
| HX710B **SCK** | **GPIO18** | `clk_pin`, Gain 128 |
| MOSFET **TRIG/PWM** | **GPIO25** | LEDC-PWM 20 kHz |
| MOSFET **GND** (Steuerseite) | ESP32 GND | |
| MOSFET **VIN+** | ESP32 **5V** | 5 V vom DevKit (aus USB, Netzteil ≥ 1 A) |
| MOSFET **VIN−** | ESP32 GND | |
| MOSFET **OUT+** | Pumpe **+ (rot)** | |
| MOSFET **OUT−** | Pumpe **− (schwarz)** | Modul schaltet **Minus** – Pumpe nur an OUT+/OUT−, nie zwischen VIN− und GND |
| 1N5819 | parallel zur Pumpe | **Strich (Kathode) an OUT+**; mit in die Klemmen |
| Antenne | U.FL am Modul → Pigtail → SMA-Buchse in der Vorderwand | Das WROOM-**32U** hat keine Leiterplattenantenne |

Auf der Modul-Unterseite (XY-MOS, laut Foto 08.10.): OUT+ unten, OUT− oben, VIN rechts. Aufdruck auf dem Modul gilt.

**Schlauchführung:**

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

---

## 5. Gehäuse

Quelle: [`gehaeuse/tankmessung-gehaeuse.scad`](gehaeuse/tankmessung-gehaeuse.scad) (OpenSCAD, Variable `TEIL = "box" | "deckel" | "alle"`).

| Datei | Wofür | Maße |
|---|---|---|
| `gehaeuse/tank_box.stl` | Box mit ESP-Fach, Stützen, Kabelbinder-Schlitzen, 4 Wandlaschen | außen 114 × 68 × 42 mm (+ Laschen auf 84 mm Breite), innen 110 × 64 × 40 mm |
| `gehaeuse/tank_deckel.stl` | Steckdeckel mit 3-mm-Rand und Ø-3-mm-Loch über der ESP-Status-LED | 114 × 68 × 4,8 mm |
| `gehaeuse/vorschau_tank.png`, `vorschau_tank_oben.png` | Vorschaubilder | – |

**Material/Druck:** PETG oder PLA, 0,2 mm Schicht, **ohne Stützen**, Boden aufs Bett (Beschriftung „TANKMESSUNG“ ist gespiegelt in den Boden eingelassen).

**Aufteilung (Draufsicht, vorne = Wand mit SMA-Buchse):**

| Bereich | Bauteil | Befestigung |
|---|---|---|
| links (x 2–53) | ESP32 DevKitC, USB-C durch die linke Wand | liegt auf **4 Stützen** (17 mm hoch, je ~4,9 mm breit), Stifte + Dupont nach **unten** |
| Trennsteg x ~53 | 6 mm niedriger Anschlag, Kabel gehen drüber | – |
| vorne, x 62 | SMA-Buchse Ø 6,6 mm, 8 mm über dem Boden | Mutter |
| vorne rechts (x 74–109) | MOSFET-Modul, Klemmen zur Mitte | 1 Kabelbinder |
| Mitte (x ~71–89) | HX710B, Stiftleiste nach vorn/unten, Stutzen nach oben | **Heißkleber** auf 2 Stützen (17 mm) unter den Ohren |
| hinten (x 57–95) | Pumpe längs, Lötfahnen links, Stutzen rechts | 2 Kabelbinder |
| rechts | Rückschlagventil, darunter Aquarium-T | 1 Kabelbinder |
| rechte Wand | Schlauch Ø 6,6 mm unten, optionale Kabeldurchführung Ø 5 mm oben | – |
| Rückwand | 8 Lüftungsschlitze | – |

**Lehren aus dem Gehäusebau** (alle vor dem Druck am 08.10. korrigiert):

- **Stiftleisten laufen über die ganze Platinenlänge** (19 × 2,54 mm). Durchgehende Stirn-Auflagen hätten an beiden Enden auf den Stiften gesessen → 4 Einzelstützen, 3,2 mm vom Längsrand, Mitte 12 mm frei (USB-Lötlaschen).
- **SMA-Mutter traf die Stifte**: Bohrung unter der Platine (x 39,5) kollidierte mit der vorderen Stiftleiste → nach x 62 rechts neben das ESP-Fach.
- **Pumpenlaschen lagen quer** zur Pumpe und das MOSFET-Modul ragte 4 mm über die Wand → Laschen nach Jens' Maßen neu gesetzt, Hüllquader-Kollisionsprüfung.
- **HX710B hat die Stiftleiste nach unten** → steht auf Stützen, Innenhöhe 30 → 40 mm (Platz für Stutzen + Schlauchbogen); Dupont ↔ Stützen 1,1/1,4 mm Luft.
- Allgemein: **vor jedem STL-Export Kollisionen prüfen** (Stifte, Muttern, Stecker), Teile vorher mit dem Messschieber messen.
- Die Lochlinie der HX710B-Ohren ist nur aus einem Foto geschätzt – deshalb Heißkleber statt Schrauben.

Ältere Stände liegen lokal als `*.vor-stuetzen-20261008`, `*.vor-laschen-20261008` (per `.gitignore` nicht im Repo).

---

## 6. Firmware

Datei: [`firmware/tankmessung.yaml`](firmware/tankmessung.yaml) – Stand aus dem ESPHome Builder (08.10.2026).
**Die Fassung im ESPHome Builder ist führend**; Änderungen hier nachziehen.

| Einstellung | Wert |
|---|---|
| Gerätename / Hostname | `tankmessung` / `tankmessung.local` |
| Anzeigename in HA | **Öltank** |
| IP | **192.168.178.194** (feste Zuordnung in der FRITZ!Box per MAC) |
| Board / Framework | `esp32dev`, **esp-idf** |
| Logger | INFO |
| API | verschlüsselt (`!secret tank_api_key`), OTA ohne eigenes Passwort |
| Fallback-Hotspot | `Tank-Fallback` + Captive Portal (Passwort `!secret tank_ap_password`) |

**Substitutions:**

| Name | Wert | Bedeutung |
|---|---|---|
| `roh_null` | `-2788747.0` | HX710B-Rohwert bei 0 mbar (eingemessen 08.10., Sensor warm) |
| `roh_pro_mbar` | `70056.0` | Rohwert-Anstieg je mbar |
| `oel_mbar_pro_cm` | `0.824` | Heizöl EL, ρ ≈ 0,84 |
| `tank_radius_dm` | `8.0` | Ø 1,6 m |
| `tank_laenge_dm` | `37.5` | 3,75 m |
| `tank_nenn_l` | `7000` | Skalierung auf Nennvolumen |

**Pumpe:** `ledc` an GPIO25, 20 kHz, `max_power: 85%` (≈ 4,05 V bei 4,77 V VIN; vorher 70 %).
Die Pumpe ist für 3–3,7 V gebaut und hängt an 5 V – deshalb die Begrenzung.
**Sicherung:** Skript `pumpe_sicherung` schaltet die Pumpe nach **60 s** immer ab, auch bei Handbetrieb.

**Messablauf (Skript `messung`):** Pumpe 100 % (= 85 % PWM) für *Spülzeit* (Standard 30 s) → aus →
*Beruhigungszeit* (Standard 10 s) → HX710B lesen → 2 s → nochmal lesen. Der Sensor wird **nur** in diesem Skript gelesen
(`update_interval: never`).

### Entitäten in Home Assistant (12, geprüft 08.10.2026)

| Entität | Typ | Zweck |
|---|---|---|
| `button.oltank_messung_starten` | Knopf | eine Messung auslösen |
| `switch.oltank_automatische_messung` | Schalter (Konfig.) | Messung alle 6 h – **ab Werk AUS** (`RESTORE_DEFAULT_OFF`) |
| `number.oltank_spulzeit_pumpe` | Zahl 5–60 s | Pumpdauer je Messung (30 s) |
| `number.oltank_beruhigungszeit` | Zahl 2–60 s | Wartezeit vor dem Lesen (10 s; für Dichtproben 60 s) |
| `fan.oltank_pumpe` | Lüfter (Diagnose) | Pumpe von Hand, max. 60 s |
| `sensor.oltank_druck_rohwert` | Diagnose | HX710B-Rohwert (für das Einmessen) |
| `sensor.oltank_druck` | mbar | Druck = Ölsäule |
| `sensor.oltank_fullhohe` | cm | Füllhöhe (begrenzt auf 0–160 cm) |
| `sensor.oltank_inhalt` | L | Inhalt, `device_class: volume_storage` |
| `sensor.oltank_wlan_signal` | dBm | am 08.10. −42 dBm |
| `sensor.oltank_laufzeit` | s | Uptime |
| `button.oltank_neustart` | Knopf (Diagnose) | ESP neu starten |

### Secrets

`firmware/secrets.example.yaml` ist nur eine Vorlage mit Platzhaltern. Die echten Werte (`wifi_ssid`, `wifi_password`,
`tank_api_key`, `tank_ap_password`) stehen **nur im ESPHome Builder** (und lokal außerhalb des Repos, Rechte 600).
`.gitignore` schließt `secrets.yaml` und `secrets.*.yaml` aus. API-Schlüssel neu erzeugen: `openssl rand -base64 32`.

### Flashen

| Weg | Wann | Wie |
|---|---|---|
| **OTA über den ESPHome Builder** (Normalfall) | jede Änderung | YAML im Builder bearbeiten → *Install* → *Wirelessly*. Gerät ist seit 06.10. ~20:05 im Builder online. |
| **Erstflash per USB** | neues Board / kaputte Firmware | `esphome run tankmessung.yaml --no-logs --device /dev/ttyUSB0` mit **echten** Secrets. Port vorher freigeben (`setfacl -m u:$USER:rw /dev/ttyUSB0`, nach jedem Umstecken neu) oder Gruppe `dialout`. |
| **Notweg bei Abbruch** | „No more data to read“ | Dieses Board kam mit 460800 Baud nicht klar: mit `esptool … --baud 115200` die fertige `firmware.factory.bin` schreiben. |

> ⚠️ **Falle:** Nie einen Prüf-Build mit Dummy-Secrets flashen (am 06.10. beim Schwestergerät passiert: falsches
> Hotspot-Passwort, falscher API-Schlüssel). `esphome upload` **übersetzt nicht neu** und spielt blind den letzten Build auf –
> für echte Firmware immer `esphome run` und auf „Successfully compiled“ achten. Danach per API mit dem echten Schlüssel gegenprüfen.

---

## 7. Anleitungen

| Anleitung | Inhalt |
|---|---|
| [docs/aufbau.md](docs/aufbau.md) | Aufbau und Inbetriebnahme auf dem Tisch |
| [docs/einmessen.md](docs/einmessen.md) | **Einmessen/Kalibrieren** mit Wassersäule, Formeln, Peiltabelle, Abgleich am Tank |
| [docs/einbau.md](docs/einbau.md) | Einbau am Tank, Freiblasen der Messleitung, AwSV, erster Lauf, Dichtprobe |
| [docs/fehlersuche.md](docs/fehlersuche.md) | bekannte Fehlerbilder mit Ursache und Lösung |
| [docs/verlauf.md](docs/verlauf.md) | Projektverlauf 04.–08.10.2026 |

Kurzfassung:

1. **Aufbau** nach `plaene/tank-bestueckung.pdf` (Dupont zuerst stecken, dann ESP auf die Stützen).
2. **Inbetriebnahme:** USB-Netzteil an, Gerät in HA online? „Messung starten“ mit offenem Schlauch → Pumpe läuft, bläst.
3. **Einmessen:** Nullpunkt bei offenem Schlauch (Sensor warm, ≥ 5 min nach Einschalten), dann 10 cm Wassersäule = 9,81 mbar →
   `roh_pro_mbar = (roh_10cm − roh_null) / 9,81`. Gegenprobe muss ~10 mbar ergeben.
4. **Einbau:** nur an eine **freie** Messleitung; Abzweig zur alten Anzeige dauerhaft dicht.
5. **Test:** erster Lauf mit 60 s Beruhigungszeit (Dichtprobe), dann Peilstab-Abgleich, dann Beruhigungszeit 10 s.
6. Erst dann **„Automatische Messung“** einschalten.

---

## 8. Home-Assistant-Anbindung

- Integration: **ESPHome**, Gerät „Öltank“, 12 Entitäten (Tabelle oben).
- Es gibt **noch keinen `ha/`-Ordner** und keine Automationen/Skripte, die das Gerät nutzen (Suche in HA am 08.10.2026).
- Geplant (aus den Notizen):
  - **Warnung bei niedrigem Stand:** Vorwarnung 1.500 l, dringend 800 l (Push an die Hausbewohner).
  - **Tankprognose** aus dem Verbrauch; Abgleich mit dem Ölverbrauch aus Brennerstunden × Düsendurchsatz (≤ 2,4 l/h) vom Optolink-Projekt.
  - Plausibilität gegen Liefermengen (Referenz: 3.000 l reichten ~14 Monate).
- Hinweis für Automationen: Die Sensoren ändern sich nur nach einer Messung; bei abgeschalteter Automatik bleibt der letzte Wert stehen.

---

## 9. Offene Punkte / nächste Schritte / Termine

| Punkt | Wer | Termin |
|---|---|---|
| Messing-T 6×4×6 (nachbestellt) abwarten | Jens | Lieferung offen |
| **Messleitung freiblasen** – Fachbetrieb (empfohlen, mit Tankreinigung + Grenzwertgeber-Tausch) oder selbst (rechtlich unklar, siehe AwSV) | Jens entscheidet | vor dem Einbau |
| Einbau am Tank, erster Lauf + 60-s-Dichtprobe, Peilstab-Abgleich | Jens + Claude | **Sa 10.10.2026 10:00** |
| Peilung im Domschacht (Erwartung bei 1.900 l ≈ 50,6 cm) | Jens | beim Einbau |
| Beruhigungszeit nach dem Test zurück auf 10 s | – | nach dem Einbau |
| Automatische Messung einschalten | – | nach dem Abgleich |
| HA: Warnung 1.500 / 800 l, Prognose | Claude | danach |
| D4184-Fehlkauf stornieren oder behalten | Jens | – |
| Ungeklärter Druckabfall im 2. Dichtlauf (18:07) beobachten | – | beim Einbau |
| Grenzwertgeber mit Lochhülse: jährliche Kontrolle durch Fachbetrieb oder Tausch gegen Schlitzhülse (TÜV-Hinweis 2019 + 2024) | Jens | mit der Tankreinigung |
| Nächste AwSV-Prüfung | Jens | 01/2029 (anmelden ab 11/2028) |

---

## 10. Dateiübersicht

```
esphome-tankmessung/
├── README.md                         diese Datei
├── README.en.md                      diese Datei auf Englisch
├── .gitignore                        schließt Secrets, Build-Ordner, Sicherungsstände aus
├── docs/
│   ├── aufbau.md                     Aufbau + Inbetriebnahme am Tisch
│   ├── einmessen.md                  Kalibrierung, Formeln, Peiltabelle
│   ├── einbau.md                     Einbau am Tank, Freiblasen, AwSV, Dichtprobe
│   ├── fehlersuche.md                Fehlerbilder
│   └── verlauf.md                    Chronik
├── firmware/
│   ├── tankmessung.yaml              ESPHome-Konfiguration (Stand Builder 08.10.2026)
│   └── secrets.example.yaml          Vorlage, keine echten Werte
├── gehaeuse/
│   ├── tankmessung-gehaeuse.scad     OpenSCAD-Quelle (Box + Deckel)
│   ├── tank_box.stl                  Box, Innenhöhe 40 (gedruckt 08.10.)
│   ├── tank_deckel.stl               Steckdeckel
│   ├── vorschau_tank.png             Vorschau
│   └── vorschau_tank_oben.png        Vorschau von oben
└── plaene/
    ├── tankmessung-schaltplan.pdf    Schaltplan + Schlauchführung (Stand 08.10.)
    ├── tank_plan.py                  Erzeuger des Schaltplans (matplotlib)
    ├── tank_plan.svg                 Schaltplan als SVG (Stand 06.10.)
    ├── tank-bestueckung.pdf          Bestückungsplan der Box, Maßstab 2:1 (Stand 08.10.)
    └── tank_bestueckung_plan.py      Erzeuger des Bestückungsplans
```

Die Erzeuger-Skripte schreiben noch auf feste Pfade außerhalb des Repos (`~/esphome/…` bzw. ein Scratchpad) – vor erneutem
Aufruf den Ausgabepfad anpassen.
