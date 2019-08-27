import discord
import os
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle
import random

# CONFIG
# ---------
prefix="!!" # This will be used at the start of commands.
client = commands.Bot(command_prefix = prefix)#Leave this alone unless you know what you're doing
activity=discord.Game(name="with memes") #This will display as the activity on Discord.
status=cycle(['U Gay', 'No u']) #Status to cycle through
bad_words=["bad", "bad2"]#Words that will automatically be deleted
join_role="Member" #This role will automcatically be given to members who join
joinleave=client.get_channel(615477865961619478)#Insert the ID of the channel that you want join and leave messages to appear in.
token = open("token.txt","r").read()
# ----------

@client.event
async def on_ready():
	print("Everything is all G baws")
	change_status.start()
	#await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)


@client.event
async def on_member_join(member):
	print(f'{member} joined the server')
	await joinleave.send("Oof we've got another crate of autism incoming - its name is {member}")

@client.event
async def on_member_remove(member):
	print(f'{member} left the server')
	await joinleave.send("Kthx cya, {member} left")

##@client.event
##async def on_member_join(member, * role: discord.Role):
	##user = member
	##await user.add_roles(join_role)

##@client.event ##Universal argument error
##async def on_command_error(ctx, error):
	##if isinstance(error, commands.MissingRequiredArgument):
		##await ctx.send('You forgot to specify an argument!')

@client.command()
@commands.has_permissions(manage_messages="true")
async def clear(ctx, amount=5):
	##amount = amount + 1
	await ctx.channel.purge(limit=amount)
	print("cleared")

@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('You forgot to specify how many messages to clear!')

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'Kicked {user.mention}')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {user.mention}')

@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_tag = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_tag):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')
			return

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
	client.unload_extenstion(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')

@client.command()
async def ping(ctx):
	ping = round(client.latency * 1000)
	await ctx.send(f'bruh. I aint gonna say pong, instead here is my latency - {ping}ms')

@client.command()
async def nigga(ctx):
	responses = ['https://www.askideas.com/media/23/African-Girl-Weird-Face-Funny-Image.jpg',
				'http://kenyanurse.com/wp-content/flagallery/ian-leave-from-school/bush-man-found-my-camera.jpg', 
				'https://scontent.fsyd7-1.fna.fbcdn.net/v/t1.0-9/49103433_1591522480994599_361774789083267072_n.jpg?_nc_cat=105&_nc_oc=AQkKLCYZlmR_A6vo6Bz7EEoa3KELtbOY2nW3t896XH7DmKxKgP0tZMusN8_9auTCP_0&_nc_ht=scontent.fsyd7-1.fna&oh=f035ecbb579a8c67b9f9b43726e686f3&oe=5DA47E5A']
	await ctx.send(f'Here is your nig: \n{random.choice(responses)}')

@tasks.loop(seconds=10)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))


##@client.event ## NOT WORKING AT THE MOMENT
##async def on_message(message):
   ## if message.author == client.user:
      ##  return

    ##if message.content.startswith('no u'):
      ##  await message.channel.send('https://i.imgur.com/yXEiYQ4.jpg')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(token.strip())
