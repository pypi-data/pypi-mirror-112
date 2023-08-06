# [Tawpy](https://tenor.com/gifapi/documentation)

An `asynchronous` api wrapper writen in python originally made to be used for [discord.py](https://discordpy.readthedocs.io/en/stable/)

## Features 
-   Almost full coverage of the `Tenor` api
-   `Asynchronous` support has been added
-   The ability to request gifs from the `Tenor` website

## Installing Tawpy 
### Requires Python Version 3.7 +
```sh
# Linux/macOS
python3 -m pip install -U tawpy

# Windows
py -3 -m pip install -U tawpy
```
To install the development version and contribute do: 
```sh
$ git clone https://github.com/devKeef/tawpy
$ cd tawpy
```


## Quick Example
```py

import tawpy
from tawpy import Tapi
from tawpy import Enum
import asyncio


client = Tapi("API_KEY")
async def main(): 
    print(await client.tenor_trending_request())

asyncio.get_event_loop().run_until_complete(main())
""" 
OUTPUT 

('https://media.tenor.com/images/0b26816e611b5511ece09f6db6c6f593/tenor.gif', 
'https://media.tenor.com/images/0d194d2aa3bbc0f0c2d0fe42b05ae274/tenor.gif', 
'https://media.tenor.com/images/0997e68794ba980c948561c66cf4c541/tenor.gif', 
'https://media.tenor.com/images/abcc26ae5960d42fc9d3897e2c6ee303/tenor.gif', 'https://media.tenor.com/images/a2c1f41d08dbd2e769ad88de33fe00e2/tenor.gif')
"""
```

## HOW TO GET API KEY 
VISIT https://tenor.com/developer/dashboard, create a new application and grab it's api key
## Documentation 
This section of the markdown file contains the duties of specific functions and their parameters and how they affect the set `tuple` of gifs you reviece from `Tenor`
## Paremters
```
Keep in mind that these are all keyword-arguments 
there are no positional arguments all functions 
are keyword-argument based.


query: str
The tag to be used to find an array or specific gif from 
the tenor website.

limt: int = 5 
The number of gifs that you would like to request from the 
tenor website with each call.

contentfilter: Enum = Enum.ContentFilter.LOW 
The the content safety of gifs requested from
the tenor website with each call.

mediafilter: Enum = Enum.MediaFilter.GIF 
The format in which the gifs are returned in.

pos: int = 5
The position you want to start collection gif's from.

locale: Enum = Enum.LocaleMedida.EN_US 
The default language to interpret search string.
```
## Methods
```
All methods in this section returns a tuple of gif urls 
from tenor. 

async def tenor_search_request(
    self , *,
    query: str ,
    limit: int = 5 , 
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    pos: int = 0 , 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:


This function request gif's from the tenor 
website starting listed most popular gif's to least.

async def tenor_trending_request(
    self , *,
    limit: int = 5 , 
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:

This function request trending gif's 
from the tenor website listed most popular gif's to least.


async def custom_random_request(
    self , *,
    query: str ,
    limit: int = 5 , 
    pos: int = 5 ,
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:

This function request random gif's from the tenor website with each call
When i say random i mean random the listing order is not most popular to least 
it is random completey random. 


async def tenor_random_request(
    self , *,
    query: str ,
    limit: int = 5 , 
    pos: int = 0 ,
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:

This function request random gif's from the tenor website
would use tenor_gif_search if i were you.
```
## Enums 
```
Content Filters

OFF: MAY INCLUDED NSFW GIFS
LOW: A LOWER RISK OF NSFW GIFS 
MEDIUM: AN EVEN LOWER RISK OF NSFW GIFS 
HIGH: THE LOWEST RISK OF NSFW GIFS


Media Filters

Gifs
----
GIF: HIGH QUALITY GIF FORMAT , LARGEST FORMAT OF GIF
MEDIUMGIF: SMALL REDUCTION OF GIF FORMAT
TINYGIF: REDUCED SIZE OF THE GIF FORMAT
NANOGIF: SMALLEST SIZE OF GIF FORMAT

Mp4
---
MP4: HIGH QUALITY MP4 FORMAT , LARGEST FORMAT OF MP4
LOOPEDMP4: SAME AS MP4
TINYMP4: REDUCED SIZE OF THE MP4 FORMAT
NANOMP4: SMALLEST SIZE OF MP4 FORM

WEBM
----
WEBM: LOWER QUALITY VIDEO FORMAT
TINYWEBM: REDUCED SIZE OF WEBM FORMAT 
NANOWEBM: SMALLEST SIZE OF WEBM FORMAT

Language Codes 

ZH_CN: CHINESE
ZH_TW: TAIWAN
EN_US: ENGLISH 
FR_FR: FRENCH
DE_DE: GERMAN
IT_IT: ITALIAN 
JA_JP: JAPANESE
KO_KR: KOREAN
PT_BR: PORTUGUESE
ES_ES: SPANISH
```
## Implementing In Discord Bot Example
### Before we begin If you don't know what `discord.py` is. Visit [discord.py](https://discordpy.readthedocs.io/en/stable/)
In this example which is placed below shows how the api wrapper is to be 
used when making a `discord bot`
```py
import discord 
from discord.ext import commands
from tawpy import Tapi # Import the "Tapi" Class from the "tawpy" module
from tawpy import Enum # Import the Enums Class from the "tawpy" module

token = "YOUR_API_KEY"
tenor_api_key = "YOUR_TENOR_API_KEY"

tenor_client = Tapi(tenor_api_key) # Create a Tapi Object ( Object used to get information from tenor )
discord_client = commands.Bot(command_prefix="!") # Create a Discord Client Object

@discord_client.event
async def on_ready(): 
    return print("running...")

@discord_client.command() 
async def gif(ctx , *,q: str): 
    # Use the tenor_search_request function 
    # To get a tuple of gifs ranging from the 
    # Most popular to the least
    gif_urls = await tenor_client.tenor_search_request(
        query = q , 
        limit = 1 , 
        mediafilter = Enum.MediaFilter.GIF
    )

    await ctx.send(gif_urls[0]) # Since it returns a tuple select index [0] Or any suitable index

    
discord_client.run(token) # Start the discord client
```

## Implementing In Discord Bot Example With Cogs
```py
import discord 
from discord.ext import commands
from tawpy import Tapi # Import the "Tapi" Class from the "tawpy" module
from tawpy import Enum # Import the Enums Class from the "tawpy" module
import os

token = "YOUR_API_KEY"
tenor_api_key = "YOUR_TENOR_API_KEY"

class MyDiscordClient(commands.Bot): 
    def __init__(self , **kwargs): 
        super(**kwargs)
        self.tenor_client = Tapi(tenor_api_key) # Create the tenor client to be used anywhere
        self.tenor_enums = Enum()
    
    async def on_ready(self): 
        return print("running")
    
discord_client = MyDicordClient(command_prefix="!")

for file in os.listdir("./cogs"):
    if file.endswith(".py"): 
        discord_client.load_extension("cogs.%s" % (file[:-3]))

discord_client.run(token)
```

Create a cog folder and a new file called `tenor.py` 
and do as followed , if you're already furmiliar with `discord.py` feel 
free to skip ahead

```py
import discord 
from discord.ext import commands

class GifCommands(commands.Cog): 
    def __init__(self , client): 
        self.client = client 

        @commands.command() 
        async def gif(self , ctx , *, query: str): 
            return await ctx.send("GIF:\n%s" % (await self.tenor_client.tenor_search_request(
                query = query , 
                limit = 1
            )))

def setup(client): 
    client.add_cog(GifCommands(client))
```