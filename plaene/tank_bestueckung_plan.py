import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages

MM = 1/25.4
fig = plt.figure(figsize=(297*MM, 210*MM))
# Zeichenflaeche im Massstab 2:1 : 114 mm Gehaeuse -> 228 mm
ax = fig.add_axes([12/297, 58/210, 228/297, 136/210])
ax.set_xlim(-2, 116); ax.set_ylim(-2, 70); ax.set_aspect("equal"); ax.axis("off")

def box(x, y, w, h, fc, ec="black", lw=1, z=2, ls="-", alpha=1):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z, ls=ls, alpha=alpha))
def txt(x, y, s, size=7, **k):
    ax.text(x, y, s, fontsize=size, ha=k.pop("ha", "center"), va=k.pop("va", "center"), zorder=10, **k)

# Gehaeuse (aussen 114 x 68, innen 2..112 x 2..66)
ax.add_patch(FancyBboxPatch((0, 0), 114, 68, boxstyle="round,pad=0,rounding_size=2", fc="#e8e8e8", ec="black", lw=1.5, zorder=0))
box(2, 2, 110, 64, "white", lw=0.6, z=1)
# Waende beschriften
txt(57, -1.2, "VORNE (Wand mit SMA-Buchse)", 6.5, style="italic")
txt(57, 69.2, "HINTEN (Lüftungsschlitze)", 6.5, style="italic")
for i in range(8): box(42+i*7, 66, 2.4, 2, "white", lw=0.4, z=1)

# ESP-Stuetzen + ESP
for x in (2, 49):
    for y in (16.9-10.9, 16.9+6):
        box(x, y, 4.5, 4.9, "#b07c3c", lw=0.4, z=2)
box(2.8, 2.8, 49.9, 28.2, "#2d6cdf", alpha=0.35, lw=1.2, z=3)
txt(27, 22, "ESP32 DevKitC", 9, weight="bold")
txt(27, 17, "liegt auf 4 Stützen (braun),\nStifte + Dupont-Stecker nach UNTEN", 6.5)
txt(27, 9.5, "USB-C ← links durch die Wand", 6.5)
box(-0.5, 16.9-3.5, 3, 7, "#2d6cdf", lw=0.8, z=4)  # USB-Oeffnung
txt(48, 27, "U.FL", 6, color="#123")
# Trennsteg
box(53.5, 2, 1.6, 29.8, "#888", lw=0.4, z=2)
txt(54.3, 34, "Trennsteg", 5.5, rotation=90, va="bottom")
# SMA
ax.add_patch(Circle((62, 1), 3.3, fc="#d4a017", ec="black", lw=0.8, zorder=4))
txt(62, 7.5, "SMA-\nBuchse", 6)
ax.plot([48, 52, 58, 62], [27, 30, 12, 4], color="#d4a017", lw=1.2, zorder=5, ls="--")
txt(56, 20, "Pigtail", 5.5, color="#8a6a00", rotation=-70)

# MOSFET XY-MOS 35 x 17,2 (x 74-109, y 4-21.2)
box(74, 4, 35, 17.2, "#1f5fa8", alpha=0.45, lw=1.2, z=3)
txt(91.5, 12.6, "MOSFET-Modul\nXY-MOS", 8, weight="bold")
box(74.5, 5, 5, 15, "#3aa0d0", lw=0.6, z=4); txt(77, 12.6, "Klemmen\nOUT/VIN", 5, rotation=90)
txt(106, 12.6, "TRIG\nGND", 5.5)
# Kabelbinder MOSFET
ax.plot([91.5, 91.5], [6.6-1.75, 18.6+1.75], color="red", lw=1.5, zorder=6, ls=":")

# HX710B auf Stuetzen (x 70.9-89.1, y 25-43.6)
for x in (70.93, 86.57): box(x, 29.8, 2.5, 5, "#b07c3c", lw=0.4, z=2)
box(70.9, 25, 18.2, 18.6, "#d9433b", alpha=0.45, lw=1.2, z=3)
txt(80, 33.5, "HX710B", 8.5, weight="bold")
txt(80, 27, "VCC OUT SCK GND\n(Stifte vorn, nach unten)", 5)
ax.add_patch(Circle((80, 39.5), 2.0, fc="black", zorder=5)); txt(80, 42.6, "Stutzen ↑", 5.5)
txt(80, 46, "Heißkleber auf die 2 Stützen", 5.5, color="#7a2a00")

# Pumpe (x 57-95, y 50-60) + Stutzen
box(57, 50, 38, 10, "#7f8c8d", alpha=0.6, lw=1.2, z=3)
txt(74, 55, "Pumpe (Lötfahnen links)", 8, weight="bold")
box(95, 51.5, 4, 2.5, "#555", lw=0.6, z=4); box(95, 56, 4, 2.5, "#555", lw=0.6, z=4)
txt(97, 49.5, "Stutzen →", 5.5)
for x in (64, 86): ax.plot([x, x], [51-1.75, 59+1.75], color="red", lw=1.5, zorder=6, ls=":")

