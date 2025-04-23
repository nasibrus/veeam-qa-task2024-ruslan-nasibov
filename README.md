# Folder Sync Tool

This script synchronizes two folders (source and replica). The replica folder is updated to exactly match the source folder.

## Features

- One-way synchronization from source to replica
- Periodic syncing (based on interval in seconds)
- File creation, update, and deletion are logged
- Logs printed to both console and log file

## Usage

```bash
python3 folder_sync.py source_folder replica_folder 10 sync.log
```

- `source_folder`: path to the source folder
- `replica_folder`: path to the replica folder
- `10`: sync every 10 seconds
- `sync.log`: path to log file

## Example

```bash
python3 folder_sync.py source_folder replica_folder 5 sync.log
```
