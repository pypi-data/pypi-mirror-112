import aiohttp
headers = {'content-type': 'application/json'} 
class TenorHttp: 
    """ 
    This way of sending request may cause some delay but 
    it was the only fix i could come up with for the unclosed 
    client session warning.
    """
    async def request(self, *, method: str = "GET" , url: str): 
        method = method.lower()
        async with aiohttp.ClientSession(headers=headers) as session:
            if method == "get": 
                return await self.__fetch(session , url)

    async def __fetch(self , client , url): 
        async with client.get(url) as resp: 
            return await resp.json()
