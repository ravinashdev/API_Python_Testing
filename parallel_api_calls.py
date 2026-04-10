import asyncio
import httpx

async def fetch_data(client, url, params):
    # 'params' works exactly like the standard requests library
    response = await client.get(url, params=params)
    return response.json()

async def main():
    urls_with_params = [
        ("https://example.com", {"id": 1}),
        ("https://example.com", {"id": 2}),
    ]
    async with httpx.AsyncClient() as client:
        tasks = [fetch_data(client, url, p) for url, p in urls_with_params]
        # Execute all calls concurrently
        results = await asyncio.gather(*tasks)
        return results[0], results[1]

api_call_1_results, api_call_2_results = asyncio.run(main())