# Rueckschlagventil + T (rechts)
box(102.5, 36, 5, 12, "#9b59b6", alpha=0.5, lw=1, z=3)
txt(105, 42, "Ventil", 5.5, rotation=90)
ax.annotate("", xy=(105, 36.5), xytext=(105, 47.5), arrowprops=dict(arrowstyle="-|>", color="#4a235a", lw=1.2), zorder=7)
ax.plot([105, 105], [38-3, 38+3], color="red", lw=1.5, zorder=6, ls=":")
box(103, 30.5, 4, 4, "#f39c12", lw=0.8, z=4); txt(110, 32.5, "T", 7, weight="bold")

# Schlaeuche
hose = dict(color="#16a085", lw=2.4, zorder=5, solid_capstyle="round")
ax.plot([99, 101.5, 105, 105], [57.2, 57.2, 54, 48], **hose)   # Pumpe (blasend) -> Ventil
ax.plot([105, 105], [36, 34.5], **hose)                        # Ventil -> T
ax.plot([103, 92, 80], [32.5, 38, 39.5], **hose)               # T -> HX710B
ax.plot([107, 109.5, 113.5], [32.5, 47.6, 47.6], **hose)       # T -> Schlauchausgang
ax.add_patch(Circle((113, 47.6), 1.8, fc="white", ec="#16a085", lw=1.5, zorder=6))
txt(116.5, 51.5, "Schlauch zur\nMessleitung\n(rechte Wand)", 6, ha="left")
ax.plot([99, 101], [52.7, 52.7], color="#16a085", lw=1, zorder=5, ls=":")
txt(104.5, 63, "2. Stutzen = Ansaugung, OFFEN lassen", 5.5)
ax.add_patch(Circle((113, 20.4), 1.3, fc="white", ec="black", lw=1, zorder=6))
txt(116.5, 20.4, "Kabeldurchführung\n(optional, oben)", 6, ha="left")

# Kabel (schematisch)
wire = dict(lw=1.1, zorder=4, alpha=0.9)
ax.plot([45, 66, 74.5], [31, 31, 14], color="#c0392b", **wire)       # 5V -> VIN+
ax.plot([45, 64, 74.5], [30, 29, 11], color="black", **wire)         # GND -> VIN-
ax.plot([50, 60, 70, 106], [31.5, 36, 23, 15], color="#e67e22", **wire)  # GPIO25 -> TRIG
ax.plot([57, 74.5], [55, 18], color="#c0392b", **wire, ls="--")     # Pumpe -> OUT
ax.plot([30, 40, 72], [31, 34, 26], color="#8e44ad", **wire)         # Sensor 4 Adern
txt(36, 36.5, "4 Adern zum HX710B\n3V3 · GPIO19 · GPIO18 · GND", 5.5, color="#5b2c6f")
txt(64, 23.5, "5V/GND → VIN", 5.5, color="#922")
txt(63.5, 41, "Pumpe → OUT+/OUT−\n(+ Diode in die Klemmen)", 5.5, color="#922")
txt(93, 26.5, "GPIO25 → TRIG", 5.5, color="#a04000")

# Titel
fig.text(12/297, 202/210, "Tankmessung – Bestückung der Box (Draufsicht, Deckel ab, Maßstab 2:1)", fontsize=13, weight="bold")
fig.text(12/297, 196.5/210, "tank_box.stl Stand 08.10.2026 · Innen 110 × 64 × 40 mm · rote Punktlinien = Kabelbinder durch die Bodenschlitze", fontsize=8)

# Legende / Schritte rechts unten und unten
schritte = (
"Einbau-Reihenfolge\n"
"1. Dupont-Kabel an ESP32 + HX710B stecken (vorher!) – unter den Platinen ist später kein Platz für Finger.\n"
"2. ESP32 auf die 4 Stützen legen, USB-C links in die Wandöffnung. Pigtail an U.FL, SMA-Buchse in die vordere Wand rechts neben dem Trennsteg.\n"
"3. HX710B mit Heißkleber auf seine 2 Stützen, Stiftleiste nach VORN, Stutzen zeigt nach oben.\n"
"4. MOSFET-Modul vorn rechts mit 1 Kabelbinder, Klemmen zur Mitte (links). Diode 1N5819: Strich an OUT+.\n"
"5. Pumpe hinten mit 2 Kabelbindern, Stutzen nach rechts. Blasender Stutzen → Ventil (Pfeil zum T), Ansaugstutzen offen.\n"
"6. Ventil rechts mit 1 Kabelbinder, darunter das T: ein Abgang zum HX710B-Stutzen, einer durch die rechte Wand zur Messleitung.\n"
"7. Kabel aufräumen, Deckel drauf. Prüfen: Messung starten → am Schlauchende perlt es / bläst es.")
fig.text(12/297, 50/210, schritte, fontsize=7.6, va="top", linespacing=1.45)
fig.text(250/297, 52/210,
"Farben\n■ blau  ESP32\n■ rot   HX710B\n■ dunkelblau  MOSFET\n■ grau  Pumpe\n■ lila  Rückschlagventil\n■ orange  T-Stück\n■ braun  Stützen\n━ grün  Schläuche\n┄ rot  Kabelbinder",
fontsize=7, va="top", linespacing=1.5)

out = "tank-bestueckung"
fig.savefig(out + ".png", dpi=130)
fig.savefig(out + ".pdf")
