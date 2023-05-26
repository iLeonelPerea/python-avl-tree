# Queue Class
class Queue:
    """ 
    Queue Class.

    This class implements a Queue with basic operations like enqueue and dequeue.
    """
    def __init__(self):
        # Initialize queue
        self._data = []

    def enqueue(self, value: object) -> None:
        """
        Add an element to the end of the queue.

        :param value: The value to be added.
        """
        self._data.append(value)  # Add the element to the queue

    def dequeue(self):
        """
        Remove an element from the front of the queue.
        """
        # Pop the first element from the queue
        return self._data.pop(0)

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        :return: True if the queue is empty, False otherwise.
        """
        return len(self._data) == 0  # Check if the queue is empty

    def __str__(self) -> str:
        """
        String representation of the queue.

        :return: A string representation of the queue.
        """
        data_str = [str(item) for item in self._data]  # Convert each item in queue to a string
        return "QUEUE { " + ", ".join(data_str) + " }"  # Join the string items