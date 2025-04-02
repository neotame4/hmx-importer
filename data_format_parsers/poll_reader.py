def read_poll(reader) -> None:
    exit = reader.numstring()
    print("exit", exit)
    enter = reader.numstring()
    print("enter", enter)