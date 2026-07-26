FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --frozen

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 7860

CMD ["python", "gradio_app.py"]