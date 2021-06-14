import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
from boto.s3.connection import S3Connection

intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.members = True

# .env setup
try:
    s3 = S3Connection(os.environ['AFFILIATE_BOT_TOKEN'])
    print('loaded config vars')
except:
    load_dotenv()
    print('loaded local env vars')

token = os.getenv('AFFILIATE_BOT_TOKEN')
bot = commands.Bot(command_prefix='r.', case_insensitive=True, chunk_guilds_at_startup=False, intents=intents)
bot.remove_command('help')

owner_id = 219966414486896640
guild_id = 574688313919799327
reward_role_id = 806516503565959188

# The links people can put to get the reward role
links = [
        'https://top.gg/bot/576181953372356638',
        'https://dsc.gg/challenger',
        'https://bots.discordlabs.org/bot/challenger',
        'https://discord.gg/53BC4n2',
        'https://discord.com/invite/53BC4n2'
    ]

@bot.event
async def on_ready():
    print(f"{bot.user} logged into {len(bot.guilds)} servers")
    game = discord.Game(f'r.help | Rewarding supporters!')
    await bot.change_presence(status=discord.Status.online, activity=game)
    await (bot.get_guild(guild_id)).chunk()
    if not affiliate_program.is_running():
        affiliate_program.start()

# Gives the reward role to whoever has one of the links in their status
@tasks.loop(seconds=120)
async def affiliate_program():
    guild = bot.get_guild(guild_id)
    role = guild.get_role(reward_role_id)
    for member in set(guild.members):
        if bool([v for v in links if v in str(member.activity)]):
            await member.add_roles(role)
            print(f'{member.name} has been given Premium')
        else:
            await member.remove_roles(role)

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000,2)} ms')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='What is this bot?', description='This bot rewards free **Challenger Premium** to users who have <@576181953372356638>\'s invite link in their custom status. [Read more about Premium here](https://www.patreon.com/ovikx?fan_landing=true)', color=discord.Color.blurple())
    embed.add_field(name='Put one of these links in your status to get Premium', value='\n'.join([f'`{i+1}` [{v}]({v})' for i, v in enumerate(links)]))
    embed.add_field(name='Important Notes', value='- Premium is removed when the user removes the link from their status\n- It may take up to two minutes to receive a free Premium subscription', inline=False)
    embed.add_field(name='Suggest links!', value=f'If you want to add a link to the list above, please DM `{bot.get_user(owner_id)}`.')
    await ctx.send(embed=embed)

bot.run(token)