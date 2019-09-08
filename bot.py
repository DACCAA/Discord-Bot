from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import find
import discord
import platform
import json
import random
import requests

searchPhrases = ['Let me just check that...', 'Checking my sources...', 'Okay, lets have a look...', 'Cogitating...', 'Thinking...', 'Coming right up...', 'Lets get my cogs turning...']
helloPhrases = ['Hey', 'Hi', 'Hello', 'Howdy', 'Yo', 'How is it hanging', 'Bonjour', 'Guten Tag!']

client = Bot(description="DACCAA Bot", command_prefix="~", pm_help = False)

@client.event
async def on_ready():
	print('Logged in as ' + client.user.name + ' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	
	print('Servers connected to:')
	for server in client.servers:
		print(server.name)
	
	return await client.change_presence(game=discord.Game(name='DACCAA.com'))

def smartSearch(query):
	r = requests.get('https://daccaa.com/search/engine/?query=' + str(query))
	data = r.json()
	data = json.dumps(data)
	data = json.loads(data)

	if data['answer'] == None:
		return data['error']

	return data['answer']



@client.command(pass_context=True)
async def search(ctx, *, query = ""):
	''' Does a DACCAA Smart Search '''
	if query == "":
		await client.say("Sample usage: ```~search How tall is Big Ben?```")
	else:
		await client.say(random.choice(searchPhrases))
		await client.say(smartSearch(query))

@client.command(pass_context=True)
async def dave(ctx, *, query = ""):
	''' Talks to DACCAA Dave '''

	#print(ctx.message.author.name)
	#print(ctx.message.author.id)

	if query == "":
		await client.say("Sample usage: ```~dave Hello```")
	else:
		r = requests.get('https://daccaa.com/dave/api.php?discord=' + str(ctx.message.author.id) + '&query=' + str(query))
		data = r.json()
		data = json.dumps(data)
		data = json.loads(data)

		if data['status'] == "unknown":
			unsure = ["I don't know how to do that yet.", "Hmm... I am unsure.", "Sorry, you appear to have confused me.", "I don't know how to help you with that."]
			await client.say(random.choice(unsure) + " You can teach me at https://daccaa.com/dave/teach.php?invoke="+ (query.replace(" ", "+")).replace("?", "%3F") + " - you must be logged in.")
			return
		
		embed = discord.Embed(title=data['output'], colour=discord.Colour(0x99cc))

		if data['discordAction'] != None:
			embed.set_image(url=data['discordAction'])
			
		embed.set_author(name="Dave", url="https://daccaa.com/dave/", icon_url="https://daccaa.com/Storage_new/2018/small/dave-small.png")
		await client.say(embed=embed)

@client.command(pass_context=True)
async def alig(ctx):
	'''Gets a random Ali G video '''

	r = requests.get('https://daccaa.com/discord/remote-data/alig.php')
	data = r.json()
	data = json.dumps(data)
	data = json.loads(data)

	alig = data['url']

	await client.say(alig)
	
client.run('') # Add your code here
