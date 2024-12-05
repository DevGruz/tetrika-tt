def strict(func):
    def wrap(*args, **kwargs):
        annotations = func.__annotations__

        for arg, expected_type in zip(args, annotations.values()):
            if arg == "return":
                continue
            if not isinstance(arg, expected_type):
                raise TypeError()

        for key, value in kwargs.items():
            if key in annotations:
                if not isinstance(value, annotations[key]):
                    raise TypeError()

        result = func(*args, **kwargs)

        if "return" in annotations:
            if not isinstance(result, annotations["return"]):
                raise TypeError()

        return result

    return wrap


@strict
def sum_two_int(a: int, b: int) -> int:
    return a + b


@strict
def sum_two_float(a: float, b: float) -> float:
    return a + b


@strict
def concat_strings(a: str, b: str) -> str:
    return a + b


tests = [
    {
        "func": sum_two_int,
        "args": (2, 3),
        "kwargs": {},
        "expected": 5,
        "description": "Сложение двух целых чисел",
    },
    {
        "func": sum_two_int,
        "args": ("2", 3),
        "kwargs": {},
        "expected_exception": TypeError,
        "description": "Неверный тип первого аргумента",
    },
    {
        "func": sum_two_int,
        "args": (2, "3"),
        "kwargs": {},
        "expected_exception": TypeError,
        "description": "Неверный тип второго аргумента",
    },
    {
        "func": sum_two_float,
        "args": (2.4, 3.7),
        "kwargs": {},
        "expected": 6.1,
        "description": "Сложение двух целых чисел",
    },
    {
        "func": sum_two_float,
        "args": ("2.6", 3.1),
        "kwargs": {},
        "expected_exception": TypeError,
        "description": "Неверный тип первого аргумента",
    },
    {
        "func": sum_two_float,
        "args": (2.7, "3.2"),
        "kwargs": {},
        "expected_exception": TypeError,
        "description": "Неверный тип второго аргумента",
    },
    {
        "func": concat_strings,
        "args": ("Hello, ", "world!"),
        "kwargs": {},
        "expected": "Hello, world!",
        "description": "Конкатенация двух строк",
    },
    {
        "func": concat_strings,
        "args": (42, "world!"),
        "kwargs": {},
        "expected_exception": TypeError,
        "description": "Неверный тип первого аргумента для строки",
    },
    {
        "func": concat_strings,
        "args": ("Hello, ", 42),
        "kwargs": {},
        "expected_exception": TypeError,
        "description": "Неверный тип второго аргумента для строки",
    },
    {
        "func": sum_two_int,
        "args": (2,),
        "kwargs": {"b": 3},
        "expected": 5,
        "description": "Передача одного аргумента через позицию, другого через имя",
    },
]

if __name__ == "__main__":
    for i, test in enumerate(tests):
        func = test["func"]
        args = test.get("args", ())
        kwargs = test.get("kwargs", {})
        expected = test.get("expected")
        expected_exception = test.get("expected_exception")

        try:
            result = func(*args, **kwargs)
            if expected_exception:
                print(
                    f"Test {i} FAILED: {test['description']} - Expected exception {expected_exception}, but no exception was raised"
                )
            elif result != expected:
                print(
                    f"Test {i} FAILED: {test['description']} - Got {result}, expected {expected}"
                )
        except Exception as e:
            if not expected_exception or not isinstance(e, expected_exception):
                print(
                    f"Test {i} FAILED: {test['description']} - Unexpected exception {type(e).__name__}: {e}"
                )
