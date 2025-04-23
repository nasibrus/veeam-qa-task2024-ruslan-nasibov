import os
import shutil
import time
import argparse
import logging

def setup_logger(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

def sync_folders(source, replica):
    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, rel_path)
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)
            logging.info(f"Created directory: {replica_root}")
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)
            if not os.path.exists(replica_file) or not filecmp(source_file, replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied/Updated file: {replica_file}")

    for root, dirs, files in os.walk(replica, topdown=False):
        rel_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, rel_path)
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_root, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"Deleted file: {replica_file}")
        for d in dirs:
            replica_dir = os.path.join(root, d)
            source_dir = os.path.join(source_root, d)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                logging.info(f"Deleted directory: {replica_dir}")

def filecmp(file1, file2):
    return os.path.getmtime(file1) == os.path.getmtime(file2)

def main():
    parser = argparse.ArgumentParser(description="Folder Synchronizer")
    parser.add_argument("source", help="Path to source folder")
    parser.add_argument("replica", help="Path to replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to log file")
    args = parser.parse_args()

    setup_logger(args.log_file)

    while True:
        logging.info("Starting synchronization...")
        sync_folders(args.source, args.replica)
        logging.info("Synchronization completed.")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
