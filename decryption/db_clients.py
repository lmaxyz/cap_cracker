from aiosqlite import Connection
from .task import Task, TaskStatus


class SQLiteClient:
    def __init__(self, db_connection: Connection):
        self.__conn = db_connection

    async def get_task(self, task_id: int):
        cursor = await self.__conn.execute(f'SELECT * FROM tasks WHERE id={task_id}')
        row = await cursor.fetchone()

        if not row:
            return None

        return Task(row[0], row[1], TaskStatus(row[2]))

    async def add_task(self, file_path: str):
        cursor = await self.__conn.cursor()
        sql_query = f"INSERT INTO tasks (file_path, status) VALUES ('{file_path}', {TaskStatus.WAITING.value})"
        await cursor.execute(sql_query)
        added_id = cursor.lastrowid
        await self.__conn.commit()
        return added_id

    async def change_task_status(self, task_id: int, task_status: TaskStatus):
        await self.__conn.execute(f"UPDATE tasks SET status={task_status.value} "
                                  f"WHERE id={task_id}")
        await self.__conn.commit()

    async def get_all_tasks(self):
        tasks = []

        async with self.__conn.execute('SELECT * FROM tasks') as cursor:
            async for row in cursor:
                task_id = int(row[0])
                file_path = row[1]
                status = TaskStatus(row[2])
                tasks.append(Task(task_id, file_path, status))

        return tasks

    async def close(self):
        await self.__conn.close()


def get_db_client(db_connection):
    if isinstance(db_connection, Connection):
        return SQLiteClient(db_connection)

    return None
