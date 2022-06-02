import discord
from discord import guild
from discord.ext import commands
import pickle
import settings

intents = discord.Intents.default()

client = commands.Bot(command_prefix=settings.Prefix, help_command=None, intents=intents)


def save_object(obj):
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)


def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)


class СharacterSheet:
    def __init__(self, name, id_play, id_char, ST=10, DX=10, IQ=10, HT=10):
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

    Characters = []


@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(settings.BotStatus))


@client.command()
async def cheak_char(ctx):
    channel = ctx.channel

    # for i in СharacterSheet.Characters:
    #     if i.play_id == channel.id:
    #         print("Yes")
    #     else:
    #         print("Nou")


@client.command()
async def create(ctx, channel_name):
    channel = ctx.channel
    id_play = channel.id
    guild = ctx.guild
    channel = await guild.create_text_channel(channel_name)
    id_char = channel.id
    NewChar = СharacterSheet(name=channel_name, id_play=id_play, id_char=id_char)
    СharacterSheet.Characters.append(NewChar)
    save_object(СharacterSheet.Characters)
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
    await channel.send(f"У вас непотрачено {NewChar.unspent_points} очка навыков")


@client.command()
async def status(ctx):
    load_object(СharacterSheet.Characters)
    guild = ctx.guild
    id_play = ctx.message.channel.id
    for pos, i in enumerate(СharacterSheet.Characters):
        if id_play == i.id_play:
            p = pos
    id = СharacterSheet.Characters[p].id_char
    channel = discord.utils.get(guild.text_channels, id=id)
    messages = await channel.history(limit=200).flatten()
    # print(messages)
    # print(messages[0].content)
    print(help(ctx))
    id = СharacterSheet.Characters[p].id_play
    channel = discord.utils.get(guild.text_channels, id=id)
    for message in messages:
        await channel.send(message.content)


# @client.command()
# async def spent(ctx, points, stat):
#     if points

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
