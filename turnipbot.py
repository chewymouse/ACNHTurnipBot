import discord
import random
from discord.ext import commands
from datetime import datetime, timedelta

server = [SERVERID]; #server ID goes here 

bot = commands.Bot(command_prefix='$')

qdict = {} 
#key: queue code
#value: dodocode, price, discord_id

qTimeDict = {} 
#key: queue code
#value: last dodocode release datetime

authorDict = {}
#key: discord_id
#value: queue code 

@bot.event
async def on_ready():
	print("ready!")

@bot.command()
async def announce(ctx, price: int, dodocode: str, AMPM: str, timezone:int):
	if (AMPM == 'AM'):
		time = '12PM'
	else:
		time = '10PM'

	code = random.randint(100,999)
	uniquecode = False;

	while (not uniquecode):
		if (code in qdict):
			code = random.randint(100,999)
		else:
			qdict[code] = dodocode + " " + str(price) + " " + str(ctx.message.author.id);
			qTimeDict[code] = datetime.now() - timedelta(minutes = 5)
			authorDict[ctx.message.author.id] = code;
			uniquecode = True;

	await bot.get_channel(server).send(':rotating_light: \nTURNIPS BEING BOUGHT AT '+ ctx.message.author.name + '\'S FOR ' + str(price) + '\nPRICES GOOD UNTIL ' + time + ' GMT ' + str(timezone) + '\nQUEUE CODE: '+ str(code)+ '\nBE COURTEOUS!')

@bot.command()
async def denounce(ctx):
	del qdict[authorDict[ctx.message.author.id]]
	await ctx.message.author.send("Removed announce for your island.")

@bot.command()
async def qcode(ctx, qcode: int):
	user = ctx.message.author
	if (qcode in qdict):
		if (datetime.now() - qTimeDict[qcode] > timedelta(minutes = 5)):
			qTimeDict[qcode] = datetime.now()
			await user.send(":onion:\nDodo Code: " + qdict[qcode].split()[0] + "\nPrice: " + qdict[qcode].split()[1] + "\nPlease do not share this.")
		else:
			await user.send(":x:\nDodo Code recently requested!\nPlease wait " + "{:0.2f}".format(5-(datetime.now() - qTimeDict[qcode]).total_seconds()/60) + " minutes!")
	else:
		await user.send("Invalid Queue Code!");

@bot.command()
async def listhelp(ctx):
	await bot.get_channel(server).send("""
		:onion:
		\n__**Commands**__
		\n```$listhelp: you're here now.```
		\n```$announce: PLEASE DM $announce TO BOT. Announces your turnip buying. Format is:
		\n       Price, Dodo Code, AM/PM ["AM" or "PM" only], Time Zone [GMT integer] separated by spaces
		\n       Example: $announce 500 F4KCD AM -7 
		\n       AGAIN, PLEASE DM SA_ACNH Turnip Bot $announce TO HIDE DODO CODE.```
		\n```$denounce: removes your announce.```
		\n```$qcode: request Dodo Code for announced hosts.
		\n        Format is: $qcode [Queue Code] 
		\n        There is a 5 minute delay between queue code requests for each host to allow for uninterrupted buying.```
		\n```$ticker: lists all current queue codes and turnip prices.```
		""");

@bot.command()
async def ticker(ctx):
	tape = ""

	for key in qdict:
		print(key)
		tape = tape + "\nQueue Code: " + str(key) + " Price: " + qdict[key].split()[1]

	if tape == "":
		tape = "No current buyers."
	await bot.get_channel(server).send("```"+tape+"```")

bot.run('[BOT TOKEN GOES HERE]') #Discord Bot token goes here
