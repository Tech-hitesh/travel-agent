from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1400, 1600
img = Image.new("RGB", (W, H), "#0f172a")
d = ImageDraw.Draw(img)

# ── font helpers ──────────────────────────────────────────────────────────
def font(size, bold=False):
    candidates_bold = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
    ]
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/verdana.ttf",
    ]
    pool = candidates_bold if bold else candidates
    for path in pool:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def text(x, y, txt, color, size=14, bold=False, anchor="lt"):
    d.text((x, y), txt, font=font(size, bold), fill=color, anchor=anchor)

def rect(x, y, w, h, fill, radius=14, border=None, bwidth=2):
    d.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill,
                         outline=border, width=bwidth)

def pill(x, y, w, h, fill, txt, tcolor, tsize=11, bold=True):
    d.rounded_rectangle([x, y, x+w, y+h], radius=h//2, fill=fill)
    text(x + w//2, y + h//2, txt, tcolor, tsize, bold, anchor="mm")

def hline(x1, y1, x2, y2, color, width=2):
    d.line([(x1,y1),(x2,y2)], fill=color, width=width)

def arrow_down(x, ytop, ybot, color, label="", lcolor="#7dd3fc", lsize=12):
    d.line([(x, ytop), (x, ybot-10)], fill=color, width=2)
    d.polygon([(x-8, ybot-10),(x+8, ybot-10),(x, ybot)], fill=color)
    if label:
        tw = d.textlength(label, font=font(lsize))
        rx = x - tw//2 - 12
        ry = (ytop + ybot)//2 - 13
        d.rounded_rectangle([rx, ry, rx+tw+24, ry+26], radius=13, fill="#111827", outline="#1e293b", width=1)
        text(rx+12+tw//2, ry+13, label, lcolor, lsize, anchor="mm")

def dashed_arrow_up(x, ytop, ybot, color, label="", lsize=11):
    for i in range(ytop, ybot, 14):
        seg_end = min(i+8, ybot)
        d.line([(x, i),(x, seg_end)], fill=color, width=2)
    d.polygon([(x-7, ytop+10),(x+7, ytop+10),(x, ytop)], fill=color)
    if label:
        tw = d.textlength(label, font=font(lsize))
        text(x+14, (ytop+ybot)//2, label, color, lsize, anchor="lm")

# ════════════════════════════════════════════════════════════════════
# TITLE
# ════════════════════════════════════════════════════════════════════
text(W//2, 30, "✈  Aria — AI Travel Planner Agent", "#f1f5f9", 28, bold=True, anchor="mt")
text(W//2, 70, "Architecture Blueprint  ·  IBM Granite on watsonx.ai  ·  Node.js + Express", "#64748b", 16, anchor="mt")
d.line([(60, 96),(W-60, 96)], fill="#1e293b", width=1)

# ════════════════════════════════════════════════════════════════════
# LAYER 1 — BROWSER
# ════════════════════════════════════════════════════════════════════
LY1 = 112
rect(30, LY1, W-60, 290, "#0e2030", radius=18, border="#1e4060", bwidth=2)
pill(48, LY1+14, 320, 26, "#0ea5e933", "🌐  LAYER 1 — BROWSER (FRONTEND)", "#7dd3fc", 12, bold=True)

# 4 feature cards
card_w, card_h = 290, 220
cards = [
    ("💬 Chat Planner",   "#7dd3fc", "#0f2e4a", "#1e4f6e",
     ["• Conversational AI chat", "• Markdown rendering", "• Message history", "• Typing indicator", "• Quick chip shortcuts"]),
    ("📋 Trip Builder",   "#7dd3fc", "#0f2e4a", "#1e4f6e",
     ["• Form-based planner", "• Destination + duration", "• Budget & style chips", "• Builds AI prompt", "• Validation + spinner"]),
    ("🗺️ Destinations",   "#7dd3fc", "#0f2e4a", "#1e4f6e",
     ["• 12 destination cards", "• Dynamic DOM render", "• One-click AI guide", "• Hover animations", "• Scrollable grid"]),
    ("💰 Budget Estimator","#7dd3fc", "#0f2e4a", "#1e4f6e",
     ["• Instant cost calculator", "• Dest-aware multipliers", "• Animated progress bars", "• 3 budget levels", "• Ask AI breakdown"]),
]
cx = 48
for title, tc, bg, border, lines in cards:
    rect(cx, LY1+52, card_w, card_h, bg, radius=12, border="#0ea5e9", bwidth=2)
    rect(cx, LY1+52, card_w, 36, "#0ea5e920", radius=12)
    text(cx+card_w//2, LY1+52+18, title, tc, 15, bold=True, anchor="mm")
    for i, ln in enumerate(lines):
        text(cx+14, LY1+100+i*26, ln, "#94a3b8", 12)
    pill(cx+14, LY1+52+card_h-26, 90, 20, "#0ea5e930", "HTML/CSS/JS", "#7dd3fc", 10)
    cx += card_w + 14

# ════════════════════════════════════════════════════════════════════
# ARROW 1 → 2
# ════════════════════════════════════════════════════════════════════
A1Y_TOP = LY1 + 290
A1Y_BOT = A1Y_TOP + 80
arrow_down(W//2 - 60, A1Y_TOP, A1Y_BOT,
           "#0ea5e9", "  POST /api/chat   ·   { messages: [ ] }   ·   JSON", "#7dd3fc", 13)
dashed_arrow_up(W//2 + 70, A1Y_TOP+8, A1Y_BOT-8, "#475569", "{ reply }", 11)

# ════════════════════════════════════════════════════════════════════
# LAYER 2 — SERVER
# ════════════════════════════════════════════════════════════════════
LY2 = A1Y_BOT + 10
rect(30, LY2, W-60, 300, "#0e0a28", radius=18, border="#3b2a6e", bwidth=2)
pill(48, LY2+14, 380, 26, "#8b5cf633", "⚙️  LAYER 2 — NODE.JS + EXPRESS BACKEND (server.js)", "#c4b5fd", 12, bold=True)

srv_cards = [
    ("🔀 Express Router",    "#c4b5fd", "#130d30", "#8b5cf6",
     ["POST /api/chat", "GET  /api/health", "GET  /api/test", "GET  * → index.html", "CORS + JSON parser"]),
    ("🔑 IAM Token Cache",   "#c4b5fd", "#130d30", "#8b5cf6",
     ["• API key → Bearer token", "• Cache for 55 minutes", "• Auto-refresh on expiry", "• Key stays server-side", "• Never reaches browser"]),
    ("🤖 System Prompt",     "#c4b5fd", "#130d30", "#8b5cf6",
     ["• Aria persona definition", "• Dest + itinerary expert", "• Budget / visa / weather", "• Injected every request", "• max_tokens: 2048"]),
    ("📄 .env Config",       "#fcd34d", "#1c1207", "#f59e0b",
     ["WATSONX_API_KEY", "WATSONX_PROJECT_ID", "WATSONX_MODEL_ID", "WATSONX_URL", "PORT"]),
]
cx = 48
for title, tc, bg, border, lines in srv_cards:
    rect(cx, LY2+52, card_w, card_h, bg, radius=12, border=border, bwidth=2)
    rect(cx, LY2+52, card_w, 36, border+"33", radius=12)
    text(cx+card_w//2, LY2+52+18, title, tc, 15, bold=True, anchor="mm")
    for i, ln in enumerate(lines):
        text(cx+14, LY2+100+i*26, ln, "#94a3b8", 12)
    cx += card_w + 14

# ════════════════════════════════════════════════════════════════════
# ARROW 2 → 3
# ════════════════════════════════════════════════════════════════════
A2Y_TOP = LY2 + 300
A2Y_BOT = A2Y_TOP + 80
arrow_down(W//2 - 60, A2Y_TOP, A2Y_BOT,
           "#8b5cf6", "  Bearer Token  +  model_id  +  project_id  +  messages[ ]", "#c4b5fd", 13)
dashed_arrow_up(W//2 + 70, A2Y_TOP+8, A2Y_BOT-8, "#475569", "choices[0]", 11)

# ════════════════════════════════════════════════════════════════════
# LAYER 3 — IBM CLOUD
# ════════════════════════════════════════════════════════════════════
LY3 = A2Y_BOT + 10
rect(30, LY3, W-60, 270, "#071810", radius=18, border="#166534", bwidth=2)
pill(48, LY3+14, 320, 26, "#22c55e33", "☁️  LAYER 3 — IBM CLOUD / WATSONX.AI", "#86efac", 12, bold=True)

ibm_cards = [
    ("🔐 IBM IAM Service",  "#86efac", "#071810", "#22c55e",
     ["iam.cloud.ibm.com", "• API key → Bearer token", "• OAuth2 client creds", "• Token TTL: 3600s", "• IBM Identity service"]),
    ("🧠 IBM Granite Model","#86efac", "#071810", "#22c55e",
     ["ibm/granite-4-h-small", "• Chat completions API", "• max_new_tokens: 2048", "• temperature: 0.7", "• top_p: 0.9"]),
    ("📁 watsonx Project",  "#86efac", "#071810", "#22c55e",
     ["ID: 0f3d281a-1ef9…", "• Scoped model access", "• Usage tracking", "• Billing & limits", "• us-south region"]),
]
ibm_w = (W - 96 - 28) // 3
cx = 48
for title, tc, bg, border, lines in ibm_cards:
    rect(cx, LY3+52, ibm_w, 190, bg, radius=12, border=border, bwidth=2)
    rect(cx, LY3+52, ibm_w, 36, border+"33", radius=12)
    text(cx+ibm_w//2, LY3+52+18, title, tc, 15, bold=True, anchor="mm")
    for i, ln in enumerate(lines):
        text(cx+14, LY3+100+i*25, ln, "#94a3b8", 12)
    pill(cx+14, LY3+52+190-28, 90, 20, border+"40", "IBM Cloud", tc, 10)
    cx += ibm_w + 14

# ════════════════════════════════════════════════════════════════════
# REQUEST FLOW
# ════════════════════════════════════════════════════════════════════
FY = LY3 + 270 + 24
d.line([(60, FY),(W-60, FY)], fill="#1e293b", width=1)
text(W//2, FY+16, "📡  REQUEST FLOW", "#475569", 13, bold=True, anchor="mm")

flow_steps = [
    ("1", "#0ea5e9", "User Clicks",   "Card / chip / types"),
    ("2", "#0ea5e9", "fetch()",       "POST /api/chat"),
    ("3", "#8b5cf6", "IAM Token",     "Cache or refresh"),
    ("4", "#22c55e", "watsonx Call",  "POST to IBM Granite"),
    ("5", "#22c55e", "AI Response",   "choices[0].content"),
    ("6", "#0ea5e9", "Render Chat",   "Markdown → HTML"),
]
sw = (W - 60) // 6
fx = 30
FBY = FY + 34
for num, color, title, sub in flow_steps:
    bx, by, bw, bh = fx, FBY, sw-8, 90
    rect(bx, by, bw, bh, "#0a1525", radius=10, border=color, bwidth=2)
    d.ellipse([bx+12, by+12, bx+40, by+40], fill=color)
    text(bx+26, by+26, num, "#fff", 14, bold=True, anchor="mm")
    text(bx+50, by+20, title, "#e2e8f0", 13, bold=True)
    text(bx+14, by+52, sub, "#64748b", 11)
    if fx + sw < W - 30:
        ax = bx + bw + 4
        ay = by + bh//2
        d.polygon([(ax,ay-6),(ax+8,ay),(ax,ay+6)], fill=color)
    fx += sw

# ════════════════════════════════════════════════════════════════════
# FILE STRUCTURE
# ════════════════════════════════════════════════════════════════════
FSY = FBY + 110
d.line([(60, FSY),(W-60, FSY)], fill="#1e293b", width=1)
text(W//2, FSY+16, "📁  PROJECT FILE STRUCTURE", "#475569", 13, bold=True, anchor="mm")

rect(30, FSY+36, W-60, 150, "#080d18", radius=12, border="#1e293b", bwidth=1)
files = [
    ("travel-agent/",           "#7dd3fc",  True,  ""),
    ("  ├── server.js",         "#e2e8f0",  False, "← Express backend · IBM watsonx proxy · IAM token cache"),
    ("  ├── .env",              "#fcd34d",  False, "← API key · project ID · model ID  (secret)"),
    ("  ├── start.bat",         "#e2e8f0",  False, "← One-click launcher · auto-kills port 3000 · opens browser"),
    ("  ├── package.json",      "#e2e8f0",  False, "← express · axios · cors · dotenv"),
    ("  └── public/index.html", "#7dd3fc",  False, "← Full SPA · 4 tabs · Chat · Builder · Destinations · Budget"),
]
for i, (name, nc, bold, comment) in enumerate(files):
    ty = FSY + 54 + i * 22
    text(50, ty, name, nc, 13, bold=bold)
    if comment:
        text(50 + d.textlength(name, font=font(13, bold)) + 20, ty, comment, "#475569", 12)

# ════════════════════════════════════════════════════════════════════
# LEGEND
# ════════════════════════════════════════════════════════════════════
LEY = FSY + 200
d.line([(60, LEY),(W-60, LEY)], fill="#1e293b", width=1)
legend = [
    ("#0ea5e9", "Frontend (Browser)"),
    ("#8b5cf6", "Backend (Node.js)"),
    ("#22c55e", "IBM Cloud (watsonx)"),
    ("#f59e0b", "Configuration (.env)"),
    ("#475569", "── ──  Response path"),
]
lx = (W - sum(d.textlength(lb, font=font(13))+90 for _,lb in legend)) // 2
for color, label in legend:
    d.rounded_rectangle([lx, LEY+14, lx+18, LEY+32], radius=4, fill=color)
    text(lx+26, LEY+23, label, "#94a3b8", 13, anchor="lm")
    lx += int(d.textlength(label, font=font(13))) + 50

# footer
text(W//2, H-20, "Made with IBM Bob", "#334155", 12, anchor="mm")

# ════════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════════
out = "architecture_diagram.jpg"
img.save(out, "JPEG", quality=95)
print(f"Saved: {os.path.abspath(out)}  ({W}x{H}px)")
