# Written by: Christopher Gholmieh
# Imports:

# Writer:
from components import (Calculator, Writer, Agent)


# Joint:
class Joint:
    # Initialization:
    def __init__(self) -> None:
        # Calculator:
        self.calculator: Calculator = Calculator()

        # Writer:
        self.writer: Writer = Writer()

        # Agent:
        self.agent: Agent = Agent()

    # Methods:
    def actuate(self) -> None:
        # Initialization:
        self.calculator.actuate()

