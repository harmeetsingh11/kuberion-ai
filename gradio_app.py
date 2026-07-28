"""
Professional Gradio interface for Kuberion AI.
"""

from __future__ import annotations

import time

from monitoring.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
)
import gradio as gr
from prometheus_client import start_http_server
from app.container import get_service

service = get_service()

QUESTION_HISTORY: list[str] = []

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

.gradio-container{
    max-width:1650px!important;
    margin:auto!important;
    padding:0!important;
}

.gr-chatbot{
    border-radius:20px!important;
    border:1px solid #243244!important;
}

button{
    border-radius:14px!important;
    font-weight:700!important;
    transition:.25s;
}

button:hover{
    transform:translateY(-2px);
}

textarea,
input{
    font-size:16px!important;
}


#sidebar{
    background:#111827;
    border-radius:18px;
    padding:20px;
    border:1px solid #243244;
}

.block{
    border-radius:18px!important;
    border:1px solid #243244!important;
    background:#111827!important;
}

.gr-textbox{
    border-radius:16px!important;
}

.gr-button-primary{
    height:54px!important;
}

.gr-button-primary{
    height:54px!important;
}

.gr-textbox textarea{
    min-height:54px!important;
}



.gr-chatbot{
    border-radius:20px!important;
    border:1px solid #243244!important;
}

button{
    border-radius:14px!important;
    font-weight:700!important;
}

button:hover{
    transform:translateY(-2px);
}

textarea{
    border-radius:14px!important;
}

.gr-button-primary{
    height:56px!important;
}

.gr-textbox textarea{
    min-height:56px!important;
}

.gradio-container{
    max-width:1500px!important;
    margin:auto!important;
    font-family:'Manrope',sans-serif!important;
    font-size:17px!important;
}

.markdown{
    font-size:17px!important;
}

.gr-chatbot{
    font-size:17px!important;
}

textarea,
input{
    font-size:17px!important;
}

button{
    font-size:16px!important;
    font-weight:700!important;
}

::-webkit-scrollbar-thumb{
    background:#3b82f6;
}

::-webkit-scrollbar-thumb:hover{
    background:#2563eb;
}

.gr-chatbot{
    font-size:17px!important;
    line-height:1.7!important;
    padding-left:8px !important;
    padding-right:8px !important;
}

.markdown{
    font-size:17px!important;
}

.gr-markdown{
    font-size:17px!important;
}

/* Sidebar panel */

#history-panel{
    height:250px !important;
    overflow-y:auto !important;

    padding:18px !important;

    background:#182235 !important;
    font-size:16px !important;

    line-height:1.8 !important;
}

/* remove markdown extra margin */

#history-panel p{
    margin:0 !important;
}

#history-panel h3{
    margin-bottom:18px !important;
}

#history-panel ul{
    padding-left:18px !important;
}

#history-panel li{
    margin-bottom:8px !important;
}

/* Chatbot scrollbar */

.gr-chatbot::-webkit-scrollbar{
    width:10px;
}

.gr-chatbot::-webkit-scrollbar-track{
    background:#111827;
    border-radius:20px;
}

.gr-chatbot::-webkit-scrollbar-thumb{
    background:#475569;
    border-radius:20px;
}

.gr-chatbot::-webkit-scrollbar-thumb:hover{
    background:#64748b;
}

.gr-chatbot > div::-webkit-scrollbar{
    width:10px;
}

.gr-chatbot > div::-webkit-scrollbar-track{
    background:#111827;
}

.gr-chatbot > div::-webkit-scrollbar-thumb{
    background:#475569;
    border-radius:20px;
}

.gr-chatbot *::-webkit-scrollbar{
    width:8px;
}

.gr-chatbot *::-webkit-scrollbar-track{
    background:#111827;
}

.gr-chatbot *::-webkit-scrollbar-thumb{
    background:#475569;
    border-radius:20px;
}

.gr-chatbot *::-webkit-scrollbar-thumb:hover{
    background:#64748b;
}

footer,
.gradio-footer,
.gradio-container footer{
    display:none !important;
}

/* Footer container */
#footer{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

"""


def ask_question(message: str, history: list):

    if history is None:
        history = []

    if not message.strip():
        yield history, "", "_No questions yet._"
        return

    ##################################################################
    # Show user message immediately
    ##################################################################

    history.append(
        {
            "role": "user",
            "content": "🧑‍💻 " + message,
        }
    )

    ##################################################################
    # Temporary assistant message
    ##################################################################

    history.append(
        {
            "role": "assistant",
            "content": "🤖 ⏳ **Thinking...**",
        }
    )
    QUESTION_HISTORY.append(message)

    history_text = ""

    if QUESTION_HISTORY:

        for q in QUESTION_HISTORY:
            history_text += f"💬 {q}\n\n"

    else:

        history_text += "_No questions yet._"

    ############################################################
    # FIRST UPDATE
    ############################################################

    yield history, "", history_text

    ############################################################
    # Run RAG
    ############################################################
    REQUEST_COUNT.inc()
    start = time.perf_counter()

    response = service.chat(message)

    REQUEST_LATENCY.observe(time.perf_counter() - start)

    answer = response.answer

    if response.sources:

        answer += "\n\n---\n### 📚 Sources\n\n"

        for source in response.sources:

            answer += f"- [{source.title}]({source.url})\n"

    ############################################################
    # Replace thinking bubble
    ############################################################

    history[-1] = {
        "role": "assistant",
        "content": answer,
    }

    yield history, "", history_text


with gr.Blocks(
    title="Kuberion AI",
) as demo:

    gr.HTML("""
