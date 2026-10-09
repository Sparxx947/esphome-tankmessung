🇬🇧 [English version](einmessen.en.md)

# Einmessen / Kalibrieren

Die Kette in der Firmware:

```
Rohwert (HX710B, 24 bit)  →  Druck p [mbar]  →  Füllhöhe h [cm]  →  Inhalt V [l]
```

## 1. Formeln

| Schritt | Formel | Konstante |
|---|---|---|
| Rohwert → Druck | `p = (roh − roh_null) / roh_pro_mbar` | `roh_null = −2.788.747`, `roh_pro_mbar = 70.056` |
| Druck → Füllhöhe | `h = p / 0,824` (begrenzt auf 0 … 160 cm) | Heizöl EL ρ ≈ 0,84 kg/l: 0,84 × 9,81 × 0,01 / 100 ≈ 0,824 mbar/cm |
| Füllhöhe → Inhalt | Kreisabschnitt `A = r²·acos((r−h)/r) − (r−h)·√(2rh − h²)` mit h in dm, `V = A · L · 7000 / (π·r²·L)` | r = 8 dm, L = 37,5 dm (Böden vernachlässigt, auf 7.000 l skaliert) |
| Wasser zum Einmessen | 10 cm Wassersäule = **9,81 mbar** | ρ Wasser = 1,0 |

## 2. Einmessen am Tisch (so am 08.10.2026 gemacht)

Benötigt: Glas mit Wasser, Lineal, die Box mit angeschlossenem Schlauch, HA-Entität `sensor.oltank_druck_rohwert`.

1. **Aufwärmen:** Gerät einschalten und **mindestens 5 Minuten** warten. Gemessen: Der Nullpunkt wanderte in den ersten
   Minuten um ~38.500 Einheiten (≈ 0,55 mbar ≈ 7 mm Öl), danach stabil (16:16 → 16:21 Δ ~300). Rauschen ~100–300.
2. **Anzeige-Abzweig dicht machen:** Am Tisch hing am T ein Ast „zur alten Anzeige“. Ein Rückschlagventil als Stopfen leckt
   schon bei ~10 mbar – das war am 08.10. die eigentliche Störung. Ast zuhalten oder fest verschließen.
3. **Nullpunkt:** Schlauchende offen an der Luft, „Messung starten“, Rohwert notieren (2 Lesungen) → `roh_null`.
   - 08.10.: **−2.788.747** (warm).
4. **Steigung:** Schlauchende senkrecht **10 cm unter die Wasseroberfläche** (gemessen ab Schlauchmündung), „Messung starten“,
   es muss perlen; Rohwert notieren.
   - 08.10.: **−2.101.492**.
5. Rechnen:
   ```
   roh_pro_mbar = (roh_10cm − roh_null) / 9,81
                = (−2.101.492 − (−2.788.747)) / 9,81
                = 687.255 / 9,81 ≈ 70.056
   ```
6. Werte in die `substitutions` der YAML im **ESPHome Builder** eintragen → OTA. Lokale `firmware/tankmessung.yaml` nachziehen.
7. **Gegenprobe:** wieder 10 cm Wasser → Soll 9,81 mbar.
   - 08.10. 16:27: **10,01 / 10,02 mbar** (+2 % ≈ 2 mm Eintauchtiefe), Füllhöhe 12,1 cm Öl-Äquivalent, Inhalt 243 l. ✔

Toleranz: Die Eintauchtiefe von Hand schwankt um einige Millimeter (spätere Läufe 10,07 … 10,76 mbar). Für den Tank
bedeutet 1 mbar ≈ 1,2 cm Öl; im unteren Bereich sind das je nach Höhe 20–45 l.

## 3. Abgleich am Tank (nach dem Einbau)

Das Tisch-Einmessen kalibriert nur den Sensor. Am Tank kommen hinzu: Lage des Leitungsendes über dem Tankboden,
tatsächliche Tankmaße und die Öldichte. Deshalb gegen eine unabhängige Messung prüfen:

1. **Peilstab im Domschacht** (ggf. mit Wasserfindungspaste, um Wasser/Schlamm am Boden zu erkennen).
2. Erwartung nach der Lieferung vom 05.10. (1.500 l in einen „leeren“ Tank, alte Anzeige danach 1.900 l):

   | Inhalt | Füllhöhe | Druck (rechnerisch) |
   |---|---|---|
   | 1.500 l | 42,7 cm | 35,2 mbar |
   | 1.700 l | 46,7 cm | 38,5 mbar |
   | 1.900 l | 50,6 cm | 41,7 mbar |

   Seitdem läuft der Brenner wieder – der aktuelle Stand liegt also etwas darunter.
   **Geklärt am 09.10.:** Die 1.900 l waren falsch – das alte Manometer ist defekt (drucklos ~800 l).
3. Weicht die Peilung ab:
   - **konstanter Versatz in cm** → Leitungsende sitzt nicht am Boden bzw. Schlamm; Korrektur über
     `number.oltank_leitungsende_uber_boden` (seit 09.10. in der Firmware, wird zur Füllhöhe addiert).
   - **proportionale Abweichung** → Öldichte/Tankmaße; `oel_mbar_pro_cm` anpassen.
