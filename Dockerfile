FROM python:3.10-alpine

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY --exclude=.env . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
RUN chmod +x /app/entrypoint.sh
CMD ["./entrypoint.sh"]
