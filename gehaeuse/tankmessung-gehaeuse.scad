// Gehaeuse „Tankmessung“ — pneumatische Oelstandsmessung an der Kupfer-Messleitung
// Inhalt: ESP32-DevKitC (der zweite aus der Bestellung), Drucksensor-Modul 0–40 kPa (HX710B),
//         Mini-Luftpumpe M20 (3 V), Dual-MOSFET-Modul CQUANZX (15 A, ohne Optokoppler; D4184-Modul taugt an 5 V nicht), Rueckschlagventil + T-Verbinder (Aquarium, 4 mm)
// Stand 04.10.2026 — Notiz project_oeltank_fuellstandsensor
//
// Die Masse von Pumpe, Sensor- und MOSFET-Modul sind nicht vermessen. Deshalb werden sie NICHT in
// passgenaue Aufnahmen gesetzt, sondern mit Kabelbindern auf Laschen im Boden gezogen (Schlitze 3,5 x 1,8 mm).
// Nur der ESP32 liegt wie im Heizungsgehaeuse auf Stirn-Auflagen.
//
// Teile: TEIL = "box" | "deckel" | "alle"
// Material: PETG oder PLA (Raumtemperatur, Wandmontage). 0,2 mm Schicht, keine Stuetzen.

TEIL = "alle";
$fn = 48;

// ---------- Innenmasse ----------
iL = 110;          // Laenge
iB = 64;           // Breite
iH = 40;           // Hoehe — 08.10.: 30 → 40, HX710B steht auf 17-mm-Stuetzen (Dupont darunter), Stutzen + Schlauchbogen oben drauf
w  = 2.0;          // Wand
bo = 2.0;          // Boden

// ESP32 (wie im Heizungsgehaeuse)
esp_l = 49.9; esp_b = 28.2; esp_spiel = 0.8;   // 48,24 + 1,6 USB-Ueberstand × 28,15 (Jens gemessen 06.10.)
auflage_h = 17;    // Platz fuer Dupont-Buchsen unter der Platine
auflage_t = 4.5;
usb_b = 12; usb_h = 7; usb_ueber_platte = 1.6;
stift_rand = 3.2;  // Stiftreihen 1,4 mm vom Laengsrand, Kunststoff + Dupont bis ~2,7 mm → Stuetzen bleiben 3,2 mm weg
mitte_frei = 12;   // freie Mitte zwischen den Stuetzen (USB-C-Loetlaschen)
hx_x = 80; hx_y0 = 25;   // HX710B: Mitte in x, Stiftleisten-Kante (vorn) in y
hx_b = 18.14; hx_st = 2.5;   // Breite ueber die Ohren, Stuetzenbreite
sma_x = 62;        // 08.10.: SMA rechts NEBEN dem ESP-Fach (Trennsteg endet bei x 55,1, Mutter ueber Ecken Ø9,2)

// Durchfuehrungen
schlauch_d = 6.6;  // 4-mm-Aquariumschlauch (6 mm aussen) zur Messleitung
kabel_d    = 5;    // optional: Leitung zum Optolink-ESP / Strom
// Kabelbinder-Laschen
kb_l = 3.5; kb_b = 1.8; kb_steg = 6;   // zwei Schlitze im Abstand kb_steg

aL = iL + 2*w; aB = iB + 2*w; aH = bo + iH;
esp_x0 = w;                         // ESP-Fach links (x = 0 … esp_l+2*spiel)
esp_iL = esp_l + 2*esp_spiel;
esp_iB = esp_b + 2*esp_spiel;

module rund_quader(l, b, h, r=2) {
    hull() for (x=[r, l-r], y=[r, b-r]) translate([x,y,0]) cylinder(r=r, h=h);
}

module kabelbinder_lasche(x, y, quer=false, steg=kb_steg) {
    // zwei Schlitze durch den Boden, Kabelbinder von unten durchziehen.
    // quer=false: Schlitze in x versetzt → Binderschlaufe umfasst ein Teil, das LAENGS y liegt.
    // quer=true:  Schlitze in y versetzt → Schlaufe umfasst ein Teil, das LAENGS x liegt.
    for (s=[-steg/2, steg/2])
        translate([x, y, -0.1]) rotate([0,0,quer?90:0])
            translate([s - kb_b/2, -kb_l/2, 0]) cube([kb_b, kb_l, bo+0.2]);
}

