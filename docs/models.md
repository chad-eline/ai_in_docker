# Models

The following models are pre-loaded into Open-webui. You can select them in the
dropdown in the top left corner once you're in the webapp.

## [Mistral 7B](https://huggingface.co/mistralai/Mistral-7B-v0.1)

Mistral 7B is a powerful, open-weight large language model designed for
efficiency and strong performance on a wide range of tasks.

- **Developer:** [Mistral AI](https://mistral.ai/)
- **Size:** ~7GB
- **Best for:** General-purpose tasks, coding, reasoning

## [Llama 3](https://huggingface.co/meta-llama/Meta-Llama-3-8B)

Llama 3 is Meta's latest open large language model, offering improved reasoning
and coding abilities.

- **Developer:** [Meta AI](https://ai.meta.com/llama/)
- **Size:** ~8GB
- **Best for:** Conversational AI, coding, analysis

## [Phi-3 Mini](https://huggingface.co/microsoft/phi-3-mini-4k-instruct)

Phi-3 Mini is a compact, instruction-tuned language model optimized for
efficiency and low resource usage.

- **Developer:** [Microsoft Research](https://www.microsoft.com/en-us/research/project/phi/)
- **Size:** ~2GB
- **Best for:** Quick responses, resource-constrained environments

## Adding More Models

You can add additional models by modifying the Ollama entrypoint in
`docker-compose.yml`:

```yaml
entrypoint: >
  sh -c "
    ollama serve &
    OLLAMA_PID=$$!
    sleep 5
    ollama pull mistral
    ollama pull llama3
    ollama pull phi3:mini
    ollama pull codellama  # Add new models here
    wait $$OLLAMA_PID
  "
```

Or pull models manually after the container is running:

```bash
docker exec ollama ollama pull codellama
```

Browse available models at [ollama.com/library](https://ollama.com/library).
