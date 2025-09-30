from langchain_core.tools import tool
import asyncio

@tool
async def check_weather(location: str) -> str:
    '''Return the weather forecast for the specified location.'''
    return f"It's always sunny in {location}"

def test_check_city():
    async def get_result():
        return await check_weather.ainvoke(input='Rio de Janeiro')
    weather = asyncio.run(get_result())
    assert 'Rio de Janeiro' in weather

def test_check_sunny():
    async def get_result():
        return await check_weather.ainvoke(input='Rio de Janeiro')
    weather = asyncio.run(get_result())
    assert 'always sunny' in weather