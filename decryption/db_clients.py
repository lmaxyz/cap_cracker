from aiosqlite import Connection
from .task import DecryptionTask, TaskStatus


class SQLiteClient:
    def __init__(self, db_connection: Connection):
        self.__conn = db_connection

    async def get_task(self, task_id: int):
        cursor = await self.__conn.execute(f'SELECT * FROM tasks WHERE id={task_id}')
        row = await cursor.fetchone()

        if not row:
            return None

        return DecryptionTask(row[0], row[1], TaskStatus(row[2]), row[3])

    async def add_task(self, file_name: str):
        cursor = await self.__conn.cursor()
        sql_query = f"INSERT INTO tasks (file_name, status) VALUES ('{file_name}', {TaskStatus.WAITING.value})"
        await cursor.execute(sql_query)
        added_id = cursor.lastrowid
        await self.__conn.commit()
        return added_id

    async def change_task_status(self, task_id: int, task_status: TaskStatus, status_msg: str = None):
        update_expression = f"status={task_status.value}"
        if status_msg is not None:
            status_msg = status_msg.replace("'", "")
            update_expression += f", result='{status_msg}'"
        
        print(update_expression)
        await self.__conn.execute(f"UPDATE tasks SET {update_expression} "
                                  f"WHERE id={task_id}")
        await self.__conn.commit()

    async def get_all_tasks(self):
        tasks = []

        async with self.__conn.execute('SELECT * FROM tasks') as cursor:
            async for row in cursor:
                task_id = int(row[0])
                file_path = row[1]
                status = TaskStatus(row[2])
                status_msg = row[3]
                tasks.append(DecryptionTask(task_id, file_path, status, status_msg))

        return tasks

    async def close(self):
        await self.__conn.close()


def get_db_client(db_connection):
    if isinstance(db_connection, Connection):
        return SQLiteClient(db_connection)

    return None
