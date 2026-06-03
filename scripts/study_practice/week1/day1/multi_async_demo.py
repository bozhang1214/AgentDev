import asyncio


async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} completed after {delay} seconds")


async def main():
    # 创建多个异步任务
    tasks = [
        task("A", 2),
        task("B", 3),
        task("C", 1)
    ]

    # 并行执行所有任务
    await asyncio.gather(*tasks)

asyncio.run(main())