<div style="padding-bottom:25px">

<h1 style="
font-size:36px;
font-weight:800;
margin:0;
color:white;">
🤖 Kuberion AI
</h1>

<div style="
margin-top:10px;
font-size:18px;
color:#94a3b8;
line-height:1.7;
max-width:900px;">

Production-ready Kubernetes Assistant powered by ⚡

<b>Hybrid Search</b> ⚡
<b>Cross Encoder Reranking</b> ⚡
<b>RAG</b> ⚡
<b>Groq LLM</b>

Ask questions using the official Kubernetes documentation.

</div>

</div>
""")

    with gr.Row():

        ##################################################
        # Sidebar
        ##################################################

        with gr.Column(
            scale=1,
            min_width=250,
            elem_id="sidebar",
        ):

            gr.Markdown("## 💬 Conversation History")

            history_panel = gr.Markdown(
                value="_No questions yet._",
                elem_id="history-panel",
            )

            clear = gr.Button(
                "🗑 Clear Chat",
                variant="primary",
                size="lg",
            )

        ##################################################
        # Chat
        ##################################################

        with gr.Column(scale=5):

            chatbot = gr.Chatbot(
                value=[],
                label=None,
                show_label=False,
                height=350,
                layout="bubble",
                buttons=["copy"],
                placeholder="""
# 👋 Welcome to Kuberion AI

Ask anything about Kubernetes.

Try asking:

• What is a Deployment?

• Explain ConfigMap.

• How do Pods communicate?

• Difference between StatefulSet and Deployment.

• Explain NetworkPolicy.
""",
            )

            with gr.Row():

                question = gr.Textbox(
                    placeholder="Ask anything about Kubernetes...",
                    show_label=False,
                    container=False,
                    autofocus=True,
                    lines=1,
                    max_lines=6,
                    scale=18,
                )

                ask = gr.Button("➤", min_width=52, size="lg", variant="primary")

            gr.Examples(
                examples=[
                    ["How do Pods communicate?"],
                    ["What is a Deployment?"],
                    ["Explain ConfigMap."],
                    ["Difference between StatefulSet and Deployment."],
                    ["Explain NetworkPolicy."],
                ],
                inputs=question,
            )

    ask.click(
        fn=ask_question,
        inputs=[
            question,
            chatbot,
        ],
        outputs=[
            chatbot,
            question,
            history_panel,
        ],
        show_progress="full",
    )

    question.submit(
        fn=ask_question,
        inputs=[
            question,
            chatbot,
        ],
        outputs=[
            chatbot,
            question,
            history_panel,
        ],
        show_progress="full",
    )

    def clear_chat():

        QUESTION_HISTORY.clear()

        return (
            [],
            "",
            "_No questions yet._",
        )

    clear.click(
        fn=clear_chat,
        outputs=[
            chatbot,
            question,
            history_panel,
        ],
    )

    gr.HTML(
        """
    <hr style="
    border:none;
    border-top:1px solid #243244;
    margin:35px 0 20px 0;
    ">
    
    <div style="
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:14px;
    padding:8px 0 18px 0;
    font-size:14px;
    color:#94a3b8;
    ">

    <!-- Row 1 -->

    <div style="
    display:flex;
    align-items:center;
    flex-wrap:wrap;
    justify-content:center;
    gap:8px;
    ">

    <span style="font-weight:600;color:white;">Built with</span>

    <a href="https://www.python.org/" target="_blank">
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
    </a>

    <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white">
    </a>

    <a href="https://www.gradio.app/" target="_blank">
    <img src="https://img.shields.io/badge/Gradio-FF7C00?style=flat-square&logo=gradio&logoColor=white">
    </a>

    <a href="https://kubernetes.io/" target="_blank">
    <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white">
    </a>

    <a href="https://www.sbert.net/" target="_blank">
    <img src="https://img.shields.io/badge/Sentence--Transformers-6B5BCE?style=flat-square">
    </a>

    <a href="https://huggingface.co/" target="_blank">
    <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black">
    </a>

    <a href="https://groq.com/" target="_blank">
    <img src="https://img.shields.io/badge/Groq-000000?style=flat-square">
    </a>

    </div>

    <!-- Row 2 -->

    <div style="text-align:center;">

    Made with ❤️ by

    <a href="https://github.com/harmeetsingh11"
    target="_blank"
    style="color:#60a5fa;font-weight:600;text-decoration:none;">
    Harmeet Singh
    </a>

    &nbsp;•&nbsp;

    <a href="https://github.com/harmeetsingh11/kuberion-ai"
    target="_blank"
    style="color:#60a5fa;text-decoration:none;">
    GitHub
    </a>

    &nbsp;•&nbsp;

    <a href="/gradio_api"
    target="_blank"
    style="color:#60a5fa;text-decoration:none;">
    Use via API
    </a>

    &nbsp;•&nbsp;

    <a href="https://www.gradio.app/"
    target="_blank"
    style="color:#60a5fa;text-decoration:none;">
    Built with Gradio
    </a>

    </div>

    <!-- Row 3 -->

    <div style="
    text-align:center;
    font-size:13px;
    color:#64748b;
    ">

    © 2026 Kuberion AI • Open Source • Built for learning and the Kubernetes community.

    </div>

    </div>
    """,
        elem_id="footer",
    )

demo.queue(
    max_size=20,
)

# Expose Prometheus metrics
start_http_server(8000)

demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    css=CUSTOM_CSS,
    theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate",
    ),
)
