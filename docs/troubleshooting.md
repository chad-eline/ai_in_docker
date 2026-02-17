# Troubleshooting

## Container Issues

### Container won't start

Check logs to identify the issue:

```bash
make logs-ollama   # Check Ollama
make logs-webui    # Check Open-webui
make logs-mcp      # Check MCP server
make logs-all      # Check all containers
```

### Ollama shows "unhealthy"

The health check runs `ollama list`. If this fails:

1. Check if Ollama is still downloading models (first run takes time)
2. View logs: `make logs-ollama`
3. Restart: `docker compose restart ollama`

### Models taking too long to load

First startup downloads the model weights:

- Mistral: ~7GB
- Llama 3: ~8GB
- Phi-3 Mini: ~2GB

Subsequent startups are much faster as models are cached in the volume.

## Network Issues

### Proxy causing timeouts

If using `make build-and-run-with-proxy`, ensure required domains are
whitelisted in `tinyproxy-whitelist.txt`.

### MCP server connection failed

If Open-webui can't connect to the MCP server:

1. **Verify MCP server is running:**
   ```bash
   make mcp-test
   ```

2. **Check the URL:** Use `http://localhost:8000` (not `http://mcp-server:8000`)
   because the browser connects directly.

3. **Check CORS:** Visit http://localhost:8000/docs - if Swagger loads, CORS is
   working.

4. **Check logs:**
   ```bash
   make logs-mcp
   ```

## Open-webui Issues

### Tools not appearing in chat

1. Ensure tools are added in **User Settings → Tools** (not Admin Settings)
2. Click the **+** button in the chat input area to enable tools
3. Create a Custom Model with tools pre-enabled (see [MCP Server docs](mcp-server.md))

### First user registration

On first access, you'll be prompted to create admin credentials. The first user
registered becomes the admin.

### Lost admin access

If you lose access to the admin account:

1. Stop containers: `make stop`
2. Restore from backup: `make restore`
3. Restart: `make build-and-run`

Or reset completely (loses all data):

```bash
make clean
make build-and-run
```

## Performance Issues

### Slow responses

- Check available RAM (models need 8-16GB+)
- Check GPU availability: `nvidia-smi`
- Try a smaller model (Phi-3 Mini)

### High memory usage

Models are loaded into memory. To reduce usage:

1. Use smaller models
2. Reduce the number of pre-loaded models in `docker-compose.yml`

## Resetting Everything

To completely reset (removes all data, conversations, settings):

```bash
make clean
make build-and-run
```

**Warning:** This deletes all conversations and settings. Back up first!

```bash
make backup
make clean
make build-and-run
```
