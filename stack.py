# Stack Class
class Stack:
    """
    Stack Class.

    This class implements a Stack with basic operations like push and pop.
    """
    def __init__(self):
        # Initialize stack
        self._data = []

    def push(self, value: object) -> None:
        """
        Push an element to the top of the stack.

        :param value: The value to be added.
        """
        self._data.append(value)  # Push the value onto the stack

    def pop(self):
        """
        Pop an element from the top of the stack.
        """
        # Pop the top element from the stack
        return self._data.pop()

    def top(self):
        """
        Get the top element of the stack.

        :return: The top element of the stack.
        """
        # Return the top element of the stack
        return self._data[-1]

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        :return: True if the stack is empty, False otherwise.
        """
        return len(self._data) == 0  # Check if the stack is empty

    def __str__(self) -> str:
        """
        String representation of the stack.

        :return: A string representation of the stack.
        """
        data_str = [str(item) for item in self._data]  # Convert each item in stack to a string
        return "STACK: { " + ", ".join(data_str) + " }"  # Join the string items