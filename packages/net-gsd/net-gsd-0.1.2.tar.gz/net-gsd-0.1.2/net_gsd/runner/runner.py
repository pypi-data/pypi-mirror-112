from typing import *
from time import perf_counter

from net_gsd.runner import Credentials
from net_gsd.host import Host
from net_gsd.task import Task
from net_gsd.runner.errors import NoHostsPresent, InvalidHostKeys, InvalidTask


class Runner:
    """Task runner"""

    tasks: Set[Task] = set()
    failed_hosts: dict = {}

    def __init__(
        self, username: str, password: str, enable: Optional[str] = None, hosts: List[Dict] = None, debug: bool = False
    ) -> None:
        """Initialise task runner. Requires username and password"""
        self.credentials: Credentials = Credentials(username=username, password=password, enable=enable)
        self.hosts: list[Host] = self.get_hosts(hosts) if hosts else []
        self.debug: bool = debug

    def get_hosts(self, hosts: List[Dict]) -> None:
        """Add hosts to host list"""
        try:
            hosts = [
                Host(hostname=host["hostname"], ip=host["ip"], platform=host["platform"], credentials=self.credentials)
                for host in hosts
            ]
        except KeyError:
            raise InvalidHostKeys("Invalid or missing keys in host list")
        return hosts

    def _validate_task(self, name: str, task: Callable, hosts: List[Dict]) -> bool:
        if not isinstance(task, Callable):
            raise InvalidTask(f"{name}: Task must be a function")
        if len(self.hosts) == 0 and not hosts:
            raise NoHostsPresent("No hosts have been passed to the runner.")
        return True

    def queue_task(self, name: str, task: Callable, hosts: List[Dict] = None) -> None:
        """Add task to pending task list, if no hosts are passed into the function,
        the class hosts will be used"""
        if self._validate_task(name, task, hosts):
            task_hosts = self.get_hosts(hosts) if hosts else self.hosts
            self.tasks.add(Task(name=name, task=task, hosts=task_hosts))

    async def run_task(self, name: str, task: Callable, hosts: List[Dict] = None) -> Tuple[dict, list]:
        """Runs task straight away, if no hosts are passed into the function,
        the class hosts will be used"""
        if self._validate_task(name, task, hosts):
            task_hosts = self.get_hosts(hosts) if hosts else self.hosts
            task: Task = Task(name=name, task=task, hosts=task_hosts)
            await task.run_task(self.debug)
        return task.result, task.failed_hosts

    async def _get_tasks(self):
        """Get tasks generator"""
        for task in self.tasks:
            yield task

    async def run(self) -> None:
        """run tasks in the pending tasks queue"""
        start = perf_counter()
        async for task in self._get_tasks():
            print(f"Starting task {task.name}")
            await task.run_task(self.debug)
        end = perf_counter()
        print(f"Tasks ran in {end - start:0.4f} seconds")

    def get_failed_hosts(self) -> List[set]:
        """Return a list if failed hosts from all tasks"""
        return [task.failed_hosts[0] for task in self.tasks if task.failed_hosts]

    def tasks_complete(self) -> bool:
        """Return a bool statiung whether the task have completed"""
        return sum(len(task.task_queue) for task in self.tasks) == 0

    def failed_hosts(self) -> bool:
        """Returns a bool indicating whether there were any failed hosts"""
        return len([task.failed_hosts for task in self.tasks]) > 0

    def get_results(self) -> dict:
        """get results for all tasks"""
        results = {}
        for task in self.tasks:
            results.update(task.result)
        return results
