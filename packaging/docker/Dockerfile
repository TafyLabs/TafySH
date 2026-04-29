# TafySH Docker Image
#
# Build:
#   docker build -t tafysh .
#
# Run:
#   docker run -it --rm -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY tafysh
#
# With volume for persistence:
#   docker run -it --rm \
#     -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
#     -v ~/.config/tafysh:/root/.config/tafysh \
#     tafysh

FROM python:3.11-slim-bookworm

LABEL org.opencontainers.image.title="TafySH"
LABEL org.opencontainers.image.description="AI-enhanced terminal shell"
LABEL org.opencontainers.image.url="https://github.com/tafysh/tafysh"
LABEL org.opencontainers.image.source="https://github.com/tafysh/tafysh"
LABEL org.opencontainers.image.licenses="MIT"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    less \
    vim \
    nano \
    jq \
    tree \
    ncurses-term \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Set locale
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV TERM=xterm-256color

# Create non-root user
RUN useradd -m -s /bin/bash tafysh

# Install TafySH
RUN pip install --no-cache-dir tafysh

# Install optional providers
RUN pip install --no-cache-dir anthropic openai || true

# Add to /etc/shells
RUN echo "/usr/local/bin/tafysh" >> /etc/shells

# Set working directory
WORKDIR /home/tafysh

# Switch to non-root user
USER tafysh

# Create config directory
RUN mkdir -p /home/tafysh/.config/tafysh

# Set shell
ENV SHELL=/usr/local/bin/tafysh

# Default command
ENTRYPOINT ["/usr/local/bin/tafysh"]
