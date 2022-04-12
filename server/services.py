import os
import time
import aiofiles

from .settings import CAP_FILES_STORAGE
from decryption import DecryptionTaskManager


def remove_file(queue):
    print("sleep")
    time.sleep(10)
    print("deleting")
    file_name = queue.get()
    if file_name:
        os.remove(CAP_FILES_STORAGE/file_name)
        print(f"{file_name} deleted")


async def save_file(file, file_name) -> str:
    dest_path = CAP_FILES_STORAGE / file_name

    async with aiofiles.open(dest_path, "wb") as f:
        await f.write(file.read())

    return dest_path


async def add_file_to_decryption_queue(file, task_manager: DecryptionTaskManager):
    saved_file_path = await save_file(file.file, file.filename)
    await task_manager.push_new_task(saved_file_path)
