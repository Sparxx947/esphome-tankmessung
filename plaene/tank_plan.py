import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch
fig = plt.figure(figsize=(8.27, 11.69)); ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,210); ax.set_ylim(0,297); ax.axis("off")
L=dict(color="black", lw=1.4)
def line(*p, **k): ax.plot([a[0] for a in p],[a[1] for a in p], **{**L, **k})
def dot(x,y,c="black"): ax.add_patch(Circle((x,y),0.9,color=c))
def box(x,y,w,h,titel,pins,seite="l",fs=8.5):
    ax.add_patch(Rectangle((x,y),w,h,fill=False,lw=1.5)); ax.text(x+w/2,y+h+2,titel,ha="center",fontsize=9.5,fontweight="bold")
    for name,(px,py) in pins.items(): ax.text(px,py,name,fontsize=fs,va="center",ha=("left" if seite=="l" else "right"))
T=lambda x,y,s,**k: ax.text(x,y,s,**{"fontsize":9,**k})
T(15,282,"Tankmessung (pneumatisch) – Schaltplan",fontsize=18,fontweight="bold")
T(15,274,"Erdtank 7.000 l · ESP32-WROOM-32U DevKitC · ESPHome tankmessung (192.168.178.194) · Stand 08.10.2026",fontsize=8.5)

# ESP32
ex,ey,ew,eh=15,170,45,85
box(ex,ey,ew,eh,"ESP32 DevKitC",{},fs=8.5)
pins={"5V":250,"3V3":238,"GND":226,"GPIO19":208,"GPIO18":196,"GPIO25":180}
for n,y in pins.items():
    T(ex+ew-2,y,n,ha="right",fontsize=9,fontweight="bold"); line((ex+ew,y),(ex+ew+4,y))
T(ex+3,ey+4,"USB-C = Strom\n(Netzteil ≥ 1 A)",fontsize=7.5,color="dimgray")

# Schienen
line((ex+ew+4,250),(195,250),color="darkorange",lw=1.8); T(197,249,"5 V",color="darkorange",fontweight="bold")
line((ex+ew+4,238),(130,238),color="firebrick",lw=1.6); T(132,237,"3V3",color="firebrick",fontweight="bold")
line((ex+ew+4,226),(195,226),lw=1.8); T(197,225,"GND",fontweight="bold")

# HX710B
hx,hy=85,190
box(hx,hy,40,30,"Drucksensor HX710B (0–40 kPa)",{},fs=8)
for n,y in (("VCC",214),("GND",207),("OUT",200),("SCK",193)): T(hx+2,y,n,fontsize=8.5); line((hx-4,y),(hx,y))
line((hx-4,214),(hx-8,214),(hx-8,238)); dot(hx-8,238,"firebrick")
line((hx-4,207),(hx-14,207),(hx-14,226)); dot(hx-14,226)
line((ex+ew+4,208),(70,208),(70,200),(hx-4,200)); line((ex+ew+4,196),(76,196),(76,193),(hx-4,193))
T(66,203.5,"GPIO19 → OUT",fontsize=7); T(66,188.5,"GPIO18 → SCK",fontsize=7)
ax.add_patch(Circle((hx+40,hy+15),2.2,fill=False,lw=1.3)); T(hx+43,hy+12,"Schlauch-\nstutzen",fontsize=7.5)

# MOSFET-Modul D4184
mx,my=140,150
box(mx,my,40,32,"Dual-MOSFET-Modul (CQUANZX)",{},fs=8)
for n,y in (("TRIG/PWM",176),("GND",169)): T(mx+2,y,n,fontsize=8.5)
for n,y in (("VIN+",176),("VIN−",169),("OUT+",160),("OUT−",154)): T(mx+38,y,n,fontsize=8.5,ha="right")
line((ex+ew+4,180),(100,180),(100,176),(mx,176)); T(78,182,"GPIO25 → PWM",fontsize=7.5)
line((mx,169),(110,169),(110,226)); dot(110,226)
line((mx+40,176),(188,176),(188,250)); dot(188,250,"darkorange")
line((mx+40,169),(192,169),(192,226)); dot(192,226)
# Pumpe
px,py=172,130
ax.add_patch(Circle((px,py),8,fill=False,lw=1.5)); T(px-3.2,py-2,"M",fontsize=12,fontweight="bold")
T(px-62,py-20,"Luftpumpe M20 (3–3,7 V)\nmax. 85 % PWM, nach 60 s aus",fontsize=7.8)
line((mx+40,160),(196,160),(196,py),(px+8,py)); line((mx+40,154),(184,154),(184,py+14),(px,py+14),(px,py+8))
dxx=160
line((dxx,py+14),(dxx,py+9)); line((dxx,py+14),(px,py+14)); ax.add_patch(Polygon([(dxx-3,py+9),(dxx+3,py+9),(dxx,py+3.5)],closed=True,fill=False,lw=1.3)); line((dxx-3,py+3.1),(dxx+3,py+3.1))
line((dxx,py+3),(dxx,py-12),(196,py-12),(196,py)); dot(196,py); dot(dxx,py+14)
T(dxx-34,py+7,"1N5819",fontsize=8,fontweight="bold"); T(dxx-34,py+2.5,"Strich → +",fontsize=7)
T(197,py+3,"+ (rot)",fontsize=8.5,fontweight="bold"); T(px+2,py+15,"− (schwarz)",fontsize=8.5,fontweight="bold")


