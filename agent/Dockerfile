FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    build-essential \
    git \
    curl \
    nano \
    ca-certificates \
    gnupg \
    graphviz \
    libgraphviz-dev \
    pkg-config

RUN mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
    | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" \
    > /etc/apt/sources.list.d/nodesource.list \
 && apt-get update && apt-get install -y nodejs

ARG NPM_VERSION=11.5.2
RUN npm install -g npm@${NPM_VERSION}

RUN python3.10 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install \
    langgraph \
    streamlit \
    python-dotenv \
    langchain-openai \
    langchain_mcp_adapters \
    pydot \
    pygraphviz

WORKDIR /app

EXPOSE 8502

CMD ["streamlit", "run", "main_ui.py", "--server.headless=true", "--server.port=8502", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
