from aiosqlite import Connection
from .task import Task, TaskStatus


class SQLiteClient:
    def __init__(self, db_connection):
        self.__conn: Connection = db_connection

    async def add_task(self, file_path):
        cursor = await self.__conn.cursor()
        sql_query = f"INSERT INTO main.tasks (file_path, status) VALUES ('{file_path}', {int(TaskStatus.WAITING)})"
        await cursor.execute(sql_query)
        added_id = cursor.lastrowid
        await self.__conn.commit()
        return added_id

    async def resolve_task(self, task_id):
        pass

    async def change_task_status(self, task_id, task_status):
        pass

    async def get_all_tasks(self):
        tasks = []

        async with self.__conn.execute('SELECT * FROM tasks') as cursor:
            async for row in cursor:
                task_id = int(row[0])
                file_path = row[1]
                status = TaskStatus(int(row[2]))
                tasks.append(Task(task_id, file_path, status))

        return tasks

    async def close(self):
        await self.__conn.close()


def get_db_client(db_connection):
    if isinstance(db_connection, Connection):
        return SQLiteClient(db_connection)

    return None
