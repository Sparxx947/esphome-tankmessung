🇬🇧 [English version](einbau.en.md)

# Einbau am Tank

Geplant: **Samstag 10.10.2026, 10:00** (Jens, erster Lauf zusammen mit Claude).

## Voraussetzung: Die Messleitung muss frei sein

Die alte Anzeige stand bei leerem Tank (Störung D1 am 03./04.10.) fest bei ~800 l, auch nach dem Pumpen. Nach der Lieferung
von 1.500 l am 05.10. zeigte sie 1.900 l – sie reagiert also wieder, die Leitung ist **nicht völlig zu**, aber vermutlich
verschlammt. Am Boden des Klarsichtbechers (Abscheider in der Messleitung unter der Anzeige) lag etwas Dunkles/Rötliches –
möglicherweise Öl in der Messleitung (unbelegt).

**Frei-Kennzeichen beim ersten Lauf:** Der Druck steigt bis zur Ölsäule (~40 mbar bei ~50 cm) und bleibt stehen.
**Über ~150 mbar = Leitung zu → sofort abbrechen** (Sensorgrenze 40 kPa, Pumpe schafft 80–120 kPa).

### AwSV: wer darf was

Recherche 08.10.2026 (keine Rechtsberatung):

- Die Anlage ist **doppelt fachbetriebspflichtig** nach § 45 Abs. 1 AwSV: unterirdisch (Nr. 1) und Heizölverbraucheranlage
  Stufe B (Nr. 4; 7 m³, WGK 2). Pflichtig sind Errichten, innen Reinigen, **Instandsetzen**, Stilllegen.
- **Verschlammte Leitung wieder gängig machen** = „Wiederherstellen“ (§ 2 Abs. 29) = Instandsetzen → pflichtig, außer nach
  § 45 Abs. 2 (keine unmittelbare Bedeutung für die Anlagensicherheit). Für Füllstandsanzeiger ordnet das **keine** Quelle ein.
  → Freiblasen selbst: **unklar, eher pflichtig**.
- **T-Stück im Keller:** unklar, geringeres Risiko. Sensor/ESP: Elektro-Ausnahme nach TRwS 791 Nr. 9.1.
- **Grenzwertgeber-Tausch:** sicher pflichtig.
- Verstoß: Ordnungswidrigkeit (§ 65 Nr. 25 AwSV / § 103 WHG); laut NRW-Zweifelsfragen (2019) bei technisch einwandfreier
  Ausführung nur Ordnungsmangel. Versicherungsbedingungen (Gewässerschaden) ungeprüft.
- **Empfehlung:** Fachbetrieb bläst frei und setzt das T gleich mit (am besten zusammen mit Tankreinigung und Tausch des
  Grenzwertgebers mit Lochhülse). Sonst schriftliche Anfrage an die zuständige untere Wasserbehörde.

### Falls doch selbst freigeblasen wird (Rat vom 08.10., Entscheidung bei Jens)

1. **Heizung aus** und danach 2–3 h aus lassen – das Leitungsende liegt im Bodenschlamm, Aufwirbeln führt sonst zu Brennerstörung (Filter).
2. Alte Anzeige und Becher **abschrauben**.
3. Zuerst mit einer **Fahrrad- oder Ballpumpe** auf das 6-mm-Kupfer.
4. Kompressor nur mit **Druckminderer ≤ ~0,5 bar**, in 1–2-s-Stößen.
5. Jemand horcht am Domschacht/an der Entlüftung: **Blubbern = frei**.
6. Danach den Ölfilter am Brenner beobachten.

## Ablauf

1. **Messing-T 6×4×6** in die Kupfer-Messleitung zwischen Becher und alter Anzeige: senkrechtes Kupferstück mittig
   durchtrennen, 6-mm-Silikonschlauch auf beide Enden und die Tüllen, Schlauchschellen. Betriebsdruck max. ~0,2 bar.
   (Hinweis: Silikon quillt in Mineralöl – in Ordnung, solange nur Luft/Dunst in der Leitung ist; bei Öl lieber PU/PA-Schlauch.)
2. **Abzweig zur alten Anzeige dauerhaft dicht** anschließen. Kein Rückschlagventil als Verschluss – das leckt (Test 08.10.).
3. **Box an die Wand** (4 Laschen, Ø 4,5 mm), 4-mm-Schlauch vom T-Abzweig in die rechte Wand der Box, USB-Netzteil ≥ 1 A.
4. ≥ 5 min warten (Sensor warm).
5. **Erster Lauf** mit Vorsicht: Bei unklarer Leitung *Vorschlag (nicht erprobt):* Spülzeit erst auf 5 s stellen und den Druck
   ansehen, bevor 30 s gepumpt wird. Ergebnis über 150 mbar → abbrechen, Leitung ist zu.
6. **Dichtprobe:** `number.oltank_beruhigungszeit` auf **60 s**, „Messung starten“. Der Druck nach 60 s muss dem nach 10 s
   entsprechen. Am Tisch: 10,07 → 10,07 mbar und 10,76 / 10,74 mbar = dicht.
7. **Peilstab-Abgleich** im Domschacht (Erwartung siehe [einmessen.md](einmessen.md#3-abgleich-am-tank-nach-dem-einbau)).
8. Beruhigungszeit **zurück auf 10 s**.
9. Erst jetzt `switch.oltank_automatische_messung` **einschalten** (Messung alle 6 h).

## Nicht anfassen

- **AFRISO-Leckanzeiger** über der Anzeige (Tank doppelwandig) – Leck-Lampe war aus.
- Die alte Anzeige bleibt in Betrieb (Ablesen nach dem Pumpen mit dem schwarzen Knopf).
