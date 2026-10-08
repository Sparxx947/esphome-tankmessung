🇬🇧 [English version](verlauf.en.md)

# Projektverlauf

| Datum | Ereignis |
|---|---|
| 03./04.10.2026 | Viessmann-Störung D1 (Brennerstörung) – Tank leer, niemand hat es bemerkt. Alte pneumatische Anzeige stand trotzdem bei ~800 l, auch nach dem Pumpen → Messleitung vermutlich verschlammt. |
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
| 10.10. (geplant) | Einbau am Tank, erster Lauf, Peilstab-Abgleich. |
