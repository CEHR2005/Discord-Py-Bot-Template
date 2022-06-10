import discord
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
    if char == "Andre.sqlite3":
        max_hp += 8
        save("max_hp", max_hp, char)
        save("hp", max_hp, char)
        return "Получено +8 хп за уровень"
    if char == "Test.sqlite3":
        ht = int(load("ht", char))
        max_hp += 8 + (ht - 10)
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
    print(f'Пытаемся добавить {key} с значением {value} в {who(ctx)}')
    save(key, value, who(ctx))
    print(load_all(who(ctx)))

@client.command()
async def dict_add_skill(ctx, key, stat, value):
    print("-----")
    value = int(value)
    stat = int(load(f"{stat}", who(ctx)))
    value = value + stat - 1
    print(f'Пытаемся добавить {key} с значением {value} в {who(ctx)}')
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
    actual_exp = int(load("actual_exp", who(ctx)))
    skill_point = int(load("skill_point", who(ctx)))
    upgrade_point = int(load("upgrade_point", who(ctx)))
    evolution_point = int(load("evolution_point", who(ctx)))
    st = int(load("st", who(ctx)))
    dx = int(load("dx", who(ctx)))
    ht = int(load("ht", who(ctx)))
    intelligence = int(load("int", who(ctx)))
    print("-----")
    print(load_all(who(ctx)))
    await channel.send(
        f"Уровень: {lvl}\n"
        f"Опыт: {load('actual_exp', char)}/{max_exp}\n"
        f"ST: {st}\n"
        f"DX: {dx}\n"
        f"HT: {ht}\n"
        f"INT: {intelligence}\n"
        f"Хп: {load('hp', char)}/{load('max_hp', char)}\n"
        f"Очки умения: {skill_point}\n"
        f"Очки улучшения: {upgrade_point}\n"
        f"Очки эволюции: {evolution_point}\n"
    )


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
    actual_exp = int(load("actual_exp", who(ctx)))
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
        max_exp = settings.lvlupexp[lvl+1]
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

@client.command()
async def dr(ctx):
    channel = ctx.channel
    Torso_dr = int(load("Torso_dr", who(ctx)))
    Skull_dr = int(load("Skull_dr", who(ctx)))
    Eye_dr = int(load("Eye_dr", who(ctx)))
    Face_dr = int(load("Face_dr", who(ctx)))
    Neck_dr = int(load("Neck_dr", who(ctx)))
    Groin_dr = int(load("Groin_dr", who(ctx)))
    Arm_dr = int(load("Arm_dr", who(ctx)))
    Leg_dr = int(load("Leg_dr", who(ctx)))
    Hands_dr = int(load("Hands_dr", who(ctx)))
    Feet_dr = int(load("Feet_dr", who(ctx)))
    All_dr = int(load("All_dr", who(ctx)))
    await channel.send(
        f"Общий: {All_dr}\n"
        f"Торс(0): {Torso_dr+All_dr}\n"
        f"Череп(-7): {Skull_dr+All_dr}\n"
        f"Урон x4\n"
        f"Глаза(-9): {Eye_dr+All_dr}\n"
        f"Урон x4, может ослепить\n"
        f"Лицо(-5): {Face_dr+All_dr}\n"
        f"Шея(-5): {Neck_dr+All_dr}\n"
        f"Дробящий и разъедающий урон ×1.5, режущий ×2.\n"
        f"Пах(-3): {Groin_dr+All_dr}\n"
        f"Руки(-2): {Arm_dr+All_dr}\n"
        f"Ноги(-2): {Leg_dr+All_dr}\n"
        f"Кисти(-4): {Hands_dr+All_dr}\n"
        f"Ступни(-4): {Feet_dr+All_dr}\n"
    )

@client.command()
async def dr_gen(ctx):
    save('Torso_dr', 0, who(ctx))
    save('Skull_dr', 2, who(ctx))
    save('Eye_dr', 0, who(ctx))
    save('Face_dr', 0, who(ctx))
    save('Neck_dr', 0, who(ctx))
    save('Groin_dr', 0, who(ctx))
    save('Arm_dr', 0, who(ctx))
    save('Leg_dr', 0, who(ctx))
    save('Hands_dr', 0, who(ctx))
    save('Feet_dr', 0, who(ctx))
    save('All_dr', 0, who(ctx))

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
