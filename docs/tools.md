# Tools and Technologies

This project uses the following tools:

## [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

Windows Subsystem for Linux - enables running Linux environments on Windows.

## [Docker Desktop](https://docs.docker.com/desktop/)

Desktop GUI for the popular container platform. Required for running the
containerized services.

## [Ollama](https://ollama.com/)

Ollama is a model runtime environment for managing models. It is akin to Docker
but for AI models - making it easy to pull, run, and manage LLMs locally.

## [Open-webui](https://openwebui.com/)

Open-webui is an open-source web UI providing a ChatGPT-style interface. It is
designed to run and operate totally offline, connecting to local Ollama models.

## [TinyProxy](https://tinyproxy.github.io/)

TinyProxy is a lightweight HTTP/HTTPS proxy server. In this setup, it is used to
control and restrict outbound internet access from the AI containers.

### Whitelist Configuration

- Whitelisted destinations are defined in `tinyproxy-whitelist.txt`
- Default whitelisted destinations: DNS resolvers, HuggingFace, PyPI, and key
  model hosting sites
- Add additional domains to `tinyproxy-whitelist.txt` as needed

### Testing Offline Capability

To test if models are truly running locally with network restrictions:

```bash
docker compose --profile with-proxy up -d --build
```

Then interact with the models and watch the logs. If they respond without
timeout, they're truly offline. Otherwise, requests will be blocked by the
proxy.

To disable the proxy (default mode):

```bash
docker compose up -d --build
```
