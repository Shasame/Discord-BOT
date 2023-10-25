from discord.ext import commands
import discord
import random
from datetime import datetime, timedelta
import re
import urllib.request

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 0  # Change to your discord id

#Flood global variables
flood_active = False
flood_users = {}
x = 10
y = 1

catchphrases = [
    "les roses sont rouges, les viollettes sont bleues, je suis un poète et toi tu pues",
    "hippity hoppity, get off my property",
    "J'ai pas le temps, j'ai piscine",
]

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

########## Commands ##########

###### Step 1 ######

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def d6(ctx):
    random_number = random.randint(1,6)
    await ctx.send(random_number)

###### Step 2 ######

@bot.command()
async def admin(ctx, member: discord.Member):
    role = discord.utils.get(member.guild.roles, name="Admin")
    if not role:
        role = await ctx.guild.create_role(name="Admin", permissions=discord.Permissions.all())
    await member.add_roles(role)
    await ctx.send(f'{member.mention} est maintenant Admin !')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = catchphrases[random.randint(0, len(catchphrases) - 1)]
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} a été banni pour la raison : {reason}!')


@bot.command()
async def flood(ctx):
    global flood_active, flood_users, x, y
    flood_active = not flood_active
    flood_users = {member.id: [] for member in ctx.guild.members}
    if flood_active:
        await ctx.send(f"Le premier qui flood {x} messages en moins de {y} minutes se fait ban c'est bon pour vous ?")
    else:
        flood_users = {member.id: [] for member in ctx.guild.members}
        await ctx.send("Spammez mes lapins.")

###### Step 3 ######

@bot.command()
async def xkcd(ctx):
    response = urllib.request.urlopen('https://c.xkcd.com/random/comic/')
    html = response.read().decode('utf-8')
    img_url = re.search(r'<div id="comic">\s*<img src="([^"]+)"', html).group(1)
    img_url = "https:" + img_url
    await ctx.send(img_url)

@bot.command()
async def poll(ctx, question: str):
    await ctx.send(f"@here {question}")
    poll_message = await ctx.send(f"{question}")
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

    
########## Events ##########

@bot.event
async def on_message(message):
    global flood_active, flood_users, x, y
    if message.content == 'Salut tout le monde':
        await message.channel.send('Salut tout seul {0.author.mention}'.format(message))

    if message.author == bot.user:
        return

    if flood_active:
        flood_users[message.author.id].append(datetime.now())
        print("test")
        print(flood_users[message.author.id])
        if len(flood_users[message.author.id]) >= x:
            if flood_users[message.author.id][-1] - flood_users[message.author.id][0] < timedelta(minutes=y):
                await message.channel.send(f"Attention: {message.author.mention} ma grosse main arrive dans ta gueule!")
                flood_users[message.author.id] = flood_users[message.author.id][-x:]
    await bot.process_commands(message)



token = "YOUR TOKEN HERE"
bot.run(token)  # Starts the bot