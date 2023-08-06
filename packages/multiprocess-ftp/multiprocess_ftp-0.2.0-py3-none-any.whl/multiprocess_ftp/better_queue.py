"""In memory objects that can be shared by multiple process workers."""
import multiprocessing
from multiprocessing.queues import JoinableQueue


class BetterQueue(JoinableQueue):
    """A better implementation of Queue.

    - Adds a reliable qsize() method
    - Incorporates a more reliable item counter

    """

    def __init__(self):
        """Initialize the queue."""
        super().__init__(ctx=multiprocessing.get_context())
        self.size = SharedCounter(0)

    def __getstate__(self):
        """Help to make MyQueue instance serializable."""
        return {
            "parent_state": super().__getstate__(),
            "size": self.size,
        }

    def __setstate__(self, state):
        """Set the initial queue state."""
        super().__setstate__(state["parent_state"])
        self.size = state.get("size", SharedCounter(0))

    def put(self, *args, **kwargs):
        """Put object into the queue."""
        super().put(*args, **kwargs)
        self.size.increment()

    def get(self, *args, **kwargs):
        """Get object from the queue."""
        item = super().get(*args, **kwargs)
        self.size.increment(-1)
        return item

    def qsize(self):
        """Reliable implementation of multiprocessing.Queue.qsize()"""
        return self.size.value

    def all_tasks_done(self):
        """Decide if the queue has been exhausted."""
        return not self.qsize()


class SharedCounter(object):
    """A synchronized shared counter."""

    def __init__(self, n=0):
        """Initialize the counter."""
        self.count = multiprocessing.Value("i", n)

    def increment(self, n=1):
        """Increment the counter by n (default = 1)"""
        with self.count.get_lock():
            self.count.value += n

    @property
    def value(self):
        """Return the value of the counter"""
        return self.count.value
