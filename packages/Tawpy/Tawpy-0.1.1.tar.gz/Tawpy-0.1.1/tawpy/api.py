"""
MIT License

Copyright (c) 2021 Keef

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import random
from .enums import Enum
from .errors import *
from .http_tenor import TenorHttp
BASE_URL_SEARCH = "https://g.tenor.com/v1/search"
BASE_URL_TRENDING = "https://g.tenor.com/v1/trending"
BASE_URL_RANDOM =  "https://g.tenor.com/v1/random"
BASE_URL_GIF = "https://g.tenor.com/v1/gifs?"

class Tapi:
    """[Tenor api wrapper used to request gif's from the website]
        This was original made to be used with discord.py bot development
        Why? , Cause i felt like it
    """
    def __init__(self , api_key = None):
        assert api_key , "Please provide an API KEY"
        self.api = api_key
        self.__session = TenorHttp() 

    
    def __get_url_from_response(
        self , 
        response: dict , 
        limit: int , 
        mediafilter: str
    ) -> tuple: 
        if response.get("code") == 5: 
            raise DoesNotExist("THE GIF ID OR NAME COULD NOT BE FOUND")
    
        urls = tuple((response['results'][index]['media'][0][mediafilter]['url'] for index in range(limit)))
        return urls

    async def tenor_search_request(
        self , *,
        query: str ,
        limit: int = 5 , 
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        pos: int = 0 , 
        locale: Enum = Enum.LocaleMedia.EN_US
    ) -> tuple:
        """[Request gif's from the tenor website starting from most popular gif's to least]

        Args:
            query (str): [The tag to be used to find the gif]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            pos (int, optional): [The position you want to start collection gif's from]. Defaults to 0.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US.

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = await self.__session.request(
            url = "%s?q=%s&limit=%s&contentfilter=%s&mediafilter=%s&pos=%s&locale=%s&key=%s"
            % 
            (BASE_URL_SEARCH , query , limit , contentfilter , mediafilter , pos , locale , self.api)
        )
        return self.__get_url_from_response(data , limit , mediafilter)

    async def tenor_trending_request(
        self , *,
        limit: int = 5 , 
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        locale: Enum = Enum.LocaleMedia.EN_US
    ) -> tuple:
        """[Request trending gif's from the tenor website]

        Args:
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = await self.__session.request(
            url = "%s?limit=%s&contentfilter=%s&mediafilter=%s&locale=%s&key=%s"
            % 
            (BASE_URL_TRENDING , limit , contentfilter , mediafilter , locale , self.api)
        )

        return self.__get_url_from_response(data , limit , mediafilter)

    async def custom_random_request(
        self , *,
        query: str ,
        limit: int = 5 , 
        pos: int = 5 ,
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        locale: Enum = Enum.LocaleMedia.EN_US
    ) -> tuple:
        """[Request random gif's from the tenor website with each call , When i say random i mean random]

        Args:
            query (str): [The tag to be used to find the gif]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            pos (int, optional): [The position you want to start collection gif's from]. Defaults to 0.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US.

        Returns:
            tuple[str]: [GIF URLS]
        """

        return await self.tenor_random_request(
            query=query,
            limit=limit,
            contentfilter=contentfilter,
            mediafilter=mediafilter,
            pos=random.randint(0 , pos),
            locale=locale,
        )


    async def tenor_random_request(
        self , *,
        query: str ,
        limit: int = 5 , 
        pos: int = 0 ,
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        locale: Enum = Enum.LocaleMedia.EN_US
    ) -> tuple:
        """[Request random gif's from the tenor , Would use tenor_gif_search]

        Args:
            query (str): [The tag to be used to find the gif]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            pos (int, optional): [The position you want to start collection gif's from]. Defaults to 0.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US.

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = await self.__session.request(
            url = "%s?q=%s&limit=%s&contentfilter=%s&mediafilter=%s&pos=%s&locale=%s&key=%s"
            % 
            (BASE_URL_RANDOM , query , limit , contentfilter , mediafilter , pos , locale , self.api)
        )

        return self.__get_url_from_response(data , limit , mediafilter)

    async def tenor_gif_request(
        self , *,
        ids: int ,
        limit: int = 5 , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
    ) -> tuple:
        """[Request a specific gif from the tenor website]

        Args:
            ids (int): [The gif id]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = await self.__session.request(
            url = "%s?ids=%s&limit=%s&mediafilter=%s&key=%s"
            % 
            (BASE_URL_GIF , ids , limit ,  mediafilter , self.api)
        )

        return self.__get_url_from_response(data , limit , mediafilter)