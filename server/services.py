import os
import time

from .settings import CAP_FILES_STORAGE


def remove_file(queue):
    print("sleep")
    time.sleep(10)
    print("deleting")
    file_name = queue.get()
    if file_name:
        os.remove(CAP_FILES_STORAGE/file_name)
        print(f"{file_name} deleted")


async def save_file(file, file_name):
    with open(CAP_FILES_STORAGE / file_name, "wb") as f:
        f.write(file.read())


async def add_file_to_decryption_queue(file, file_name):
    await save_file(file, file_name)
    file_path = CAP_FILES_STORAGE/file_name
    print("process was started")
