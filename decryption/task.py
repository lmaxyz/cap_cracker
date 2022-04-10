from dataclasses import dataclass
from enum import IntEnum


class TaskStatus(IntEnum):
    WAITING = 0
    PROCESSING = 1
    FINISHED = 2
    FAILED = 3


@dataclass
class Task:
    task_id: int
    path_file: str
    status: TaskStatus

    @property
    def status_str(self):
        return self.status.name
