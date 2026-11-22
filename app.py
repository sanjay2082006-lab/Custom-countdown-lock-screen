import streamlit as st
from datetime import datetime, date, timedelta
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="T-Minus Countdown Lock Screen", page_icon="⏳", layout="centered")

st.title("⏳ T-Minus Countdown & Lock Screen Generator")
st.write("Plan your deadline milestones and generate a custom 9:16 phone lock screen.")

# --- 1. INPUTS ---
col1, col2 = st.columns(2)
with col1:
    goal_name = st.text_input("Goal / Deadline Name", value="Final Exam Prep")
with col2:
    target_date = st.date_input("Target Date", value=date.today() + timedelta(days=14), min_value=date.today())

theme = st.selectbox("Lock Screen Theme", ["Midnight Dark", "Ocean Slate", "Minimalist Light", "Forest Calm"])

# --- 2. LIVE COUNTDOWN ---
days_left = (target_date - date.today()).days
st.markdown("---")
st.subheader(f"🎯 Target: {goal_name}")
st.metric(label="Days Remaining", value=f"{days_left} Days", delta=f"Target: {target_date.strftime('%b %d, %Y')}")

# --- 3. T-MINUS MILESTONES ---
st.markdown("### 📋 T-Minus Milestones (Under 5 words each)")
st.caption("Edit your milestones and check them off as you progress:")

default_milestones = [
    ("T-14", "Outline core topics & plan"),
    ("T-7", "Complete first full practice"),
    ("T-3", "Review weak areas thoroughly"),
    ("T-1", "Final light revision & rest"),
]

milestones = []
for tag, default_task in default_milestones:
    c1, c2, c3 = st.columns([0.12, 0.2, 0.68])
    with c1:
        checked = st.checkbox("", key=f"chk_{tag}")
    with c2:
        st.markdown(f"**{tag}**")
    with c3:
        task = st.text_input(f"Task for {tag}", value=default_task, key=f"txt_{tag}", label_visibility="collapsed")
    m_date = target_date - timedelta(days=int(tag.replace("T-", "")))
    milestones.append((tag, m_date.strftime("%b %d"), task, checked))

# --- 4. LOCK SCREEN IMAGE GENERATOR (9:16 - 1080x1920) ---
def create_lockscreen(goal, days, target_dt, items, selected_theme):
    W, H = 1080, 1920
    themes = {
        "Midnight Dark": {"bg": (18, 20, 28), "card": (30, 34, 46), "text": (245, 247, 250), "accent": (99, 179, 237), "muted": (160, 174, 192)},
        "Ocean Slate": {"bg": (15, 32, 39), "card": (32, 58, 67), "text": (255, 255, 255), "accent": (72, 209, 204), "muted": (180, 210, 215)},
        "Minimalist Light": {"bg": (244, 245, 247), "card": (255, 255, 255), "text": (26, 32, 44), "accent": (49, 130, 206), "muted": (113, 128, 150)},
        "Forest Calm": {"bg": (22, 36, 28), "card": (35, 56, 44), "text": (240, 248, 242), "accent": (104, 211, 145), "muted": (165, 195, 175)},
    }
    t = themes[selected_theme]
    img = Image.new("RGB", (W, H), color=t["bg"])
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 46)
        font_days = ImageFont.truetype("DejaVuSans-Bold.ttf", 96)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 34)
        font_item = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 28)
    except:
        font_title = font_days = font_sub = font_item = font_small = ImageFont.load_default()

    # Top space left clean (y = 0 to 520) for phone clock & notifications
    y = 540
    draw.text((90, y), "T-MINUS COUNTDOWN:", fill=t["accent"], font=font_sub)
    y += 50
    draw.text((90, y), goal.upper()[:28], fill=t["text"], font=font_title)
    y += 85
    draw.text((90, y), f"{days} DAYS LEFT", fill=t["accent"], font=font_days)
    y += 120
    draw.text((90, y), f"Target Date: {target_dt.strftime('%B %d, %Y')}", fill=t["muted"], font=font_sub)
    y += 90

    # Milestone Cards
    for tag, m_dt, task, done in items:
        card_top = y
        card_bottom = y + 165
        draw.rounded_rectangle([(80, card_top), (W - 80, card_bottom)], radius=28, fill=t["card"])

        # Checkbox
        box_x, box_y = 125, card_top + 55
        draw.rectangle([(box_x, box_y), (box_x + 48, box_y + 48)], outline=t["accent"], width=4)
        if done:
            draw.line([(box_x + 10, box_y + 24), (box_x + 22, box_y + 38), (box_x + 40, box_y + 12)], fill=t["accent"], width=5)

        # Text
        draw.text((205, card_top + 35), f"{tag}  •  {m_dt}", fill=t["accent"], font=font_small)
        draw.text((205, card_top + 82), task[:34], fill=t["text"], font=font_item)
        y += 195

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

st.markdown("---")
st.subheader("📱 Lock Screen Preview & Download")
lockscreen_bytes = create_lockscreen(goal_name, days_left, target_date, milestones, theme)

st.image(lockscreen_bytes, caption="9:16 Phone Lock Screen (Top space reserved for clock)", width=300)

st.download_button(
    label="⬇️ Download Lock Screen PNG",
    data=lockscreen_bytes,
    file_name="countdown_lockscreen.png",
    mime="image/png"
                       )
