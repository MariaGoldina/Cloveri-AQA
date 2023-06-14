from datetime import datetime
from selenium import webdriver
import pytest


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    test_time = (end_time - start_time).total_seconds()
    print(f"\nTest time is: {test_time}")
    if test_time <= 1:
        print('Test time less 1 sec')
    else:
        print('Test failed\n')
    # return f"\nTest time is: {test_time}"


# @pytest.fixture(autouse=True)
# def request_fixture(request):
#     print(request.module.__name__)
#     print(request.function.__name__)
    # print(request.param)


@pytest.fixture(scope='function')
def web_browser():
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")

    yield driver
    driver.quit()
