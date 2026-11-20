```python
import io
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Yapay Zeka Asistanım",
    page_icon="🎀",
    layout="wide"
)

MODEL = "gemini-3.5-flash-lite"

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Pembe tasarım
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 15%, #ffd6ed 0%, transparent 30%),
        radial-gradient(circle at 90% 10%, #ffc1e3 0%, transparent 28%),
        linear-gradient(135deg, #ffe6f3, #fbc8e4, #f8dff3);
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.kitty-area {
    background: rgba(255,255,255,0.48);
    border: 2px solid #ffadd8;
    border-radius: 28px;
    padding: 15px;
    text-align: center;
    min-height: 230px;
    box-shadow: 0 8px 25px #e88abd44;
}

.chat-area {
    background: rgba(255,255,255,0.55);
    border: 1px solid #ffb8dc;
    border-radius: 22px;
    padding: 15px;
}

h1, h2, h3, p {
    color: #a52a69;
}

[data-testid="stChatInput"] {
    border: 2px solid #f28cbd;
    border-radius: 18px;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.55);
    border-radius: 18px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Üst tasarım
sol, sag = st.columns([1, 2])

with sol:
    st.markdown(
        '<div class="kitty-area">',
        unsafe_allow_html=True
    )

    try:
        st.image("hello.png", use_container_width=True)
    except Exception:
        st.warning("hello.png dosyasını uygulama klasörüne koy.")

    st.markdown("</div>", unsafe_allow_html=True)

with sag:
    st.markdown(
        "<h2 style='text-align:right;'>Yapay Zeka Asistanım 💕</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:right;'>Seninle konuşmaya hazırım...</p>",
        unsafe_allow_html=True
    )

st.divider()

# Fotoğraf küçültme
def kucult(dosya):
    resim = Image.open(dosya).convert("RGB")
    resim.thumbnail((1024, 1024))

    tampon = io.BytesIO()
    resim.save(tampon, format="JPEG", quality=85)

    return tampon.getvalue()

# Sohbet geçmişi
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

for m in st.session_state.mesajlar:
    with st.chat_message(m["rol"]):
        for r in
