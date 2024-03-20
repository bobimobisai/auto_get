import aiofiles, asyncio, aiohttp, json
from fake_useragent import UserAgent


base_proxy = "for_proxy/proxy.json"
valid_file = "for_proxy/valid_proxy.json"
p_proxy = "new_proxy_2024-03-20.txt"

url = "https://my.saleads.pro/s/dfqJk"


def get_headers():
    ua = UserAgent()
    yield {"User-Agent": ua.random}


async def get_proxies_from_file(file_path):
    proxy_list = []
    async with aiofiles.open(file_path, "r") as file:
        async for line in file:
            proxy_list.append(line.strip())
    return proxy_list


# async def get_proxies_from_file(file_path: str) -> list:
#     try:
#         async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
#             content = await file.read()
#             proxies = json.loads(content)
#             return proxies["proxy"]
#     except FileNotFoundError:
#         print(f"File '{file_path}' not found.")
#     except PermissionError:
#         print(f"Permission denied to open file '{file_path}'.")


async def write_proxies_to_file(file_path: str, proxies):
    data = {"proxy": proxies}
    async with aiofiles.open(file_path, "w") as file:
        await file.write(json.dumps(data, indent=4))


async def check_proxy(proxy, url):
    headers = next(get_headers())
    timeout = aiohttp.ClientTimeout(total=20)
    connector = aiohttp.TCPConnector(keepalive_timeout=20)
    async with aiohttp.ClientSession(
        headers=headers, timeout=timeout, connector=connector
    ) as session:
        try:
            await asyncio.sleep(20)
            async with session.get(url, proxy=f"http://{proxy}") as response:
                if response.status == 200:
                    print(f"Успешно вошли на сайт через прокси {proxy}")
                    return proxy, True
                else:
                    print(
                        f"Не удалось получить доступ к веб-сайту через прокси {proxy}"
                    )
        except aiohttp.ClientError as e:
            print(f"Ошибка прокси {proxy}: {e}")
            return proxy, False


async def check_proxies(proxies, url):
    tasks = [check_proxy(proxy, url) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    valid_proxies = [proxy for proxy, success in results if success]
    await write_proxies_to_file(valid_file, valid_proxies)


async def main():
    proxies = await get_proxies_from_file(file_path=p_proxy)
    await check_proxies(proxies, url)


if __name__ == "__main__":
    asyncio.run(main())
