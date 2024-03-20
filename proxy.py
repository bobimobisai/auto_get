import aiofiles
import asyncio
import aiohttp
from fake_useragent import UserAgent


no_valide = "for_proxy/no_valid.txt"
valid_file = "for_proxy/valid.txt"
base_proxy = "for_proxy/proxy.txt"

ua = UserAgent()
url = "https://my.saleads.pro/s/dfqJk"
headers = {"User-Agent": ua.random}


async def get_proxies_from_file(file_path: str) -> tuple:
    try:
        async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
            proxies = []
            async for line in file:
                proxies.append(str(line.strip()))
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied to open file '{file_path}'.")
    else:
        return tuple(proxies)


async def write_proxies_to_file(file_path: str, proxies: tuple):
    async with aiofiles.open(file_path, "w") as file:
        await file.write(proxies + "\n")


async def check_proxies(proxy, url):
    for prox in proxy:
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(url, proxy=f"http://{prox}") as response:
                    if response.status == 200:
                        print(f"Успешно вошли на сайт через прокси {prox}")
                        await write_proxies_to_file(
                            file_path=valid_file, proxies=str(prox)
                        )
                    else:
                        print(
                            f"Не удалось получить доступ к веб-сайту через прокси {prox}"
                        )
                        await write_proxies_to_file(file_path=no_valide, proxies=prox)
            except aiohttp.ClientError as e:
                await write_proxies_to_file(file_path=no_valide, proxies=prox)
                print(f"{prox}: {e}")


async def main():
    proxies = await get_proxies_from_file(file_path=base_proxy)
    await check_proxies(proxy=proxies, url=url)


if __name__ == "__main__":
    asyncio.run(main())
