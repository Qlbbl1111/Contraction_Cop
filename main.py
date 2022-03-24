from dotenv import load_dotenv
import discord, json, os, re
from discord.ext import commands

dir = os.path.dirname(__file__)

load_dotenv(os.path.join(dir, ".env"))

prefixpath = os.path.join(dir, 'settings', 'prefix.json')
deletepath = os.path.join(dir, 'settings', 'delete.json')

#making settings folder and file if not already made
if os.path.isdir(os.path.join(dir, 'settings')):
    pass
else:
    os.mkdir(os.path.join(dir, 'settings'))
    
if os.path.isdir(prefixpath):
    pass
else:
    os.mkdir(prefixpath)
    
if os.path.isdir(deletepath):
    pass
else:
    os.mkdir(deletepath)

def get_prefix(client, message):
    with open(prefixpath, 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def get_delete(client, message):
    with open(deletepath, 'r') as f:
        deletes = json.load(f)
    return deletes[str(message.guild.id)]


bot = commands.Bot(command_prefix=(get_prefix))
bot.remove_command("help") #makes it so my custom help command works

#list of contractions
contractions = open(os.path.join(dir, 'contractions.txt')).read().splitlines()

#bot startup
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="cc!help"))

#creates guild settings
@bot.event
async def on_guild_join(guild):
    with open(prefixpath, 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'cc!'

    with open(prefixpath, 'w') as f:
        json.dump(prefixes, f, indent=4)
        
    with open(deletepath, 'r') as f:
        deletes = json.load(f)
        
    deletes[str(guild.id)] = "True"

    with open(deletepath, 'w') as f:
        json.dump(deletes, f, indent=4)

#removes guild settings
@bot.event
async def on_guild_remove(guild):
    with open(prefixpath, 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open(prefixpath, 'w') as f:
        json.dump(prefixes, f, indent=4)
        
    with open(deletepath, 'r') as f:
        deletes = json.load(f)
        
    deletes.pop(str(guild.id))
    
    with open(deletepath, 'w') as f:
        json.dump(deletes, f, indent=4)

#message checker and responder for contractions
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    for c in contractions:
        for m in str(message.content).split():
            if re.match(c, m, re.IGNORECASE):
                delete = get_delete(bot, message)
                if delete == "False":
                    await message.reply(f"Hey! <@{str(message.author.id)}> that is a big no no")
                    return
                elif delete == "True":
                    await message.delete()                    
                    await message.author.send("Oops you just said a no no")
                    return
    await bot.process_commands(message)

#help command
@bot.command()
async def help(ctx):
    prefix = get_prefix(bot, ctx.message)
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Contraction Cop Help",
      "color": 0,
      "description": "This is a list of commands use any to bring up further info",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
        {
          "name": f"{prefix}help",
          "value": "you just used this"
        },
        {
          "name": f"{prefix}settings",
          "value": "used to configure the bot"
        }
      ]
    }
  ))    

#settings command
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def settings(ctx, setting, args):
    prefix = get_prefix(bot, ctx.message)
    
    if setting == "prefix" and args:
        with open(prefixpath, 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = args

        with open(prefixpath, 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to: {args}')
     
    elif setting == "delete" and args == "on":
        
        with open(deletepath, 'r') as f:
            deletes = json.load(f)

        deletes[str(ctx.guild.id)] = "True"

        with open(deletepath, 'w') as f:
            json.dump(deletes, f, indent=4)
            
        await ctx.send(f'Deleting is now: {args}')
    
    elif setting == "delete" and args == "off":
        
        with open(deletepath, 'r') as f:
            deletes = json.load(f)

        deletes[str(ctx.guild.id)] = "False"

        with open(deletepath, 'w') as f:
            json.dump(deletes, f, indent=4)
            
        await ctx.send(f'Deleting is now: {args}')
        
#settings help message if there is no args
@settings.error
async def flip_error(ctx, error):
    prefix = get_prefix(bot, ctx.message)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=discord.Embed.from_dict({
             "title": "List Of Settings",
             "color": 0,
             "timestamp": "",
             "author": {},
             "image": {},
             "thumbnail": {},
             "footer": {},
             "fields": [
               {
                 "name": "prefix",
                 "value": f"used to change bot prefix\nusage: {prefix}settings prefix <new prefix>"
               },
               {
                 "name": "delete",
                 "value": f"changes if the bot deletes messages or just warns\nusage: {prefix}settings delete <on/off>"
               }
             ]
           }))

if __name__ == '___main__': 
    pass

#runs bot using KEY enviroment vaiable gotten from .env
bot.run(os.environ.get("KEY"))