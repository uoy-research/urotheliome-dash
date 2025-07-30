# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

WORKDIR /usr/local/app/DashApp

COPY pyproject.toml ../pyproject.toml
COPY uv.lock ../uv.lock
COPY DashApp/ ./

# Install the dependencies
RUN uv sync

# Update PATH to include virtual env binaries
ENV PATH="/usr/local/app/.venv/bin:$PATH"

# Remove default entrypoint from base image
ENTRYPOINT []

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]