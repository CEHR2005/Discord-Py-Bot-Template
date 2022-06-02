import discord
from discord import guild
from discord.ext import commands

import settings

intents = discord.Intents.default()

client = commands.Bot(command_prefix=settings.Prefix, help_command=None, intents=intents)


class СharacterSheet:
    def __init__(self, name, id_play,id_char, ST=10, DX=10, IQ=10, HT=10):
        self.id_play = id_play
        self.id_char = id_char
        self.name = name
        self.ST = ST
        self.DX = DX
        self.IQ = IQ
        self.HT = HT
        self.HP = ST
        self.WILL = IQ
        self.PER = IQ
        self.FP = HT
        self.SPEED = (HT + DX) / 4
        self.MOVE = round((HT + DX) / 4)
        self.unspent_points = 2


@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(settings.BotStatus))


@client.command()
async def create(ctx, channel_name):
    channel = ctx.channel
    id_play = channel.id
    guild = ctx.guild
    channel = await guild.create_text_channel(channel_name)
    id_char = channel.id
    NewChar = СharacterSheet(name=channel_name, id_play=id_play, id_char=id_char)
    await channel.send(
        f"Имя персонажа: {NewChar.name}\n"
        f'ST: {NewChar.ST}\n'
        f'HT: {NewChar.HT}\n'
        f'DX: {NewChar.DX}\n'
        f'IQ: {NewChar.IQ}\n'
        f'PER: {NewChar.PER}\n'
        f'WILL: {NewChar.WILL}\n'
        f'MOVE: {NewChar.MOVE}\n'
        f'SPEED: {NewChar.SPEED}\n'
        f'{NewChar.id_char}\n'
        f'{NewChar.id_play}\n'
    )


@client.command()
async def print_info(ctx):
    channel = discord.utils.get(ctx.guild.channels, name='')
    too = ctx.channel.name
    messages = await channel.history(limit=123).flatten()
    await too.send(messages)


# @client.command()
# async def spent(ctx, points, stat):

# @client.event
# async def on_message(message):
#     username = str(message.author).split("#")[0]
#     user_message = str(message.content)
#     channel = str(message.channel.name)
#     print(f"{username}: {user_message} ({channel})")
#
#     if message.author == client.user:
#         return
#     if user_message == 'Войти':
#         channel = discord.utils.get(client.get_all_channels(), name=f'{username}')
#
#         if not channel:
#             channel = await guild.create_text_channel(username)
#             await message.channel.send('Чарник создан')


client.run(settings.TOKEN)
