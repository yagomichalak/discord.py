import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
from pprint import pprint
import asyncio

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
token = os.getenv('TOKEN')

@client.event
async def on_ready():
    print('BOT is online!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can't do that!")

    print(error)

@client.event
async def on_button_click(components):

    # print('opa')
    # print(components)
    pass

@client.command()
async def test(ctx) -> None:
    await ctx.send(f"Command successfully tested!")
# @client.event
# async def on_socket_response(data):

#     if data['t'] != 'INTERACTION_CREATE':
#         return



@client.event
async def on_interaction_update(message, member, button, response):
    print('NORMAL!')
    print('message=', message)
    print()
    print('member=', member)
    print()
    print('button=', button)

    print()
    # button.ping(response)
    button.defer(response)
    await asyncio.sleep(2)
    button.update_response(response, "opa opa")
    # await message.edit(content='hey')
    # button.update(response)


@client.event
async def on_raw_interaction_update(payload, user, button, response):
    # print('RAW!')
    # print('payload=', payload)
    # print()
    # print('user=', user)
    # print(itoken)

    button.success(response)

@client.command()
async def cc(ctx) -> None:

    components = []
    for i in range(5):
        component = discord.Component()
        for ii in range(5):
            component.add_button(label=f"Btn {ii+1}", style=5, url="https://thelanguagesloth.com", emoji='🦥')
        components.append(component)


    # client.dispatch("button_click", components)

    opa = await ctx.send(embed=discord.Embed(title='hey'), components=components)
    # print(opa.embeds)
    # print()
    # print(opa.components)

@client.command()
async def compo(ctx) -> None:

    compo = discord.Component()
    compo.add_button(label=f"Btn 1!", style=1, custom_id=f"btn_1_id", emoji="<:transmutated_sloth:839509433159385090>")
    compo.add_button(label=f"Btn 2!", style=1, custom_id=f"btn_2_id", emoji="🧑‍🏫")
    compo.add_button(label=f"Btn 3!", style=1, custom_id=f"btn_3_id", emoji="<a:hackerman:802354539184259082>")
    await ctx.send('something', components=[compo])


# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         client.load_extension(f"cogs.{filename[:-3]}")

# @client.command(hidden=True)
# @commands.has_permissions(administrator=True)
# async def load(ctx, extension: str = None):
#     '''
#     Loads a cog.
#     :param extension: The cog.
#     '''
#     if not extension:
#         return await ctx.send("**Inform the cog!**")
#     client.load_extension(f'cogs.{extension}')
#     return await ctx.send(f"**{extension} loaded!**", delete_after=3)


# @client.command(hidden=True)
# @commands.has_permissions(administrator=True)
# async def unload(ctx, extension: str = None):
#     '''
#     Unloads a cog.
#     :param extension: The cog.
#     '''
#     if not extension:
#         return await ctx.send("**Inform the cog!**")
#     client.unload_extension(f'cogs.{extension}')
#     return await ctx.send(f"**{extension} unloaded!**", delete_after=3)


# @client.command(hidden=True)
# @commands.has_permissions(administrator=True)
# async def reload(ctx, extension: str = None):
#     '''
#     Reloads a cog.
#     :param extension: The cog.
#     '''
#     if not extension:
#         return await ctx.send("**Inform the cog!**")
#     client.unload_extension(f'cogs.{extension}')
#     client.load_extension(f'cogs.{extension}')
#     return await ctx.send(f"**{extension} reloaded!**", delete_after=3)

client.run(token)