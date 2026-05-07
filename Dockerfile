FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS builder

ARG QUARTO_VERSION=1.6.42
RUN apt-get update && apt-get install -y wget curl && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb && \
    dpkg -i quarto-${QUARTO_VERSION}-linux-amd64.deb && \
    rm quarto-${QUARTO_VERSION}-linux-amd64.deb

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY . .

RUN uv sync --frozen
RUN uv run quarto render 2>&1 || (echo "=== QUARTO RENDER FAILED ===" && exit 1)
RUN test -f /app/_output/index.html || (echo "ERROR: index.html not found" && exit 1)

FROM nginx:alpine
RUN apk add --no-cache wget
COPY --from=builder /app/_output/. /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
