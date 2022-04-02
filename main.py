from dotenv import load_dotenv
import discord, json, os, re
from discord.ext import commands

dir = os.path.dirname(__file__)

load_dotenv(os.path.join(dir, ".env"))

#making settings folder and file if not already made
if os.path.isdir(os.path.join(dir, 'settings')):
    pass
else:
    os.mkdir(os.path.join(dir, 'settings'))

def joinguild(guild):
    if os.path.exists(os.path.join(f'{dir}' , 'settings', f'{guild}.json')) == True:
        return
    else:
        with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'w+') as f:
            json.dump({
                "delete" : "True",
                "prefix" : "cc!"
            }, f, indent=4)

def checkfiles(guild):
    if os.path.isdir(os.path.join(f'{dir}' , 'settings', f'{guild}.json')) == True:
        return
    else:
        joinguild(guild)
        return

def get_prefix_start(client, message):
    guild = message.guild.id
    if os.path.exists(os.path.join(f'{dir}' , 'settings', f'{guild}.json')) == True:
        pass
    else:
        joinguild(guild)
        return
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        prefix = x["prefix"]
    return prefix

def get_prefix(guild):
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        prefix = x["prefix"]
    return prefix

def set_prefix(guild, prefix):
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        jsonload = json.load(f)
        jsonload["prefix"] = prefix
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'w') as f:
        json.dump(jsonload, f, indent=4)

def get_delete(guild):
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        delete = x["delete"]
    return delete

def set_delete(guild, delete):
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        jsonload = json.load(f)
        jsonload["delete"] = delete
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'w') as f:
        json.dump(jsonload, f, indent=4)

bot = commands.Bot(command_prefix=(get_prefix_start))
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
    joinguild(guild.id)
    
#message checker and responder for contractions
@bot.listen('on_message')
async def on_message(message):
    if (message.author.bot):
        return
    if isinstance(message.channel, discord.channel.DMChannel):
        await message.reply(f"Hey! <@{str(message.author.id)}> that is a big no no")
        return
    checkfiles(message.guild.id)
    for c in contractions:
        for m in str(message.content).split():
            if re.fullmatch(c, m, re.IGNORECASE):
                delete = get_delete(message.guild.id)
                if delete == "False":
                    await message.reply(f"Hey! <@{str(message.author.id)}> that is a big no no")
                    return
                elif delete == "True":
                    await message.delete()                    
                    await message.author.send("Oops you just said a no no")
                    return

#help command
@bot.command()
async def help(ctx):
    prefix = get_prefix(ctx.guild.id)
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
    prefix = get_prefix(ctx.guild.id)
    
    if setting == "prefix" and args and len(args) <= 5:
        set_prefix(ctx.guild.id, args)
        await ctx.send(f'Prefix changed to: {args}')
        
    elif setting == "prefix" and args and len(args) >= 5:
        await ctx.send("Choosen prefix too long")
                
    elif setting == "delete" and args == "on":
        set_delete(ctx.guild.id, "True")   
        await ctx.send(f'Deleting is now: {args}')
    
    elif setting == "delete" and args == "off":
        set_delete(ctx.guild.id, "False")  
        await ctx.send(f'Deleting is now: {args}')
        
#settings help message if there is no args
@settings.error
async def flip_error(ctx, error):
    prefix = get_prefix(ctx.message.guild.id)
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
