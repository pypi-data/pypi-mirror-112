import argparse
import pytest
from funcx import FuncXClient
from funcx.sdk.executor import FuncXExecutor
import funcx
import time
import logging

endpoint = '340b6b4e-38a9-46de-b4a7-95b2d4c646fa'


def double(x):
    return x, x * 2


def test_bag_of_tasks(fx, endpoint_id, count=10):

    futures = []
    for i in range(count):
        f = fx.submit(double, i, endpoint_id=endpoint_id)
        futures.append(f)

    for fu in futures:
        print("Result : ", fu.result())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint_id", required=True)
    parser.add_argument("-c", "--count", default=10)
    args = parser.parse_args()

    # funcx.set_stream_logger()
    """
    #futures_logger = logging.getLogger("concurrent.futures")
    #futures_logger.addHandler(handler)

    logger = logging.getLogger("asyncio")
    handler = logging.FileHandler("ASYNCIO.log")
    handler.setLevel(logging.DEBUG)
    format_string = "%(asctime)s.%(msecs)03d %(name)s:%(lineno)d [%(levelname)s]  %(message)s"
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    """

    # logger = funcx.set_stream_logger(level=logging.WARNING)

    fxc = FuncXClient(funcx_service_address='http://localhost:5000/api/v1')
    fx = FuncXExecutor(fxc)
    test_bag_of_tasks(fx, args.endpoint_id, count=int(args.count))
    test_bag_of_tasks(fx, args.endpoint_id, count=int(args.count))
