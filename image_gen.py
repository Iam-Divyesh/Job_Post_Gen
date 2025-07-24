import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# === CONFIG ===
TEMPLATE_PATH = "./template/Job_Post_TEMP.png"
FONT_BOLD_ITALIC = "fonts/Montserrat-ExtraBoldItalic.ttf"
FONT_REGULAR = "fonts/Montserrat-Regular.ttf"
FONT_SEMIBOLD = "fonts/Montserrat-SemiBold.ttf"

st.set_page_config(page_title="Job Image Generator")
st.title("📌 Job Post Image Designer")

# === Load Template ===
template = Image.open(TEMPLATE_PATH)

# === Input Fields ===



role = st.text_input("Job Role", placeholder="Python Developer")
skills = st.text_area("Required Skills (comma-separated)", placeholder="Python, Django, APIs")
contact = st.text_input("Contact Number", placeholder="+91 9016768065")
email = st.text_input("Email Address", placeholder="divyeshsarvaiya2@gmail.com")
location = st.text_input("Job Location", placeholder="Surat")
logo_file = st.file_uploader("Upload Logo Image", type=["png", "jpg", "jpeg", "webp"])

# === SIDEBAR CONTROLS ===
st.sidebar.header("🎛️ Logo Adjustment Only")
logo_x = st.sidebar.slider("Logo X Position", 0, 1000, 200)
logo_y = st.sidebar.slider("Logo Y Position", 0, 1000, 100)
logo_size = st.sidebar.slider("Size", 0.0, 1000.0, 300.0)

# === Static Text Settings ===
role_x, role_y, role_font_size = 210, 1050, 100
skills_x, skills_y, skills_font_size = 210, 1200, 70
contact_x, contact_y, contact_font_size = 200, 1680, 36
email_x, email_y, email_font_size = 200, 1730, 36
location_x, location_y, location_font_size = 200, 1780, 36

# === Validate Required Fields ===
if not all([role.strip(), skills.strip(), contact.strip(), email.strip(), location.strip(), logo_file]):
    st.error("⚠️ Please fill in all fields and upload the logo to generate and download the image.")
else:
    # === Create Canvas ===
    canvas = template.copy()
    draw = ImageDraw.Draw(canvas)

    # === Load Fonts ===
    font_role = ImageFont.truetype(FONT_BOLD_ITALIC, role_font_size)
    font_skills_bold = ImageFont.truetype(FONT_SEMIBOLD, skills_font_size)
    font_skills_normal = ImageFont.truetype(FONT_REGULAR, skills_font_size)
    font_contact = ImageFont.truetype(FONT_REGULAR, contact_font_size)
    font_email = ImageFont.truetype(FONT_REGULAR, email_font_size)
    font_location = ImageFont.truetype(FONT_REGULAR, location_font_size)

    # === Draw Text ===
    draw.text((role_x, role_y), role, font=font_role, fill="black")
    draw.text((skills_x, skills_y), "Skills:", font=font_skills_bold, fill="#3c83bb")

    label_bbox = draw.textbbox((0, 0), "Skills:", font=font_skills_bold)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text((skills_x + label_width + 10, skills_y), skills, font=font_skills_normal, fill="black")

    draw.text((contact_x, contact_y), contact, font=font_contact, fill="black")
    draw.text((email_x, email_y), email, font=font_email, fill="black")
    draw.text((location_x, location_y), location, font=font_location, fill="black")

    # === Add Uploaded Logo (preserving aspect ratio) ===
    try:
        logo = Image.open(logo_file).convert("RGBA")
        orig_w, orig_h = logo.size
        scale = min(logo_size / orig_w, logo_size / orig_h, 1.0)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        logo = logo.resize((new_w, new_h), Image.LANCZOS)
        canvas.paste(logo, (logo_x, logo_y), logo)
    except Exception as e:
        st.warning("⚠️ Couldn't load uploaded logo")
        st.text(f"Error: {e}")

    # === Show & Download ===
    st.image(canvas, caption="✅ Generated Job Post", use_column_width=True)

    buffered = BytesIO()
    canvas.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    st.download_button(
        label="📥 Download Image",
        data=img_bytes,
        file_name="job_post.png",
        mime="image/png"
    )
