class Switch:
    def __init__(self, value):
        self.__value = value
        self.__stopped = False

    def case(self, case_value, function):
        if not self.__stopped and case_value == self.__value:
            function()
            self.__stopped = True

        return self

    def default(self, function):
        if not self.__stopped:
            function()



for i in range(10):
    print(i)
    Switch(i) \
    .case(0, lambda: (
        print("null"),
        print("done")
    )).case(1, lambda: (
        print("eins"),
        print("done")
    )).case(2, lambda: (
        print("zwei"),
        print("done")
    )).case(3, lambda: (
        print("drei"),
        print("done")
    )).default(lambda:(
        print("default done")
    ))