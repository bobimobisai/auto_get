import aiohttp, asyncio, aiofiles, json
from datetime import datetime


url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
list_urls = [
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
]

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d")


async def get_proxy_list(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    res = await response.text()
                    file_name = f"new_proxy_{formatted_datetime}.txt"
                    async with aiofiles.open(file_name, "w") as file:
                        await file.write(res)
        except Exception as e:
            print(e)


async def get_proxies_from_file(file_path):
    proxy_list = []
    async with aiofiles.open(file_path, "r") as file:
        async for line in file:
            proxy_list.append(line.strip())
    return proxy_list


async def main():
    # data = await get_proxy_list(url=url)
    proxies = await get_proxies_from_file(file_path="new_proxy_2024-03-20.txt")
    print(proxies)


if __name__ == "__main__":
    asyncio.run(main())
