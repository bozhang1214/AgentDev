import httpx
import asyncio

async def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
    
async def main():
    data = await get_weather("Zhengzhou")
    current_temp = data['current_condition'][0]['temp_C']
    print(f"郑州当前温度: {current_temp}℃")

if __name__ == "__main__":
    asyncio.run(main())