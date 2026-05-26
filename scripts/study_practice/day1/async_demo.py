# async_demo.py
import asyncio
import os


async def say_hello():
    print("Hello, World!")
    await asyncio.sleep(1)  # 模拟异步操作
    print("Goodbye, World!")


async def main():
    await say_hello()
    # 环境变量加载代码可在此处添加，如果需要

if __name__ == "__main__":
    asyncio.run(main())
