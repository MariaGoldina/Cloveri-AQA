import functools


def logger_tests(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pass
        # file_content = (f"Request: <{func.__name__}>  <{args}, {kwargs}> \n Response: < {func(*args, **kwargs)} >  \n")
        # with open('D:\Education\PyCharmProjects\Cloveri-AQA\\tests\logs\pytest-logs.txt', 'a', encoding='utf-8') as file:
        #     file.write(file_content)
        return func(*args, **kwargs)
    return wrapper
