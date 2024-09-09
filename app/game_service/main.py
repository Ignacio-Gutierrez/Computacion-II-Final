import multiprocessing

from async_game_server import run_async_server
from connect_db_server import connect_to_db

if __name__ == '__main__':
    async_server = multiprocessing.Process(target=run_async_server)
    connect_db_server = multiprocessing.Process(target=connect_to_db)

    async_server.start()
    connect_db_server.start()

    async_server.join()
    connect_db_server.join()