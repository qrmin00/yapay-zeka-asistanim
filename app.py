
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
IMAGE_MODEL = "gemini-3.1-flash-image"

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# PEMBE TASARIM
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
.stButton button {
    background: #ff69b4;
    color: white;
    border-radius: 15px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ÜST TASARIM
sol, sag = st.columns([1, 2])

with sol:
    st.markdown('<div class="kitty-area">', unsafe_allow_html=True)
    try:
        st.image("hello.png", use_container_width=True)
    except Exception:
        st.warning("hello.png dosyasını uygulama klasörüne koy.")
    st.markdown('</div>', unsafe_allow_html=True)

with sag:
    st.markdown(
        "<h1 style='text-align:right;'>Yapay Zeka Asistanım 💕</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:right;'>Seninle konuşmaya hazırım...</p>",
        unsafe_allow_html=True
    )

st.divider()

# FOTOĞRAF KÜÇÜLTME
def kucult(dosya):
    resim = Image.open(dosya).convert("RGB")
    resim.thumbnail((1024, 1024))
    tampon = io.BytesIO()
    resim.save(tampon, format="JPEG", quality=85)
    return tampon.getvalue()

# SEKME AYARLARI
sohbet, fotograf = st.tabs([
    "💬 Yapay Zeka Sohbet",
    "🎨 Fotoğraf Düzenle"
])

# SOHBET
with sohbet:

    st.subheader("💕 Benimle Sohbet Et")

    if "mesajlar" not in st.session_state:
        st.session_state.mesajlar = []

    for m in st.session_state.mesajlar:
        with st.chat_message(m["rol"]):
            for r in m["resimler"]:
                st.image(r, width=300)
            st.write(m["metin"])

    girdi = st.chat_input(
        "Bir şey yaz veya fotoğraf ekle... 💗",
        accept_file=True,
        file_type=["jpg", "jpeg", "png", "webp"],
    )

    if girdi:
        soru = girdi.text or ""
        resimler = [kucult(d) for d in girdi.files]

        if not soru and resimler:
            soru = "Bu fotoğrafı analiz et."

        st.session_state.mesajlar.append({
            "rol": "user",
            "metin": soru,
            "resimler": resimler
        })

        with st.chat_message("user"):
            for r in resimler:
                st.image(r, width=300)
            st.write(soru)

        gecmis = []

        for m in st.session_state.mesajlar:
            parcalar = [
                types.Part.from_bytes(
                    data=r,
                    mime_type="image/jpeg"
                )
                for r in m["resimler"]
            ]

            parcalar.append(
                types.Part.from_text(text=m["metin"])
            )

            rol = "user" if m["rol"] == "user" else "model"

            gecmis.append(
                types.Content(role=rol, parts=parcalar)
            )

        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum... 💗"):
                try:
                    cevap = client.models.generate_content(
                        model=MODEL,
                        contents=gecmis
                    )
                    metin = cevap.text or "Bir cevap oluşturamadım."
                except Exception as hata:
                    metin = "Bir hata oluştu: " + str(hata)

            st.write(metin)

        st.session_state.mesajlar.append({
            "rol": "assistant",
            "metin": metin,
            "resimler": []
        })


# FOTOĞRAF DÜZENLEME
with fotograf:

    st.subheader("🎀 AI Fotoğraf Düzenleyici")
    st.write(
        "Fotoğrafını yükle ve nasıl değiştirmek istediğini anlat. "
        "Yapay zekâm istediğin değişiklikleri yapmaya çalışsın. 💗"
    )

    yuklenen = st.file_uploader(
        "📸 Fotoğrafını buraya yükle",
        type=["jpg", "jpeg", "png", "webp"],
        key="duzenleme_fotografi"
    )

    if yuklenen:

        orijinal = Image.open(yuklenen).convert("RGB")

        st.image(
            orijinal,
            caption="Yüklediğin fotoğraf",
            use_container_width=True
        )

        talimat = st.text_area(
            "✨ Fotoğrafta ne değiştirmek istiyorsun?",
            placeholder=(
                "Örneğin: Arka plana gün batımı ekle. "
                "Yüzümü ve kıyafetimi değiştirme."
            ),
            height=120
        )

        if st.button(
            "💗 Fotoğrafımı Düzenle",
            use_container_width=True
        ):

            if not talimat.strip():
                st.warning("Önce ne değiştirmek istediğini yaz.")
            else:

                with st.spinner("Fotoğrafın düzenleniyor... 🎀"):

                    try:

                        cevap = client.models.generate_content(
                            model=IMAGE_MODEL,
                            contents=[
                                types.Part.from_text(
                                    text=(
                                        "Edit this uploaded photograph "
                                        "according to the user's instructions. "
                                        "Preserve the original person's identity "
                                        "and facial features unless explicitly "
                                        "asked otherwise. Make realistic edits. "
                                        "Return the edited image. "
                                        "User instructions: " + talimat
                                    )
                                ),
                                types.Part.from_bytes(
                                    data=kucult(yuklenen),
                                    mime_type="image/jpeg"
                                )
                            ],
                            config=types.GenerateContentConfig(
                                response_modalities=["TEXT", "IMAGE"]
                            )
                        )

                        duzenlenmis = None
                        aciklama = ""

                        for parca in cevap.parts:
                            if parca.text:
                                aciklama += parca.text

                            if parca.inline_data:
                                duzenlenmis = parca.as_image()
                                break

                        if duzenlenmis:

                            st.success("Fotoğrafın hazır! 💕")

                            st.image(
                                duzenlenmis,
                                caption="Düzenlenmiş fotoğrafın",
                                use_container_width=True
                            )

                            tampon = io.BytesIO()
                            duzenlenmis.save(tampon, format="PNG")

                            st.download_button(
                                "📥 Fotoğrafı İndir",
                                data=tampon.getvalue(),
                                file_name="duzenlenmis_fotograf.png",
                                mime="image/png",
                                use_container_width=True
                            )

                        else:
                            st.error(
                                "Görsel oluşturulamadı. "
                                "Model açıklaması:"
                            )
                            st.write(aciklama or "Model görsel döndürmedi.")

                    except Exception as hata:

                        st.error("Bir hata oluştu:")
                        st.code(str(hata))

                        st.info(
                            "Görsel modelinin API anahtarında "
                            "kullanılabilir olduğunu ve kotanı kontrol et."
                        )

    else:
        st.info("Başlamak için yukarıdan fotoğraf yükle. 💗")
