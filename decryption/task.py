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

    def is_failed(self):
        return self.status is TaskStatus.FAILED

    def is_finished(self):
        return self.status is TaskStatus.FINISHED

    def is_processed(self):
        return self.status is TaskStatus.PROCESSING