module box() {
    platte_z = bo + auflage_h;
    usb_z = platte_z + 1.6 + usb_ueber_platte;
    difference() {
        rund_quader(aL, aB, aH);
        translate([w, w, bo]) cube([iL, iB, iH+1]);

        // USB-C fuer den ESP32 (linke Stirnseite), ESP liegt an der vorderen Wand (y klein)
        translate([-1, w + esp_iB/2 - usb_b/2, usb_z - usb_h/2]) cube([w+2, usb_b, usb_h]);

        // SMA-Antennenbuchse (WROOM-32U braucht die externe Antenne) in der vorderen Wand, rechts neben dem
        // ESP-Fach. 08.10.: vorher unter der Platine bei x 39,5 / z 10 — die Mutter (bis z 14,6) traf dort die
        // Stifte der vorderen Leiste (Spitzen bis z ~10,5, y ~4). Pigtail reicht vom U.FL am Antennenende.
        translate([sma_x, -1, bo + 8]) rotate([-90,0,0]) cylinder(d=6.6, h=w+2);

        // Schlauch zur Messleitung (rechte Stirnseite, unten)
        translate([aL-w-1, aB*0.70, bo+6]) rotate([0,90,0]) cylinder(d=schlauch_d, h=w+2);
        // optionale Kabeldurchfuehrung (rechte Stirnseite, oben)
        translate([aL-w-1, aB*0.30, bo+iH-7]) rotate([0,90,0]) cylinder(d=kabel_d, h=w+2);

        // Lueftung hinten
        for (i=[0:7]) translate([w+40+i*7, aB-w-1, bo+8]) cube([2.4, w+2, 14]);

        // Kabelbinder-Laschen im rechten Bereich (Pumpe, Sensor, MOSFET)
        // 08.10. neu nach Jens' Massen (rechtes Fach innen x 55,1–112, y 2–66). Vorher lag die Pumpe quer zu
        // ihren Bindern und das MOSFET-Modul (35 mm) ragte 4 mm ueber die rechte Wand.
        // Pumpe Ø 9,95 × 38, Stutzen stirnseitig → laengs x, hinten, Stutzen nach rechts (Platz bis Ø 20)
        kabelbinder_lasche(64, 55, true, 8);   // Pumpe x 57–95 (Loetfahnen links, Stutzen ~+4 mm rechts)
        kabelbinder_lasche(86, 55, true, 8);
        // MOSFET CQUANZX 35 × 17,2 × 14,2 → laengs x, vorn rechts (x 74–109, y 4–21), weg von der SMA-Mutter
        kabelbinder_lasche(91.5, 12.6, true, 12);
        // Drucksensor-Modul HX710B: KEINE Binder — Stiftleiste zeigt nach unten (Fotos 08.10.), steht auf zwei Stuetzen (s. u.)
        // Rueckschlagventil / T-Verbinder → rechts, zwischen Pumpenstutzen und Schlauchausgang
        kabelbinder_lasche(105, 38, false, 6);

        // Wandlaschen-Loecher kommen ueber die Laschen (siehe unten)
        // Beschriftung Boden aussen
        translate([aL/2, aB/2, -0.01]) mirror([1,0,0]) linear_extrude(0.5)
            text("TANKMESSUNG", size=5, font="Liberation Sans:style=Bold", halign="center", valign="center");
    }
    // ESP32-Stuetzen: je Stirnseite zwei, ZWISCHEN Stiftleiste und Mitte (wie Optolink-Gehaeuse 07.10.).
    // 08.10.: vorher durchgehende Auflage ueber die ganze Breite → die nach unten zeigenden Stifte
    // (Leisten laufen ueber die ganze Platinenlaenge) waeren an beiden Enden aufgesessen.
    st_b = esp_b/2 - stift_rand - mitte_frei/2;      // Breite je Stuetze (~4,9 mm)
    for (x=[esp_x0, esp_x0 + esp_iL - auflage_t], s=[-1,1])
        translate([x, w + esp_iB/2 + (s>0 ? mitte_frei/2 : -mitte_frei/2 - st_b), bo])
            cube([auflage_t, st_b, auflage_h]);
    // HX710B-Stuetzen unter den beiden Befestigungsohren (Jens 08.10.: Ohrenbreite 18,14, Laenge 18,35, Koerper 13,59,
    // Hoehe ueber Platine bis Stutzen 11,24; Lochlinie ~7,3 mm von der Stiftleisten-Kante, aus Foto geschaetzt).
    // Stiftleiste (VCC OUT SCK GND) liegt 4,9–12,9 mm vom linken Ohrrand → Dupont-Buchsen haben ≥ 1 mm Luft zu den Stuetzen.
    // Befestigung: Heisskleber auf die Stuetzen (Lochabstand nur geschaetzt, daher keine Schraubloecher).
    for (x=[hx_x - hx_b/2, hx_x + hx_b/2 - hx_st])
        translate([x, hx_y0 + 7.3 - 2.5, bo]) cube([hx_st, 5, auflage_h]);
    // Trennsteg als Anschlag fuer die ESP-Platine (nur niedrig, laesst Kabel durch)
    translate([esp_x0 + esp_iL, w, bo]) cube([1.6, esp_iB, 6]);
    // Wandlaschen mit Schraubloch (oben und unten an den Laengsseiten)
    for (x=[aL*0.2, aL*0.8], y=[-8, aB]) translate([x-7, y, 0]) difference() {
        hull() { cube([14, 8, 3]); }
        translate([7, (y<0)?4:4, -1]) cylinder(d=4.5, h=5);
    }
}

module deckel() {
    difference() {
        union() {
            rund_quader(aL, aB, 1.8);
            translate([w+0.25, w+0.25, 1.8]) difference() {
                cube([iL-0.5, iB-0.5, 3]);
                translate([1.4,1.4,-1]) cube([iL-0.5-2.8, iB-0.5-2.8, 5]);
            }
        }
        // Sichtfenster ueber dem ESP fuer die Status-LED (optional)
        translate([w+esp_iL*0.5, w+esp_iB*0.5, -1]) cylinder(d=3, h=5);
    }
}

if (TEIL=="box") box();
if (TEIL=="deckel") deckel();
if (TEIL=="alle") { box(); translate([0, aB+20, 0]) deckel(); }
