import discord
from discord import guild
from sqlitedict import SqliteDict
from discord.ext import commands
import settings

intents = discord.Intents.default()

client = commands.Bot(command_prefix=settings.Prefix, help_command=None, intents=intents)


def save(key, value, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict[key] = value  # Using dict[key] to store
            mydict.commit()  # Need to commit() to actually flush the data
    except Exception as ex:
        print("Error during storing data (Possibly unsupported):", ex)


def pop(key, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict.pop(key)  # Using dict[key] to store
            mydict.commit()  # Need to commit() to actually flush the data
    except Exception as ex:
        print("Error during poping data (Possibly unsupported):", ex)


def load(key, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            value = mydict[key]  # No need to use commit(), since we are only loading data!
        return value
    except Exception as ex:
        print("Error during loading data:", ex)


def load_all(cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            val = mydict.keys()
            for i in val:
                print(f"{i}: {mydict[i]}")
        pass
    except Exception as ex:
        print("Error during loading data:", ex)


def who(ctx):
    if ctx.channel.id == 982224998309716018:
        return "Nastya.sqlite3"
    if ctx.channel.id == 984396714746187786:
        return "Test.sqlite3"
    if ctx.channel.id == 983437334160760902:
        return "Andre.sqlite3"
    else:
        return "cache.sqlite3"


def hp_up(ctx):
    char = who(ctx)
    max_hp = int(load("max_hp", char))
    if char == "Nastya.sqlite3":
        max_hp += 8
        save("max_hp", max_hp, char)
        save("hp", max_hp, char)
        return "Получено +8 хп за уровень"
    if char == "Test.sqlite3":
        max_hp += 8
        save("max_hp", max_hp, char)
        save("hp", max_hp, char)
        return "Получено +8 хп за уровень"


# class СharacterSheet:
#     def __init__(self, name, id_play, id_char, ST=10, DX=10, IQ=10, HT=10):
#         self.id_play = id_play
#         self.id_char = id_char
#         self.name = name
#         self.ST = ST
#         self.DX = DX
#         self.IQ = IQ
#         self.HT = HT
#         self.HP = ST
#         self.WILL = IQ
#         self.PER = IQ
#         self.FP = HT
#         self.SPEED = (HT + DX) / 4
#         self.MOVE = round((HT + DX) / 4)
#         self.unspent_points = 2
#
#     Characters = []


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
    СharacterSheet.Characters.append(NewChar)
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
    )
    await channel.send(f"У вас непотрачено {NewChar.unspent_points} очка навыков")


@client.command()
async def status(ctx):
    guild = ctx.guild
    channel = ctx.channel
    if channel.id == 982224998309716018:
        channel2 = discord.utils.get(guild.text_channels, id=982260623805124609)
        messages = await channel2.history(limit=200).flatten()
        for message in messages:
            await channel.send(message.content)


@client.command()
async def inventory(ctx):
    guild = ctx.guild
    channel = ctx.channel
    if channel.id == 982224998309716018:
        channel2 = discord.utils.get(guild.text_channels, id=982225206259089518)
        messages = await channel2.history(limit=200).flatten()
        for message in messages:
            await channel.send(message.content)


@client.command()
async def dict_add(ctx, key, value):
    print("-----")
    print(f'Пытаемся добваить {key} с значением {value} в {who(ctx)}')
    save(key, value, who(ctx))
    print(load_all(who(ctx)))


@client.command()
async def dict_load(ctx, key):
    print("-----")
    print(f"{key}: {load(key, who(ctx))}")
    print(type(load(key, who(ctx))))


@client.command()
async def info(ctx):
    char = who(ctx)
    channel = ctx.channel
    lvl = int(load('lvl', char))
    max_exp = settings.lvlupexp[int(lvl + 1)]
    print("-----")
    print(load_all(who(ctx)))
    await channel.send(f"Уровень: {lvl}\n"
                       f"Опыт: {load('actual_exp', char)}/{max_exp}\n"
                       f"Хп: {load('hp', char)}/{load('max_hp', char)}")


@client.command()
async def dict_pop(ctx, key):
    print("-----")
    print(f'Пытаемся удалить {key} из {who(ctx)}')
    pop(key, who(ctx))
    print(load_all(who(ctx)))


@client.command()
async def exp(ctx, value):
    channel = ctx.channel
    value = int(value)
    lvl = int(load("lvl", who(ctx)))
    actual_exp = load("actual_exp", who(ctx))
    actual_exp = int(actual_exp)
    max_exp = int(settings.lvlupexp[int(lvl + 1)])
    actual_exp += value
    skill_point = int(load("skill_point", who(ctx)))
    upgrade_point = int(load("upgrade_point", who(ctx)))
    evolution_point = int(load("evolution_point", who(ctx)))
    while actual_exp >= max_exp:
        lvl += 1
        await channel.send(f"**Получен {lvl} уровень**")
        await channel.send(hp_up(ctx))
        await channel.send("Получен поинт навыка")
        skill_point += 1
        if lvl % 5 == 0:
            await channel.send("Получен поинт улучшения")
            upgrade_point += 1
        if lvl % 10 == 0:
            await channel.send("Получен поинт умения")
            evolution_point += 1
        actual_exp -= max_exp
        max_exp = settings.lvlupexp[lvl]
    save("lvl", lvl, who(ctx))
    save("actual_exp", actual_exp, who(ctx))
    save("skill_point", skill_point, who(ctx))
    save("upgrade_point", upgrade_point, who(ctx))
    save("evolution_point", evolution_point, who(ctx))

    await channel.send(f"Уровень: {lvl}\nОпыт: {actual_exp}/{max_exp}\n"
                       f"Очки умения: {skill_point}\n"
                       f"Очки улучшения: {upgrade_point}\n"
                       f"Очки эволюции: {evolution_point}\n")


@client.command()
async def hp(ctx, value):
    channel = ctx.channel
    value = int(value)
    hp = int(load("hp", who(ctx)))
    max_hp = int(load("max_hp", who(ctx)))
    hp += value
    save("hp", hp, who(ctx))
    await channel.send(f"Здоровье: {hp}/{max_hp}")


@client.command()
async def chaos(ctx, value):
    channel = ctx.channel
    value = int(value)
    chaos = int(load("chaos", who(ctx)))
    chaos += value
    save("chaos", chaos, who(ctx))
    await channel.send(f"Энергия Хаоса: {chaos}/∞")


@client.command()
async def chaos_info(ctx):
    channel = ctx.channel
    await channel.send(f"Энергия Хаоса: {int(load('chaos', who(ctx)))}/∞")


save("Титулы", ['Test1', 'test2'], "Nastya.sqlite3")
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
