import multiprocessing

from async_game_server import run_async_server
from connect_db_server import connect_to_db

if __name__ == '__main__':
    async_to_db_conn1, async_to_db_conn2 = multiprocessing.Pipe()
    db_to_async_conn1, db_to_async_conn2 = multiprocessing.Pipe()

    async_server = multiprocessing.Process(target=run_async_server, args=(async_to_db_conn1, db_to_async_conn2))
    connect_db_server = multiprocessing.Process(target=connect_to_db, args=(db_to_async_conn1, async_to_db_conn2))

    async_server.start()
    connect_db_server.start()

    async_server.join()
    connect_db_server.join()