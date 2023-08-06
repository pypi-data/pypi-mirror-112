import asyncio
import shutil
import os


class Utils:
    @staticmethod
    def create_folder(folder: str):
        if os.path.exists(folder) is False:
            os.makedirs(folder)

    @staticmethod
    def delete_folder(folder: str):
        if os.path.exists(folder):
            shutil.rmtree(folder)

    @staticmethod
    def progress_bar(
            iteration: int,
            total: int,
            prefix: str
    ):
        f = int(100 * iteration // total)

        print(f"{prefix} [{'█' * f + ' ' * (100 - f)}] {100 * (iteration / float(total)):.2f}%", end='\r')

        if iteration == total:
            print()

    @staticmethod
    def clear_line():
        print('\033[F\033[K', end='')

    @staticmethod
    async def limit_task(number: int, *tasks):
        semaphore = asyncio.Semaphore(number)

        async def sem_task(task):
            async with semaphore:
                return await task

        return await asyncio.gather(*(sem_task(task) for task in tasks))

    def send_except(self, error: str):
        print()
        self.clear_line()
        print(error)
