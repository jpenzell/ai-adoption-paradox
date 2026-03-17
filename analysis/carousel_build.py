"""
LinkedIn carousel PDF — 8 slides, 1080x1080pt square
Topic: What you FEEL about AI predicts whether you use it
Aesthetic: editorial ink-and-paper, bold typographic
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch

OUT = "/home/claude/carousel/linkedin_carousel.pdf"

# ── PALETTE ──────────────────────────────────────────────────────────────────
INK   = HexColor("#1A1208")
PAPER = HexColor("#F5F0E8")
ACCENT= HexColor("#E8630A")
MID   = HexColor("#6B5E4E")
RULE  = HexColor("#C8BCA8")
LITE  = HexColor("#EDE7DC")
WHITE = HexColor("#FFFFFF")
GREEN = HexColor("#2E7D32")
RED   = HexColor("#C62828")

W = H = 1080

def new_page(c):
    c.showPage()

def bg(c, color=PAPER):
    c.setFillColor(color); c.rect(0,0,W,H,fill=1,stroke=0)

def top_rules(c):
    c.setFillColor(INK);   c.rect(0,H-8, W,8, fill=1,stroke=0)
    c.setFillColor(ACCENT);c.rect(0,H-14,W,4, fill=1,stroke=0)

def bot_rules(c):
    c.setFillColor(ACCENT);c.rect(0,4,W,4,fill=1,stroke=0)
    c.setFillColor(INK);   c.rect(0,0,W,4,fill=1,stroke=0)

def label(c, text, x, y, size=16, color=MID, align="left", bold=False):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    if align=="center": c.drawCentredString(x,y,text)
    elif align=="right": c.drawRightString(x,y,text)
    else: c.drawString(x,y,text)

def swipe_cue(c):
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold",20)
    c.drawRightString(W-60,62,"swipe →")

def slide_num(c, n, total=8):
    c.setFillColor(RULE)
    c.setFont("Helvetica",18)
    c.drawRightString(W-60,38,f"{n} / {total}")

def footer_strip(c, text="Josh Penzell · Imagination Applied"):
    c.setFillColor(MID); c.setFont("Helvetica",18)
    c.drawString(60,38,text)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — HOOK
# ═══════════════════════════════════════════════════════════════════════════════
def slide_1(c):
    bg(c, INK); top_rules(c); bot_rules(c)

    # decorative circles — centered inward so they don't clip edges
    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.circle(W-200,H-200,160,fill=0,stroke=1)
    c.circle(W-200,H-200,100,fill=0,stroke=1)

    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold",18)
    c.drawString(72,H-90,"AI ADOPTION · NEW DATA · 2025")

    c.setFillColor(WHITE); c.setFont("Times-Bold",108)
    c.drawString(72,H-260,"Change")
    c.setFont("Times-Italic",108); c.setFillColor(ACCENT)
    c.drawString(72,H-370,"how they feel.")

    c.setFillColor(WHITE); c.setFont("Times-Roman",72)
    c.drawString(72,H-490,"Not how much")
    c.drawString(72,H-570,"they know.")

    c.setStrokeColor(ACCENT); c.setLineWidth(3)
    c.line(72,H-640,420,H-640)

    c.setFillColor(RULE); c.setFont("Times-Italic",30)
    c.drawString(72,H-690,"I analyzed 33,231 developer responses to find out")
    c.drawString(72,H-730,"what actually predicts daily AI use. Swipe to see.")

    c.setFillColor(RULE); c.setFont("Helvetica",16)
    c.drawString(72,H-800,"linkedin.com/in/josh-penzell")

    c.setFillColor(MID); c.setFont("Helvetica",18)
    c.drawString(72,38,"Source: 2025 Stack Overflow Developer Survey  ·  n = 33,231")
    slide_num(c,1); swipe_cue(c)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE WRONG PROBLEM
# ═══════════════════════════════════════════════════════════════════════════════
def slide_2(c):
    bg(c); top_rules(c); bot_rules(c)

    label(c,"THE PROBLEM",72,H-72,size=18,color=ACCENT,bold=True)
    label(c,"2 / 8",W-72,H-72,size=18,color=RULE,align="right")

    c.setFillColor(INK); c.setFont("Times-Bold",64)
    c.drawString(72,H-160,"We've been solving")
    c.setFont("Times-BoldItalic",64); c.setFillColor(ACCENT)
    c.drawString(72,H-236,"the wrong problem.")

    c.setStrokeColor(RULE); c.setLineWidth(1.5)
    c.line(72,H-300,W-72,H-300)

    items_left = [
        ("What most orgs focus on:", INK, True),
        ("More training & access",   MID, False),
        ("Better tools",             MID, False),
        ("Mandatory AI courses",     MID, False),
    ]
    items_right = [
        ("What the data says matters:", ACCENT, True),
        ("How people FEEL about AI",    INK, False),
        ("Structured learning pathway", INK, False),
        ("Using AI agents at all",      INK, False),
    ]

    lx, rx = 90, W//2+40
    for i,(items,x) in enumerate([(items_left,lx),(items_right,rx)]):
        for j,(text,color,bold) in enumerate(items):
            yy = H-380 - j*152
            if j==0:
                c.setFillColor(color); c.setFont("Helvetica-Bold",26)
                c.drawString(x,yy,text)
                c.setStrokeColor(RULE if i==0 else ACCENT); c.setLineWidth(1)
                c.line(x,yy-8,x+390,yy-8)
            else:
                prefix = "✗  " if i==0 else "✓  "
                pc = RED if i==0 else GREEN
                c.setFillColor(pc); c.setFont("Helvetica-Bold",34)
                c.drawString(x,yy,prefix)
                c.setFillColor(color); c.setFont("Times-Roman",34)
                c.drawString(x+46,yy,text)

    c.setStrokeColor(RULE); c.setLineWidth(1)
    c.line(W//2,H-330,W//2,H-900)

    # bottom anchor — raised to close gap
    c.setStrokeColor(ACCENT); c.setLineWidth(1.5)
    c.line(72, 170, W-72, 170)
    c.setFillColor(MID); c.setFont("Times-Italic", 26)
    c.drawCentredString(W//2, 130, "The fix isn't more training. It's different training.")

    footer_strip(c); swipe_cue(c)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE NUMBER
# ═══════════════════════════════════════════════════════════════════════════════
def slide_3(c):
    bg(c, INK); top_rules(c); bot_rules(c)

    # circle — center raised so bottom clears footer text
    cx, cy, r = W//2, H//2+100, 360
    c.setFillColor(HexColor("#2A1500"))
    c.circle(cx,cy,r,fill=1,stroke=0)
    c.setFillColor(ACCENT); c.setLineWidth(2); c.setStrokeColor(ACCENT)
    c.circle(cx,cy,r,fill=0,stroke=1)
    c.circle(cx,cy,r-20,fill=0,stroke=1)

    label(c,"THE NUMBER",72,H-72,size=18,color=ACCENT,bold=True)
    label(c,"3 / 8",W-72,H-72,size=18,color=MID,align="right")

    # "42.9%" same baseline, size-contrasted — centered in circle
    c.setFillColor(ACCENT)
    c.setFont("Times-Bold",200)
    w35   = c.stringWidth("42",  "Times-Bold",200)
    c.setFont("Times-Bold",100)
    w_dec = c.stringWidth(".9%","Times-Bold",100)
    total_w = w35 + w_dec
    x0 = cx - total_w/2
    baseline = cy + 10   # lowered from cy+50 to sit at circle visual center
    c.setFont("Times-Bold",200); c.drawString(x0,baseline,"42")
    c.setFont("Times-Bold",100); c.drawString(x0+w35,baseline,".3%")

    # label inside circle
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold",24)
    c.drawCentredString(cx, cy-160, "OF WHAT PREDICTS DAILY AI USE")

    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.line(cx-200,cy-195,cx+200,cy-195)

    c.setFillColor(RULE); c.setFont("Times-Italic",36)
    c.drawCentredString(cx, cy-240, "...is your sentiment toward AI.")

    # below circle
    c.setFillColor(WHITE); c.setFont("Times-Roman",38)
    c.drawCentredString(cx, 200, "Not how long you've coded. Not how much you trust it.")

    c.setFillColor(MID); c.setFont("Helvetica",18)
    c.drawString(72,70,"\"Sentiment\" = SO survey item: \"How favorable is your stance on using AI tools?\" · 6-point scale")
    c.drawString(72,50,"Predictive model · 33,231 responses · 77.1% accuracy · 5-fold cross-validated")
    c.drawString(72,30,"Cross-sectional data · association is strong and consistent · causal direction requires further study")
    slide_num(c,3); swipe_cue(c)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — BAR CHART
# ═══════════════════════════════════════════════════════════════════════════════
def slide_4(c):
    bg(c); top_rules(c); bot_rules(c)

    label(c,"THE FULL PICTURE",72,H-72,size=18,color=ACCENT,bold=True)
    label(c,"4 / 8",W-72,H-72,size=18,color=RULE,align="right")

    c.setFillColor(INK); c.setFont("Times-Bold",56)
    c.drawString(72,H-148,"What actually predicts")
    c.setFont("Times-BoldItalic",56); c.setFillColor(ACCENT)
    c.drawString(72,H-214,"daily AI use:")

    features = [
        ("How you FEEL about AI",           42.9, True),
        ("Learned a new AI tool this year", 16.3, False),
        ("Agent use",                       13.6, False),
        ("How capable you think AI is",     10.1, False),
        ("How much you TRUST AI",            9.2, False),
        ("Years of experience",              4.0, False),
        ("Years coding",                     3.6, False),
        ("Job threat perception",            0.6, False),
    ]

    bar_x    = 72
    bar_w_max= W - 72 - 230
    bar_h_hi = 44
    bar_h_lo = 30
    max_pct  = 38
    start_y  = H - 308   # was H-268 — first label was printing ON TOP of title
    row_h    = 112

    for i,(lbl_txt,pct,hi) in enumerate(features):
        yy   = start_y - i*row_h
        bh   = bar_h_hi if hi else bar_h_lo
        bw   = (pct/max_pct)*bar_w_max
        fs   = 26 if hi else 22

        c.setFillColor(INK if hi else MID)
        c.setFont("Times-Bold" if hi else "Times-Roman", fs)
        c.drawString(bar_x, yy+bh+8, lbl_txt)

        c.setFillColor(LITE)
        c.roundRect(bar_x,yy,bar_w_max,bh,4,fill=1,stroke=0)

        c.setFillColor(ACCENT if hi else MID)
        if not hi: c.setFillColorRGB(0.42,0.37,0.31,alpha=0.5)
        c.roundRect(bar_x,yy,bw,bh,4,fill=1,stroke=0)

        c.setFillColor(ACCENT if hi else MID)
        c.setFont("Times-Bold" if hi else "Times-Roman", fs)
        c.drawString(bar_x+bar_w_max+14, yy+(bh-fs)//2+fs//2, f"{pct}%")

    # prominent callout — elevated from footnote
    c.setFillColor(ACCENT); c.setLineWidth(2); c.setStrokeColor(ACCENT)
    c.line(72, 168, W-72, 168)
    c.setFillColor(ACCENT); c.setFont("Times-Bold", 30)
    c.drawCentredString(W//2, 118, "Sentiment is 4\u00d7 more predictive than trust. 15\u00d7 more than experience.")

    # Source attribution on data slide (replaces generic footer)
    c.setFillColor(MID); c.setFont("Helvetica",15)
    c.drawString(60,52,"Source: 2025 Stack Overflow Developer Survey  ·  n = 33,231")
    c.drawString(60,32,"Top 6 of 13 model features shown  ·  remaining 10.4% distributed across other variables")
    c.drawRightString(W-60,38,"Josh Penzell · Imagination Applied")
    swipe_cue(c)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — TWO SURPRISES
# ═══════════════════════════════════════════════════════════════════════════════
def slide_5(c):
    bg(c); top_rules(c); bot_rules(c)

    label(c,"TWO SURPRISES IN THE DATA",72,H-72,size=18,color=ACCENT,bold=True)
    label(c,"5 / 8",W-72,H-72,size=18,color=RULE,align="right")

    # Card 1 — fills top half
    card_y = H-108
    c.setFillColor(INK)
    c.roundRect(60,card_y-390,W-120,410,8,fill=1,stroke=0)

    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold",20)
    c.drawString(90,card_y-34,"SURPRISE #1 · THE THREAT PARADOX")

    c.setFillColor(WHITE); c.setFont("Times-Bold",58)
    c.drawString(90,card_y-108,"Threatened developers")
    c.drawString(90,card_y-174,"use AI MORE.")

    c.setFillColor(RULE); c.setFont("Times-Italic",30)
    c.drawString(90,card_y-224,"Threatened developers use AI more (3.05 vs 2.67).")
    c.drawString(90,card_y-264,"They're hedging — building competency defensively.")

    c.setFillColor(ACCENT); c.setFont("Times-Bold",72)
    c.drawRightString(W-90,card_y-120,"3.05")
    c.setFillColor(RULE); c.setFont("Helvetica",20)
    c.drawRightString(W-90,card_y-158,"avg usage score (0–4)")

    # Card 2 — fills bottom half, goes all the way down
    card2_y = card_y-442
    c.setFillColor(LITE)
    c.roundRect(60,card2_y-448,W-120,468,8,fill=1,stroke=0)
    c.setStrokeColor(ACCENT); c.setLineWidth(3)
    c.line(60,card2_y-448,60,card2_y+20)

    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold",20)
    c.drawString(90,card2_y-34,"SURPRISE #2 · THE OCCASIONAL-USER DIP")

    c.setFillColor(INK); c.setFont("Times-Bold",58)
    c.drawString(90,card2_y-104,"First contact is where")
    c.drawString(90,card2_y-170,"trust dies.")

    c.setFillColor(MID); c.setFont("Times-Italic",24)
    c.drawString(90,card2_y-212,"Monthly users trust AI LESS than people")
    c.drawString(90,card2_y-244,"who've never tried it. Trust only fully")
    c.drawString(90,card2_y-276,"recovers at daily use.")

    # mini bar chart — right-aligned, clear of text
    trust_pts = [("Not yet",1.64),("Mon.",1.31),("Wkly",1.72),("Daily",2.21)]
    bw=50; gap=24; cx_start = W-354
    for i,(lbl,val) in enumerate(trust_pts):
        x = cx_start + i*(bw+gap)
        bh = int(val*80)
        col = RED if i==1 else GREEN if i==3 else MID
        c.setFillColor(HexColor("#D8D0C6"))
        c.rect(x,card2_y-356,bw,200,fill=1,stroke=0)
        c.setFillColor(col)
        c.rect(x,card2_y-356,bw,bh,fill=1,stroke=0)
        c.setFillColor(col if i in [1,3] else MID)
        c.setFont("Helvetica-Bold" if i in [1,3] else "Helvetica",16)
        c.drawCentredString(x+bw//2,card2_y-378,lbl)

    # rotated axis label
    c.saveState()
    c.translate(cx_start-18, card2_y-256)
    c.rotate(90)
    c.setFillColor(MID); c.setFont("Helvetica",12)
    c.drawCentredString(0,0,"avg. trust score")
    c.restoreState()

    footer_strip(c); swipe_cue(c)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — THE 29pp FINDING
# ═══════════════════════════════════════════════════════════════════════════════
def slide_6(c):
    bg(c, INK); top_rules(c); bot_rules(c)

    label(c,"THE LEARNING PATHWAY EFFECT",72,H-72,size=18,color=ACCENT,bold=True)
    label(c,"6 / 8",W-72,H-72,size=18,color=MID,align="right")

    # "29" big, "-point gap" smaller — same baseline
    c.setFillColor(ACCENT)
    c.setFont("Times-Bold",260)
    w29  = c.stringWidth("29","Times-Bold",260)
    c.setFont("Times-Bold",96)
    wsub = c.stringWidth("-point gap","Times-Bold",96)
    x0   = 72
    base = H-430
    c.setFont("Times-Bold",260); c.drawString(x0,base,"29")
    c.setFont("Times-Bold",96);  c.drawString(x0+w29+10,base," point gap")

    c.setFillColor(WHITE); c.setFont("Times-Bold",42)
    c.drawString(72,H-482,"in trust between structured")
    c.drawString(72,H-532,"and informal AI learners.")

    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.line(72,H-562,W-72,H-562)

    pairs = [
        ("Bootcamp / online course","66.5% trust",GREEN,True),
        ("Colleague / on the job",  "37.3% trust",RED,  False),
    ]
    for i,(method,trust,col,hi) in enumerate(pairs):
        y = H-610 - i*160
        c.setFillColor(HexColor("#2A1500") if hi else HexColor("#1A1208"))
        c.roundRect(72,y-100,W-144,140,6,fill=1,stroke=0)
        c.setStrokeColor(col); c.setLineWidth(4)
        c.line(72,y-100,72,y+40)

        # vertically centered within card (card spans y-100 to y+40, mid = y-30)
        c.setFillColor(RULE); c.setFont("Helvetica",26)
        c.drawString(108,y-20,method)
        c.setFillColor(col); c.setFont("Times-Bold",44)
        c.drawRightString(W-100,y-24,trust)

    c.setStrokeColor(HexColor("#3A2010")); c.setLineWidth(1)
    c.line(72,H-896,W-72,H-896)
    c.setFillColor(MID); c.setFont("Times-Italic",28)
    c.drawString(72,H-934,"Structured learning builds trust. Exposure alone doesn't.")

    footer_strip(c); swipe_cue(c)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — IMPLICATIONS
# ═══════════════════════════════════════════════════════════════════════════════
def slide_7(c):
    bg(c); top_rules(c); bot_rules(c)

    label(c,"WHAT THIS MEANS FOR L&D",72,H-72,size=18,color=ACCENT,bold=True)
    label(c,"7 / 8",W-72,H-72,size=18,color=RULE,align="right")

    c.setFillColor(INK); c.setFont("Times-Bold",56)
    c.drawString(72,H-152,"Five implications")
    c.setFont("Times-BoldItalic",56); c.setFillColor(ACCENT)
    c.drawString(72,H-218,"for your AI programs:")

    implications = [
        ("Measure sentiment before training.", "You need a baseline, not an assumption."),
        ("Design for feeling, not knowing.",   "Demos that delight build adoption. Lectures don't."),
        ("Build structured pathways.",         "The 29-point gap is a design problem, not a people problem."),
        ("Expect the first-contact dip.",      "New users often trust AI LESS. That's not failure."),
        ("Resisters aren't ignorant.",         "They're unconvinced. Different problem, different fix."),
    ]

    start_y = H-284; row_h = 134
    for i,(title,detail) in enumerate(implications):
        yy = start_y - i*row_h
        c.setFillColor(ACCENT)
        c.circle(96,yy-14,24,fill=1,stroke=0)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold",22)
        c.drawCentredString(96,yy-22,str(i+1))

        c.setFillColor(INK); c.setFont("Times-Bold",28)
        c.drawString(136,yy,title)
        c.setFillColor(MID); c.setFont("Times-Italic",24)
        c.drawString(136,yy-34,detail)

        if i < len(implications)-1:
            c.setStrokeColor(RULE); c.setLineWidth(0.75)
            c.line(72,yy-56,W-72,yy-56)

    # closing rule above footer to frame the content zone
    c.setStrokeColor(RULE); c.setLineWidth(0.75)
    c.line(72,110,W-72,110)

    footer_strip(c); swipe_cue(c)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — CTA
# ═══════════════════════════════════════════════════════════════════════════════
def slide_8(c):
    bg(c, INK); top_rules(c); bot_rules(c)

    label(c,"8 / 8",W-72,H-72,size=18,color=MID,align="right")

    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold",18)
    c.drawString(72,H-90,"FROM THE DATA")

    # quote
    c.setFillColor(WHITE); c.setFont("Times-Italic",64)
    c.drawString(72,H-188,'"Change how they feel.')
    c.drawString(72,H-262,'Not how much')
    c.drawString(72,H-336,'they know."')

    c.setStrokeColor(ACCENT); c.setLineWidth(3)
    c.line(72,H-368,380,H-368)

    c.setFillColor(RULE); c.setFont("Times-Roman",28)
    c.drawString(72,H-416,"Sentiment outpredicts trust 4 to 1.")
    c.drawString(72,H-452,"It outpredicts experience 15 to 1.")

    c.setStrokeColor(RULE); c.setLineWidth(1)
    c.line(72,H-540,W-72,H-540)

    # question — shifted down so spacing is balanced through the slide
    c.setFillColor(WHITE); c.setFont("Times-Italic",40)
    c.drawString(72,H-622,"When your org rolled out AI — did you")
    c.drawString(72,H-672,"measure how people felt first, or jump")
    c.drawString(72,H-722,"straight to tools and training?")

    c.setFillColor(RULE); c.setFont("Times-Roman",26)
    c.drawString(72,H-772,"Drop your answer below. I read every reply.")

    # author block — compact, well-filled card
    c.setFillColor(HexColor("#2A1500"))
    c.roundRect(60,100,W-120,130,8,fill=1,stroke=0)
    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.roundRect(60,100,W-120,130,8,fill=0,stroke=1)

    c.setFillColor(ACCENT); c.setFont("Times-Bold",34)
    c.drawString(100,196,"Josh Penzell")
    c.setFillColor(RULE); c.setFont("Helvetica",20)
    c.drawString(100,162,"Founder, Imagination Applied  ·  AI Transformation Consulting")
    c.setFillColor(MID); c.setFont("Helvetica",18)
    c.drawString(100,132,"linkedin.com/in/josh-penzell")
    c.drawRightString(W-100,132,"joshpenzell.com")

# ── BUILD ─────────────────────────────────────────────────────────────────────
import os
os.makedirs("/home/claude/carousel", exist_ok=True)

c = canvas.Canvas(OUT, pagesize=(W,H))
slide_1(c); new_page(c)
slide_2(c); new_page(c)
slide_3(c); new_page(c)
slide_4(c); new_page(c)
slide_5(c); new_page(c)
slide_6(c); new_page(c)
slide_7(c); new_page(c)
slide_8(c)
c.save()
print(f"Done: {OUT}")