T(15,113,"Hinweise",fontsize=11,fontweight="bold")
T(15,105,"• Pumpe NICHT direkt an einen GPIO – nur über das MOSFET-Modul. Freilaufdiode 1N5819: Strich (Kathode) an OUT+.",fontsize=8.2)
T(15,99,"• HX710B an 3V3 (nicht 5 V), sonst liegen 5-V-Pegel an GPIO19.",fontsize=8.2)
T(15,93,"• Masse gemeinsam: ESP-GND, Sensor-GND, Modul-GND (Steuer- und Lastseite).",fontsize=8.2)
T(15,87,"• Modul schaltet MINUS: Pumpe nur an OUT+/OUT−, nie zwischen VIN− und GND. Aufdruck auf dem Modul gilt.",fontsize=8.2)

# Pneumatik
T(15,78,"Schlauchführung (erst NACH dem Freiblasen der Messleitung anschließen)",fontsize=11,fontweight="bold")
yy=50
items=[(15,"Erdtank\n(Leitungsende\nam Boden)"),(50,"Kupfer-\nMessleitung\n6 mm"),(85,"Messing-T\n6×4×6"),(150,"Aquarium-T\n4 mm")]
for x,t in items: ax.add_patch(Rectangle((x,yy-6),24,12,fill=False,lw=1.2)); T(x+12,yy,t,ha="center",va="center",fontsize=7)
for a,b in ((39,50),(74,85),(109,150)): line((a,yy),(b,yy),color="steelblue",lw=2.5)
T(112,yy+2,"4-mm-Silikonschlauch",fontsize=7,color="steelblue")
line((97,yy+6),(97,yy+14),color="steelblue",lw=2.5); ax.add_patch(Rectangle((85,yy+14),24,9,fill=False,lw=1.2)); T(97,yy+18.5,"alte Anzeige",ha="center",va="center",fontsize=7)
line((162,yy+6),(162,yy+14),color="steelblue",lw=2.5); ax.add_patch(Rectangle((150,yy+14),24,9,fill=False,lw=1.2)); T(162,yy+18.5,"HX710B",ha="center",va="center",fontsize=7.5)
line((162,yy-6),(162,yy-12),color="steelblue",lw=2.5)
ax.add_patch(Rectangle((150,yy-21),24,9,fill=False,lw=1.2)); T(162,yy-16.5,"Rückschlag-\nventil",ha="center",va="center",fontsize=6.8)
ax.add_patch(FancyArrowPatch((185,yy-16),(175,yy-16),arrowstyle="-|>",mutation_scale=10,color="steelblue",lw=2))
ax.add_patch(Rectangle((185,yy-21),17,9,fill=False,lw=1.2)); T(193.5,yy-16.5,"Pumpe",ha="center",va="center",fontsize=7.5)
T(15,5,"Rückschlagventil: Luft nur von der Pumpe zur Leitung (Pfeil auf dem Ventil zeigt zur Leitung).\n"
       "Ablauf je Messung: Pumpe 30 s (Leitung leerblasen, bis es am Tankboden perlt) → aus → 10 s Ruhe → Druck = Ölsäule.\n"
       "1 cm Heizöl ≈ 0,824 mbar · voll (160 cm) ≈ 132 mbar.\n"
       "Eingemessen 08.10.: roh_null −2.788.747, 70.056 roh/mbar (10 cm Wassersäule = 9,81 mbar). Abzweig zur alten Anzeige DICHT verschließen.",fontsize=7.6)
fig.savefig("tankmessung-schaltplan.pdf")
