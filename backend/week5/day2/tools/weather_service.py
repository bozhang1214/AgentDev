import httpx
from openai import timeout
import time 
from typing import Dict, Tuple

# 天气代码 -> 中文描述映射（可自行扩展）
WEATHER_CODE_MAP = {
    0: "晴朗",
    1: "主要晴朗",
    2: "部分多云",
    3: "多云",
    45: "雾",
    48: "雾",
    51: "毛毛雨",
    53: "毛毛雨",
    55: "毛毛雨",
    61: "雨",
    63: "雨",
    65: "雨",
    80: "阵雨",
    81: "阵雨",
    82: "强阵雨",
    95: "雷雨",
}
DEFAULT_DESC = "未知天气"

async def get_coordinates(city_name: str):
    """
    使用 Open-Meteo Geocoding API 将城市名转换为经纬度。
    返回 (latitude, longitude) 或 (None, None)
    """
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "zh",
        "format": "json"
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(geocode_url, params=params, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results")
            if results and len(results) > 0:
                lat = results[0].get("latitude")
                lon= results[0].get("longitude")
                return lat, lon
        except Exception:
            pass
    return None, None

def get_weather_desciption(weather_code: int) -> str:
    """根据 WMO 天气代码返回中文描述"""
    return WEATHER_CODE_MAP.get(weather_code, DEFAULT_DESC)

_cache: Dict[str, Tuple[float, str]] = {}
CACHE_TTL = 300

async def get_weather(city: str) -> str:
    """
    异步获取指定城市的天气信息（自动将城市名转为经纬度）。
    参数 city: 城市名（如 "北京"、"Shanghai" 等，支持中英文）
    返回: 格式化天气字符串，如 "北京当前天气：晴朗，温度 22°C"
    """

    # check cache first
    if city in _cache:
        timestamp, cached_weather = _cache[city]
        if time.time() - timestamp < CACHE_TTL:
            print(f"[缓存命中] {city}")
            return cached_weather
        else:
            del _cache[city]

    lat, lon = await get_coordinates(city)
    if (lat is None or lon is None):
        return f"未找到城市“{city}”，请检查城市名称是否正确。"
    
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "Asia/Shanghai",
        "temperature_unit": "celsius",
        "windspped_unit": "kmh"
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(weather_url, params=params, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
            current = data.get("current_weather", {})
            temp = current.get("temperature")
            weather_code = current.get("weathercode")
            wind_speed = current.get("windspeed")

            if temp is None or weather_code is None:
                return f"获取{city}天气失败：返回数据格式异常。"

            desc = get_weather_desciption(weather_code)
            weather_str = f"{city}当前天气：{desc}，温度 {temp}°C，风速{wind_speed} 公里/小时"

            # save cache
            _cache[city] = (time.time(), weather_str)
            return weather_str
        except httpx.TimeoutException:
            return f"查询 {city} 天气超时，请稍后再试。"
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return f"未找到城市“{city}”，请检查名称。"
            else:
                return f"天气服务出错：HTTP {e.response.status_code}"
        except Exception as e:
            return f"查询天气失败：{str(e)}"

if __name__ == "__main__":
    import asyncio

    async def test():
        cities = ["北京", "Shanghai", "纽约", "tokyo"]
        for city in cities:
            result = await get_weather(city)
            print(result)
    
    asyncio.run(test())