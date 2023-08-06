import argparse
import pytest
from funcx import FuncXClient
from funcx.sdk.executor import FuncXExecutor
import time

endpoint = '340b6b4e-38a9-46de-b4a7-95b2d4c646fa'


def double(x):
    return x * 2


def test_simple_blocking(fx, endpoint_id):
    f = fx.submit(double, 5, endpoint_id=endpoint_id)
    print("Result : ", f.result())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint_id", required=True)
    args = parser.parse_args()

    fxc = FuncXClient(funcx_service_address='http://localhost:5000/api/v1')
    fx = FuncXExecutor(fxc)
    test_simple_blocking(fx, args.endpoint_id)