4. Später zusätzlich mit jeder **Liefermenge** gegenprüfen (Zunahme in Litern vor/nach der Lieferung).

### Abgleich ohne Peilstab: Lieferbilanz (09.10.2026)

Der Peilstab war nicht erreichbar. Stattdessen:

- 05.10.: **1.500 l** in einen „leeren“ Tank (der Brenner bekam kein Öl mehr = Spiegel am Ende des Saugrohrs).
- Verbrauch bis 09.10. ~35 l (geschätzt, ~7 l/Tag im Oktober) → jetzt **mindestens ~1.465 l** + Rest unter dem Saugrohr.
- Gemessen **ohne** Korrektur: 30,95–31,1 mbar beim Pumpen, nach 10 s Ruhe ≈ 30 mbar → 36,1 cm ≈ **1.184 l** – weniger als
  allein die Lieferung. → Das Leitungsende sitzt **über dem Tankboden**.

Unbekannt bleibt der Rest unter dem Saugrohr. Abhängig davon:

| Saugrohr endet … über Boden | Rest vor Lieferung | Inhalt jetzt | Leitungsende über Boden |
|---|---|---|---|
| 3 cm | 30 l | ≈ 1.495 l | **6,5 cm** (eingestellt) |
| 5 cm | 65 l | ≈ 1.530 l | 7,2 cm |
| 10 cm | 182 l | ≈ 1.647 l | 9,6 cm |
| 15 cm | 331 l | ≈ 1.796 l | 12,5 cm |
| 20 cm | 505 l | ≈ 1.970 l | 15,8 cm |

Eingestellt ist der **Mindestwert 6,5 cm**: Der Inhalt wird eher zu niedrig angezeigt – für Warnungen die sichere Seite.
Kontrolllauf 09.10. 16:07: **43,0 cm ≈ 1.516 l**.

**Genauer Abgleich bei der nächsten Lieferung:** direkt davor und direkt danach je eine Messung, Liefermenge vom Lieferschein.
Weil der Tank rund ist, entspricht jeder Zentimeter je nach Höhe unterschiedlich vielen Litern – aus zwei Höhen und der
bekannten Literdifferenz ergibt sich die Korrektur eindeutig.

## 4. Peiltabelle (aus der Firmware-Formel)

Rechnerisch mit r = 8 dm, L = 37,5 dm, skaliert auf 7.000 l, 0,824 mbar/cm. Der erwartete Rohwert gilt für die
Einmessung vom 08.10. Druck und Rohwert gelten **ohne** Leitungsende-Korrektur; mit Korrektur gehört ein Druck zur Füllhöhe
„Tabellenhöhe + Korrektur“.

| Füllhöhe | Inhalt | Druck | Rohwert (erwartet) |
|---|---|---|---|
| 10 cm | 182 l | 8,2 mbar | −2.211.000 |
| 20 cm | 505 l | 16,5 mbar | −1.634.000 |
| 28 cm | 823 l | 23,1 mbar | −1.172.000 |
| 30 cm | 909 l | 24,7 mbar | −1.057.000 |
| 40 cm | 1.369 l | 33,0 mbar | −480.000 |
| 50 cm | 1.869 l | 41,2 mbar | +98.000 |
| 60 cm | 2.398 l | 49,4 mbar | +675.000 |
| 70 cm | 2.944 l | 57,7 mbar | +1.252.000 |
| 80 cm | 3.500 l | 65,9 mbar | +1.829.000 |
| 100 cm | 4.602 l | 82,4 mbar | +2.984.000 |
| 120 cm | 5.631 l | 98,9 mbar | +4.138.000 |
| 140 cm | 6.495 l | 115,4 mbar | +5.293.000 |
| 160 cm | 7.000 l | 131,8 mbar | +6.447.000 |

Warnschwellen (geplant): 1.500 l ≈ 42,7 cm, 800 l ≈ 27,5 cm.

> Hinweis (rechnerisch, nicht am Gerät geprüft): Der HX710B liefert 24-bit-Werte bis +8.388.607. Mit dieser Einmessung
> wäre das bei rund **160 mbar** erreicht. Ein voller Tank (132 mbar) passt noch hinein; Werte darüber sind kein Füllstand,
> sondern Pumpendruck in einer verstopften Leitung.

## 5. Einstellungen nach dem Einmessen

| Entität | Normalbetrieb | Dichtprobe |
|---|---|---|
| `number.oltank_spulzeit_pumpe` | 30 s | 30 s |
| `number.oltank_beruhigungszeit` | **10 s** | 60 s |
| `number.oltank_uberdruck_grenze` | 150 mbar | 150 mbar (erster Lauf an neuer Leitung: 50 mbar) |
| `number.oltank_leitungsende_uber_boden` | 6,5 cm (vorläufig, siehe oben) | – |
| `switch.oltank_automatische_messung` | erst nach dem Abgleich am Tank **an** (an seit 09.10.) | aus |
