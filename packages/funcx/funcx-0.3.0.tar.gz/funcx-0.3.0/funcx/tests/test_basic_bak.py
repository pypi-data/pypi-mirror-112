import argparse
from funcx.sdk.client import FuncXClient
import pytest
import time


def hello_world() -> str:
    return 'Hello World'


def wait_for_task(fxc, task_id, walltime: int = 2):
    import time
    start = time.time()
    while True:
        if time.time() > start + walltime:
            raise Exception("Timeout")
        try:
            r = fxc.get_result(task_id)
        except Exception:
            print("Not available yet")
            time.sleep(1)
        else:
            return r


def test_blocking(fxc, endpoint):
    fn_uuid = fxc.register_function(hello_world, endpoint, description='Hello')
    task_id = fxc.run(endpoint_id=endpoint,
                      function_id=fn_uuid)

    print("Task_id: ", task_id)
    time.sleep(2)
    r = fxc.get_result(task_id)
    print("Task_result : ", r)


def test_non_blocking(fxc, endpoint):
    fn_uuid = fxc.register_function(hello_world, endpoint, description='Hello')
    task_id = fxc.run(endpoint_id=endpoint,
                      function_id=fn_uuid)

    for i in range(5):
        try:
            result = fxc.get_task_status(task_id)
        except Exception as e:
            print(f"Got exception : {e}")
            time.sleep(1)
        else:
            print(f"Result: {result}")
            assert result == hello_world(), "Result from remote function not correct"
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint_id", required=True)
    args = parser.parse_args()

    fxc = FuncXClient()
    test_blocking(fxc, args.endpoint_id)
