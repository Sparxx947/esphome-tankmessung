🇬🇧 [English version](verlauf.en.md)

# Projektverlauf

| Datum | Ereignis |
|---|---|
| 03./04.10.2026 | Viessmann-Störung D1 (Brennerstörung) – Tank leer, niemand hat es bemerkt. Alte pneumatische Anzeige stand trotzdem bei ~800 l, auch nach dem Pumpen → damals für verschlammte Leitung gehalten (am 09.10. widerlegt: ~800 l ist die Ruhestellung des defekten Manometers). |
| 04.10. | Tankdaten aus den TÜV-Unterlagen: 7.000 l, DIN 6608-D, Baujahr 1967, Stahl, unterirdisch, Doppelwand + Leckanzeiger, Grenzwertgeber; Prüfungen 2019 und 2024 ohne Mängel, nächste 01/2029. Maße Ø 1,6 × 3,75 m aus der DIN-Tabelle. |
| 04.10. | Entscheidung für Weg B (direkte pneumatische Messung an der vorhandenen Leitung) mit ESP32 + HX710B + Mini-Pumpe; Spar-Variante mit Messing-Tüllen-T statt Klemmring-Teilen. Warenkorb bestellt. YAML und Gehäuse (Innenhöhe 30) vorbereitet. |
| 05.10. | 1.500 l Heizöl geliefert, alte Anzeige danach 1.900 l. Brenner läuft nach Entlüften wieder. Messing-T „konnte nicht versandt werden“. |
| 06.10. ~20:00 | Zweiter ESP32 geflasht (115200 Baud, 460800 brach ab), .194, in HA als „Öltank“ (12 Entitäten), feste IP, im ESPHome Builder online. |
| 06.10. abends | D4184-MOSFET-Modul als untauglich für 5 V erkannt → CQUANZX Dual-MOSFET + 1N5819 bestellt. Schaltplan neu gezeichnet und gedruckt. |
| 07.10. | Lieferung: CQUANZX-Modul, Diodensortiment. |
| 08.10. ~14:30 | Gehäuse vor dem Druck korrigiert: ESP-Stützen zwischen den Stiftreihen, SMA neben das ESP-Fach, Laschen nach gemessenen Maßen (MOSFET 35 × 17,2 × 14,2, Pumpe Ø 9,95 × 38), HX710B auf 2 Stützen, Innenhöhe 40. Messing-T nachbestellt. |
| 08.10. ~14:55 | Box gedruckt. |
| 08.10. 15:21–15:35 | Erster Pumpentest: Pumpe lief nicht (Klemmkontakt vermutet), nach Nachklemmen läuft sie. Nullpunkt wanderte. |
| 08.10. ~16:25 | **Eingemessen** mit 10 cm Wassersäule: `roh_null` −2.788.747, `roh_pro_mbar` 70.056, Pumpe 70 → 85 %. Störung war ein Leck am Anzeige-Abzweig. OTA über den Builder. |
| 08.10. 16:27 | Gegenprobe 10,01/10,02 mbar ✔. |
| 08.10. ~17:40 | Bestückungsplan erstellt und gedruckt. |
| 08.10. 18:07–18:15 | Box bestückt: Funktion ✔, Dichtprobe 60 s – ein Abfall (ungeklärt), zwei Läufe dicht. Beruhigungszeit zurück auf 10 s. |
| 08.10. ~18:30 | Frage Freiblasen in Eigenregie; AwSV-Recherche: eher fachbetriebspflichtig, Empfehlung Fachbetrieb. |
| 09.10. ~15:44 | **Einbau am Tank** (vorgezogen vom 10.10.). Box an der Wand, WLAN −61 dBm (später −50 dBm). Messing-T eingesetzt, Abzweig zur alten Anzeige dicht. Leitung nicht freigeblasen. |
| 09.10. 15:52 | Firmware: Druck wird **während** des Pumpens alle 0,5 s gelesen, **Überdruck-Abschaltung** (Grenze einstellbar, Standard 150 mbar), Höchstdruck + Abbruch-Melder. Grund: vorher lief die Pumpe stur 30 s – gegen eine verstopfte Leitung hätte das den Sensor überlastet. |
| 09.10. 15:53 | **Lauf 1** (Grenze 50 mbar zur Sicherheit): linearer Anstieg ~7 mbar/s, ab 15:53:43 **Plateau 30,95 mbar flach über 25 s Pumpen** = Luft perlt aus → **Leitung frei**, Freiblasen unnötig. Nach Pumpenstopp Abfall 30,9 → 21,4 (10 s) → 19,95 mbar (12 s) = **Leck an den neuen Anschlüssen**. |
| 09.10. 15:59 | Neu abgedichtet. **Lauf 2** (Beruhigung 60 s): Plateau 31,02–31,05 mbar, nach 60 s 29,75 mbar → **praktisch dicht** (~1 mbar fällt direkt nach Pumpenstopp = Strömungsanteil, danach fast nichts). |
| 09.10. ~16:00 | **Peilstab nicht erreichbar.** Lieferbilanz statt Peilung: 1.500 l in einen „leeren“ Tank (Brenner stand), ~35 l Verbrauch → mindestens ~1.465 l. Gemessen ohne Korrektur nur 36,1 cm ≈ 1.184 l → **das Leitungsende sitzt über dem Tankboden**. |
| 09.10. 16:06 | Firmware: einstellbare Korrektur **„Leitungsende über Boden“**, Standard **6,5 cm** = Mindestwert (Saugrohr 3 cm über Boden angenommen). |
| 09.10. 16:07 | **Automatische Messung eingeschaltet.** Kontrolllauf: Plateau 31,10, nach 10 s 30,09 mbar → **43,0 cm ≈ 1.516 l**. |
| 09.10. 19:35 | Firmware: **Median aus 15 Einzelwerten** + Sensor *Messstreuung*. Chip-Rauschen 0,04–0,07 mbar; Lauf-zu-Lauf aber bis ~18 l (19:38–19:43: 1.538,6 / 1.545,7 / 1.529,2 / 1.528,0 l) → Glättung in HA über 4 Messungen. |
| 09.10. | **Alte Anzeige defekt:** drucklos ~800 l, gepumpt knapp 1.900 l bei tatsächlich ~1.500 l. |
