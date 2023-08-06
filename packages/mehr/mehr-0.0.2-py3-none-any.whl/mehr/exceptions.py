class CaseAfterDefaultException(Exception):
    def __init__(self):
        super().__init__("Used a 'case' clause after the 'default' clause of the switch statement.")

class SameCaseException(Exception):
    def __init__(self, value):
        super().__init__(f"Used two or more 'case' clause that match {value}.")

class DoubleDefaultException(Exception):
    def __init__(self):
        super().__init__("Used more than one 'default' clause in a switch statement.")

class NoDefaultException(Exception):
    def __init__(self):
        super().__init__("This switch statement has no 'default' clause.")

class BreakNotification(Exception):
    pass