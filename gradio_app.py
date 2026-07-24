"""
Professional Gradio interface for Kuberion AI.
"""

from __future__ import annotations

import gradio as gr

from app.container import get_service

service = get_service()


def ask_question(
    message: str,
    history: list,
):
    """
    Handle a chat request.
    """

    if not message.strip():
        return history, ""

    response = service.chat(message)

    answer = response.answer

    if response.sources:

        answer += "\n\n---\n### 📚 Sources\n\n"

        for source in response.sources:

            answer += f"- [{source.title}]({source.url})\n"

    history.append(
        {
            "role": "user",
            "content": message,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return history, ""


with gr.Blocks(
    title="Kuberion AI",
) as demo:

    gr.Markdown("""
# 🤖 Kuberion AI

### Kubernetes Retrieval-Augmented Generation (RAG) Assistant

Ask questions about Kubernetes using the official Kubernetes documentation.
""")

    chatbot = gr.Chatbot(
        label="Conversation",
        height=500,
        type="messages",
    )

    with gr.Row():

        question = gr.Textbox(
            placeholder="Ask a Kubernetes question...",
            show_label=False,
            scale=8,
        )

        ask = gr.Button(
            "🚀 Ask",
            variant="primary",
            scale=1,
        )

    gr.Examples(
        examples=[
            ["How do Pods communicate?"],
            ["What is a Deployment?"],
            ["What is a ConfigMap?"],
            ["What is a StatefulSet?"],
            ["Explain NetworkPolicy."],
        ],
        inputs=question,
    )

    clear = gr.ClearButton(
        components=[
            question,
            chatbot,
        ]
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
        ],
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
        ],
    )

demo.queue()

demo.launch(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
    )
)
