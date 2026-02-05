# Backup and Restore

Your conversations, notes, and settings are stored in Docker volumes and persist
across container restarts. However, running `make clean` will delete them.

## Backup Your Data

```bash
make backup
```

This creates a timestamped backup file in the `backups/` directory:

```
backups/openwebui-backup-20260205-125000.tar
```

## Restore from Backup

### Restore most recent backup

```bash
make restore
```

### Restore specific backup

```bash
make restore BACKUP=openwebui-backup-20260205-125000.tar
```

After restoring, restart the containers:

```bash
make build-and-run
```

## What's Backed Up

| Data             | Location              | Included |
| ---------------- | --------------------- | -------- |
| Conversations    | `openwebui_data`      | Yes      |
| User settings    | `openwebui_data`      | Yes      |
| Notes            | `openwebui_data`      | Yes      |
| Knowledge bases  | `openwebui_data`      | Yes      |
| Model weights    | `ollama_data`         | No (re-downloaded) |
| MCP data files   | `mcp_data`            | No (separate backup if needed) |

## When to Backup

- Before running `make clean`
- Before major upgrades
- Periodically (consider a cron job)

## Automated Backups

To set up automated daily backups, add a cron job:

```bash
crontab -e
```

Add this line (backs up daily at 2 AM):

```
0 2 * * * cd /path/to/ai_in_docker && make backup
```

## Backup MCP Data Separately

If you have important files in the MCP data volume:

```bash
docker run --rm -v ai_in_docker_mcp_data:/data -v $(pwd)/backups:/backup \
  alpine tar cvf /backup/mcp-data-$(date +%Y%m%d).tar /data
```
