Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo.
![print do app](https://github.com/user-attachments/assets/a91a1e48-5968-440c-9fd1-5f3cf0ca2972)

👨🏼‍🏫 Ary Slides! 📺

Um aplicativo web construído com Streamlit que permite fazer upload de arquivos .ppt e .pptx, convertê-los para imagens e apresentar os slides diretamente no navegador, em tela cheia.

Funcionalidades

- Upload de arquivos .ppt/.pptx
- Conversão para PDF usando LibreOffice
- Conversão de PDF em imagens com `pdf2image`
- Apresentação dos slides em tela cheia com controle por teclado e mouse
- Interface estilizada com HTML e CSS customizados

Como executar

1. Clone este repositório:
    ```bash
    git clone https://github.com/aryribeiro/ary-slides.git
    cd ary-slides
    ```

2. (Opcional) Crie e ative um ambiente virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate   # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute a aplicação:
    ```bash
    streamlit run app.py
    ```

Requisitos

- Python 3.8+
- LibreOffice instalado e disponível no PATH (para converter PPT/PPTX em PDF)
- Poppler instalado (necessário para `pdf2image` funcionar)

Controles da Apresentação

- Clique no botão "APRESENTAR!" para iniciar em tela cheia
- Use as setas do teclado (⯇ ⯈) para navegar entre os slides
- Clique com o botão esquerdo para voltar e botão direito para avançar

Observações

- Slides protegidos por senha ou com erro na conversão serão ignorados.
