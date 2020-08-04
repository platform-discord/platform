from datetime import datetime
from random import choice, randint

import pytz
import requests
from aiohttp import request

from decouple import config

from discord import Member, Forbidden
from discord.ext.commands import Cog, cooldown, BucketType
from discord.ext.commands import command

from utils import basic_utilties as utils

standard_cooldown = 3.0

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""
        self._8ballResponse = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely',
                              'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good',
                              'Signs point to yes', 'Yes', 'Reply hazy, try again', 'Ask again later',
                              'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                              "Don't bet on it", 'My reply is no', 'My sources say no', 'Outlook not so good',
                              'Very doubtful']
        self.pp_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        100]
        self.weather_api_key = config("WEATHER_API_KEY")

    @command(name="weather")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_weather(self, ctx, *, city: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        api_url = "http://api.openweathermap.org/data/2.5/weather?"
        # Complete the api_url with the API token.
        complete_url = api_url + "appid=" + self.weather_api_key + "&q=" + city
        # Get the response from the url
        response = requests.get(complete_url)
        # Get the JSON
        x = response.json()
        if x["cod"] != "404": # Make sure the page isn't 404'd :thonk:
            y = x["main"] # Main section
            current_temp = round(int(y["temp"]) - 273.15) # Get the temperature (Kelvin -> Celsius)
            current_temp_f = (current_temp * 9/5) + 32 # Get the temperature (Celsius -> Fahrenheit)
            current_pressure = y["pressure"] # Get the atmospheric pressure (hPa)
            current_humidity = y["humidity"] # Humidity (%)
            z = x["weather"] # Weather Info
            weather_description = z[0]["description"] # Weather Description
            icon = z[0]["icon"] # The Weather Icon

            # Put it all into a useful little embed
            embed = utils.embed_message(title=f"Weather in: {x['name']}",
                                        message="**Temperature: (C/F)**\n" +
                                        f"{current_temp} / {current_temp_f}\n" +
                                        "**Atmospheric Pressure: (hPa)**\n" +
                                        f"{current_pressure}\n" +
                                        "**Humidity: (%)**\n" +
                                        f"{current_humidity}\n" +
                                        "**Weather Description:**\n" +
                                        f"{weather_description}",
                                        thumbnail=f"https://openweathermap.org/img/wn/{icon}@4x.png",
                                        footer_icon=self.bot.user.avatar_url,
                                        footer_text=utils.random_message())
            await ctx.send(embed=embed)
        else: # If it 404'd or otherwise, we just assume that it wasn't found.
            return await ctx.send("That was not found... Try another City or Country!")


    @command(name="floof")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_cat_dog_image(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        api_url = choice(["https://some-random-api.ml/img/dog", "https://some-random-api.ml/img/cat"])
        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image = data["link"]

                if api_url == "https://some-random-api.ml/img/dog":
                    dog_or_cat = "Dog"
                else:
                    dog_or_cat = "Cat"

                message = utils.embed_message(title=f"Here's a random image of a {dog_or_cat}",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())
                message.set_image(url=image)

                return await ctx.send(embed=message)
            else:
                return await ctx.send(f"API returned a {response.status} status.")

    @command(name="kanye", aliases=["ye"])
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_kanye_quotes(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        api_url = "https://api.kanye.rest/"
        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                quote = data["quote"]

                message = utils.embed_message(title=f"\"{quote}\" - Kanye West",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())

                return await ctx.send(embed=message)
            else:
                return await ctx.send(f"API returned a {response.status} status.")

    @command(name="hug")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_hug(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            member = ctx.author
        api_url = "https://some-random-api.ml/animu/hug"

        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]

                message = utils.embed_message(message=f"{ctx.author.mention} has hugged {member.mention}",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())
                message.set_image(url=image_link)

                return await ctx.send(embed=message)
            else:
                return await ctx.send(f"API returned a {response.status} status.")

    @command(name="pat")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_pat(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            member = ctx.author
        api_url = "https://some-random-api.ml/animu/pat"

        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]

                message = utils.embed_message(message=f"{ctx.author.mention} has patted {member.mention}",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())
                message.set_image(url=image_link)

                return await ctx.send(embed=message)
            else:
                return await ctx.send(f"API returned a {response.status} status.")

    @command(name="wasted")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_wasted(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            member = ctx.author
        api_url = f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format='png')}"

        message = utils.embed_message(message=f"**WASTED** {member.mention}",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        message.set_image(url=api_url)

        await ctx.send(embed=message)

    @command(name="meme")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_meme(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        api_url = "https://some-random-api.ml/meme"

        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["image"]
                caption = data["caption"]
                category = data["category"]

                message = utils.embed_message(title=f"Category: {category}",
                                              message=caption,
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())
                message.set_image(url=image_link)

                return await ctx.send(embed=message)
            else:
                return await ctx.send(f"API returned a {response.status} status.")

    @command(name="babyname", aliases=["nickme"])
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_babyname(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        api_url = "https://randomuser.me/api/"

        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                name = data["results"][0]["name"]["first"]

                try:
                    await ctx.author.edit(nick=name)
                    await ctx.send(f"I chose {name} for you, what a beautiful name, king or queen 😍")
                except Forbidden:
                    await ctx.send(f"I was unable to change your name, but I chose {name} for you anyways 💅")

    @command(name="timezone", aliases=["tz"])
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_timezone(self, ctx, timezone: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if timezone is None:
            await ctx.send("You can get a list of all the timezones at -> https://kal-byte.co.uk/timezones.txt")
        tz_ = pytz.timezone(timezone)
        datetime_tz = datetime.now(tz_)
        datetime_tz_readable = datetime_tz.strftime("%A / %d %B %Y / %H:%M:%S")
        timezone_message = utils.embed_message(title=f"Time in {timezone}",
                                               message=f"It's currently **{datetime_tz_readable}** in **{timezone}**",
                                               footer_icon=self.bot.user.avatar_url,
                                               footer_text=utils.random_message())
        await ctx.send(embed=timezone_message)

    @command(name="urbandictionary", aliases=["ud", "urban"])
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_urbandictionary(self, ctx, *, definition):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        get_definition = await utils.urban_def(definition)
        get_example = await utils.urban_xmp(definition)

        if len(get_definition) + len(get_example) > 2048:
            return await ctx.send(f"The urban lookup for this word is too large! (Above 2048 Characters)")

        message = utils.embed_message(title=f"Urban Dictionary Definition of -> {definition}",
                                      message=f"**Definition ->**\n" +
                                              f"{get_definition}\n\n" +
                                              f"**Example ->**\n" +
                                              f"{get_example}",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @command(name="8ball", aliases=["8b"])
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_8ball(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        await ctx.send(f"{ctx.author.mention}, {choice(self._8ballResponse)}")

    @command(name="rps")
    @cooldown(1, 5, BucketType.user)
    async def fun_rock_paper_scissors(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        def check(m):
            return m.author == ctx.author

        rps = ["Rock", "Paper", "Scissors",
               "Rock", "Paper", "Scissors",
               "Rock", "Paper", "Scissors",
               "Rock", "Paper", "Scissors",
               "Rock", "Paper", "Scissors"]
        rps_choice = choice(rps).lower()
        await ctx.send("Please choose either: Rock, Paper or Scissors")
        user_input = await self.bot.wait_for("message", timeout=10, check=check)
        user_input_str = str(user_input.content).lower()

        if user_input_str == rps_choice.lower():
            await ctx.send("You got the same. Retry?")

        elif user_input_str == "rock":
            if rps_choice == "paper":
                await ctx.send("You lost loser!!")
            elif rps_choice == "scissors":
                await ctx.send("The bot got scissors. You won! GG")

        elif user_input_str == "paper":
            if rps_choice == "scissors":
                await ctx.send("You lost loser!!")
            elif rps_choice == "rock":
                await ctx.send("The bot got rock. You won! GG")

        elif user_input_str == "scissors":
            if rps_choice == "rock":
                await ctx.send("You lost loser!!")
            elif rps_choice == "paper":
                await ctx.send("The bot got paper. You won! GG")

        else:
            await ctx.send("You did not choose Rock, Paper or Scissors")

    @command(name="rng")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_rng(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        def check(m):
            return m.author == ctx.author

        random_number = randint(1, 10)
        await ctx.send("Please guess from a number 1 - 10")
        user_input = await self.bot.wait_for("message", timeout=10, check=check)
        user_input_str = str(user_input.content)

        if user_input_str == str(random_number):
            await ctx.send("GG you guessed the number correctly!")
        else:
            await ctx.send(f"You guessed it wrong the bots answer was {random_number}! Try again maybe?")

    @command(name="penis", aliases=["pp", "schlong"])
    async def fun_penis(self, ctx, *, arg: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if arg is None:
            arg = ctx.author
        pp_size = choice(self.pp_sizes)
        pp_message = utils.embed_message(message=f"{arg}'s pp size\n" +
                                                 f"8{'=' * pp_size}D",
                                         footer_icon=self.bot.user.avatar_url,
                                         footer_text=utils.random_message())
        await ctx.send(embed=pp_message)

    @command(name="fact", aliases=["randomfact"])
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_randomfact(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        api_url = "https://uselessfacts.jsph.pl/random.json?language=en"
        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                fact = data["text"]
                fact_id = data["id"]

                fact_message = utils.embed_message(title="Random Fact:",
                                                   message=fact,
                                                   footer_icon=self.bot.user.avatar_url,
                                                   footer_text=f"Fact ID: {fact_id}")
                await ctx.send(embed=fact_message)

    @command(name="poll")
    @cooldown(1, standard_cooldown, BucketType.member)
    async def fun_poll(self, ctx, *, poll_q):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        poll_embed = utils.embed_message(title="User Poll",
                                         message=poll_q,
                                         footer_icon=self.bot.user.avatar_url,
                                         footer_text=f"Poll by -> {ctx.author}")
        poll = await ctx.send(embed=poll_embed)
        await poll.add_reaction("👍")
        await poll.add_reaction("👎")
        await poll.add_reaction("🤷‍♀️")

def setup(bot):
    bot.add_cog(Fun(bot))