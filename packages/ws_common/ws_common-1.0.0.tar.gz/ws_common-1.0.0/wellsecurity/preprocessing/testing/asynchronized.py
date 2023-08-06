import asyncio
import time

# 一个真实的耗时操作，可以比如去爬取网页
def mysleep(x, task_name):
    time.sleep(x)
    return task_name + "____" + str(time.time())

async def mytask(task_name):
    print(task_name, 'start')
    # r = asyncio.sleep(1) # 好多教程的做法
    r = await asyncio.get_event_loop().run_in_executor(None, mysleep, 3, task_name)
    print(r)
    print(task_name, 'end')

# for x in range(0, 100):
#     loop = asyncio.get_event_loop()
#     tasks = [mytask('task1'), mytask('task2')]
#     loop.run_until_complete(asyncio.wait(tasks))
#     loop.close()
loop = asyncio.get_event_loop()
t1 = time.time()
tasks = [mytask('task1'), mytask('task2'), mytask('task3'), mytask('task4'), mytask('task5'), mytask('task6'), mytask('task7'), mytask('task8'), mytask('task9'), mytask('task10')]
loop.run_until_complete(asyncio.wait(tasks))
print(time.time()-t1)
loop.close()
