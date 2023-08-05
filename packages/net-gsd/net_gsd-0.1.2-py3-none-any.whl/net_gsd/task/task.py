import asyncio
from os import access
from typing import Callable, List, Set, Awaitable

from net_gsd.host import Host, FailedHost


class Task:
    task_queue: set = set()
    failed_hosts: list = []
    debug: bool = False
    result: dict = {}
    complete: bool = False

    def __init__(self, task: Callable, name: str, hosts: List[Host]) -> None:
        self.task: Callable = task
        self.name: str = name
        self.hosts: List[Host] = hosts

    async def _get_hosts(self):
        for host in self.hosts:
            yield host

    async def run_task(self, debug: bool) -> list:
        """Starts the task running"""
        self.debug = debug
        for host in self.hosts:
            if self.debug:
                print(f"running task for {host.hostname}")
            task = asyncio.get_event_loop().create_task(self.task(host), name=f"{self.name}:{host.hostname}:{host.ip}")
            self.task_queue.add(task)
            task.add_done_callback(self._handle_task_result)
        await self._monitor_task()

    async def _monitor_task(self):
        """Monitors the task and removes finished tasks from task list"""
        while len(self.task_queue):
            complete, _ = await asyncio.wait(self.task_queue, timeout=0.5)
            self.task_queue.difference_update(complete)
            if self.debug:
                print(len(self.task_queue))
        self.complete = True

    async def monitor(self):
        """calls the monitor task function"""
        await self._monitor_task()

    def _handle_task_result(self, task: asyncio.Task) -> None:
        """handles the asyncio task callback once task has finshed"""
        try:
            result = task.result()
            hostname = task.get_name().split(":")[1]
            if result and isinstance(result, dict):
                self.result.update({hostname: result})
        except asyncio.CancelledError:
            pass
        except Exception as e:
            task_name, device, ip = task.get_name().split(":")
            self.failed_hosts.append(FailedHost(device, ip, task_name, getattr(e, "message", str(e))))

    def get_failed_hosts(self):
        return self.failed_hosts
