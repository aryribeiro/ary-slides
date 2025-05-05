import streamlit as st
import subprocess
import os
from pdf2image import convert_from_path
import base64
from io import BytesIO
import json
import hashlib

@st.cache_data
def convert_pptx_to_images(pptx_file, file_id):
    try:
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", pptx_file, "--outdir", "."],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        pdf_file = pptx_file.replace(".pptx", ".pdf").replace(".ppt", ".pdf")
        return convert_from_path(pdf_file, dpi=150)
    except:
        return None

st.set_page_config(page_title="Ary Slides!", page_icon="👨🏼‍🏫", layout="wide")
st.title("...👨🏼‍🏫 Ary Slides! 📺")

st.markdown("""
<style>
html, body {
    margin: 0;
    padding: 0;
    height: 90%;
    overflow: hidden;
}
.stApp {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.stFileUploader {
    border: 2px dashed #1a73e8;
    border-radius: 5px;
    padding: 10px;
    background: #f5f6fa;
    max-width: 420px;  /* reduzido 30% */
}
.stButton > button {
    background: #1a73e8;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.3s, transform 0.1s;
}
.stButton > button:hover {
    background: #1557b0;
    transform: scale(1.05);
}
.container {
    text-align: center;
    margin: 20px 0;
}
#slide-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    z-index: 999;
}
#slide-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    display: block;
    margin: 0 auto;  /* Centraliza horizontalmente */
}
#caption-text {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: #fff;
    font-size: 24px;
    font-weight: 500;
    background: rgba(0, 0, 0, 0.3);
    padding: 5px 10px;
    border-radius: 5px;
    z-index: 1001;
}
</style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Faça upload do arquivo clicando aqui!", type=["ppt", "pptx"])
if uploaded_file:
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    tmp = f"temp{ext}"
    
    # Ler o conteúdo do arquivo e gerar um hash único
    file_content = uploaded_file.read()
    file_id = hashlib.md5(file_content).hexdigest()
    
    # Resetar o ponteiro do arquivo e salvar no disco
    uploaded_file.seek(0)
    with open(tmp, "wb") as f:
        f.write(file_content)

    images = convert_pptx_to_images(tmp, file_id=file_id)
    if images:
        b64 = []
        for img in images:
            buf = BytesIO()
            img.save(buf, format="PNG")
            b64.append(base64.b64encode(buf.getvalue()).decode())
        data = json.dumps(b64)

        html = f"""
        <div class="container"><button id="start">APRESENTAR!</button></div>
        <div id="slide-container">
            <img id="slide-image" src="" alt="Slide">
            <div id="caption-text"></div>
        </div>
        <script>
            const imgs = {data};
            let idx = 0;
            const imgEl = document.getElementById('slide-image');
            const cap = document.getElementById('caption-text');
            const cont = document.getElementById('slide-container');
            const startBtn = document.getElementById('start');

            function upd() {{
                imgEl.src = 'data:image/png;base64,' + imgs[idx];
                cap.innerText = `Slide ${{idx+1}} / ${{imgs.length}}`;
            }}
            function prev() {{ if(idx>0) {{ idx--; upd(); }} }}
            function next() {{ if(idx<imgs.length-1) {{ idx++; upd(); }} }}

            document.addEventListener('keydown', e => {{
                if(e.key==='ArrowLeft') {{ e.preventDefault(); prev(); }}
                if(e.key==='ArrowRight') {{ e.preventDefault(); next(); }}
            }});
            cont.addEventListener('mousedown', e => {{
                e.preventDefault(); if(e.button===0) prev(); if(e.button===2) next();
            }});
            cont.addEventListener('contextmenu', e => e.preventDefault());

            startBtn.onclick = () => {{ document.documentElement.requestFullscreen(); }};
            document.addEventListener('fullscreenchange', () => {{
                startBtn.style.display = document.fullscreenElement ? 'none' : 'block';
                upd();
            }});

            upd();
        </script>
        """
        st.components.v1.html(html, height=900, scrolling=False)
    else:
        st.error("Slides com Senha. Ou, defeito...")
    os.remove(tmp)
    pdf_tmp = tmp.replace(ext, ".pdf")
    if os.path.exists(pdf_tmp): os.remove(pdf_tmp)

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #333333;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Esconde completamente todos os elementos da barra padrão do Streamlit */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    /* Remove qualquer espaço em branco adicional */
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Remove quaisquer margens extras */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)