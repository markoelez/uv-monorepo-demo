from .other import func
import pandas as pd
from lib1.models import TestModel


def main():
    print("Hello from project1!")
    t = func()
    print("main.py", t)

    t = pd.DataFrame([1, 2, 3])
    print(t)

    x = TestModel(name="tester")
    print(x)


if __name__ == "__main__":
    main()
