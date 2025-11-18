# AI Docker Examples

## Overview

This is a simple example of how to build and run AI models with a chat-gpt style
web interface. The objective is to create a simple environment to experiment and
evaluate different AI models locally.

## Tools

This project uses the following tools:

### [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

-Windows Subsystem for Linux

### [Docker Desktop](https://docs.docker.com/desktop/)

- Desktop GUI for the popular container platform.

### [Ollama](https://ollama.com/)

- Ollama is a model runtime environment.for managing models.
- It is akin to docker but for AI models.

### [Open-webui](https://openwebui.com/)

- Open-webui is an open-source web ui, providing a chat-gpt style interface.
- It is designed to run and operate totally offline.

### TinyProxy

TinyProxy is a lightweight HTTP/HTTPS proxy server. In this setup, it is used to control and restrict outbound internet access from the AI containers. Only whitelisted IP addresses (such as 4.2.2.2 and 8.2.2.2) are allowed for outbound connections, ensuring that no unintended data leaves the local environment. The proxy is configured via a custom `tinyproxy.conf` file, which is mounted into the proxy container.

## Models

The following models are pre-loaded into Open-webUI. You can select them in the drop
down in the top left corner once you're in the webapp.

### [Mistral 7B](https://huggingface.co/mistralai/Mistral-7B-v0.1)

Mistral 7B is a powerful, open-weight large language model designed for efficiency and strong performance on a wide range of tasks. Developed by [Mistral AI](https://mistral.ai/).

### [Llama 3](https://huggingface.co/meta-llama/Meta-Llama-3-8B)

Llama 3 is Meta's latest open large language model, offering improved reasoning and coding abilities. Developed by [Meta AI](https://ai.meta.com/llama/).

### [Phi-3 Mini](https://huggingface.co/microsoft/phi-3-mini-4k-instruct)

Phi-3 Mini is a compact, instruction-tuned language model optimized for efficiency and low resource usage. Developed by [Microsoft Research](https://www.microsoft.com/en-us/research/project/phi/).

## Build and Run

- Make sure docker-desktop is up and running.
- Then run the following make cmd on the cli. This will build and start the containers.

```bash
make build-and-run
```

- Then open the following [this url to the UI.](http://localhost:3000/auth?redirect=%2F)

- You can check the status of Ollama [at this URL.](http://localhost:11434/)
