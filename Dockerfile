FROM python:3.10-alpine

# Install dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    libpq

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY app alembic /app
COPY alembic.ini entrypoint.sh pyproject.toml uv.lock /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
RUN chmod +x /app/entrypoint.sh
CMD ["./entrypoint.sh"]
