from funcx.sdk.client import FuncXClient
import uuid
fxc = FuncXClient(funcx_service_address='http://localhost:5000/api/v1', asynchronous=True)


def squared(x):
    return x**2


async def task():
    endpoint = 'c6c7888a-1134-40a7-b062-8f3ecfc4b6c2'
    squared_function = fxc.register_function(squared)
    inputs = list(range(10))
    batch = fxc.create_batch(batch_id=str(uuid.uuid4()))
    for x in inputs:
        batch.add(x, endpoint_id=endpoint, function_id=squared_function)
    batch_res = fxc.batch_run(batch)
    print("Got batch_res : ", batch_res)

    for f in batch_res:
        print(await f)

fxc.loop.run_until_complete(task())
