import discord
from discord.ext import commands

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		guild = message.guild
		author = message.author
		ch = message.channel
		if message.content[:3] == "up!":
			args = message.content[3:].split(" ")
			if args[0] == "help":
				color = discord.Colour.from_rgb(154,223,176)
				if len(args) == 1:
					embed = discord.Embed(
						title="Help Arrived",
						color=color,
						description="""If you wanna know all the commands for the user, please say ``up!help user``
						\n \nIf you wanna know all the commands for server, please say ``up!help server``
						\n \nIf you wanna know how to change the settings for the server, please say ``up!help settings``\
						\n \nIf you wanna get the invite link for the bot, please say ``up!invite``
						\n \nJoin our support server: [Invite Link](https://discord.gg/mAyYgfkqU8)""")
					await ch.send(embed=embed)
				elif args[1] == "user":
					embed = discord.Embed(
						title="Help - User",
						color=color,
						description="""Check your level,rank and exp with ``up!lvl``
						\n \nChange your theme with ``up!theme choice``(replace `choice` with your choice of theme)
						\n \nCheck the leaderboard of a server with ``up!leaderboard page``(replace the page with the leaderboard page no. you wanna see)""")
					await ch.send(embed=embed)
				elif args[1] == "server":
					embed = discord.Embed(
						title="Help - Server",
						color=color,
						description="""Register the server with ``up!register``
						\n \nAdd a role reward with ``up!setup role(ping the reward role) level(say level which the reward is for)``
						\n \nAdd a channel to ignore list with ``up!ignore-channel add channel(mention the channel you wanna add to the ignore list)``
						\n \nRemove a channel from ignore list with ``up!ignore-channel remove channel(mention the channel you wanna remove to the ignore list)``
						\n \nReset everyone's level and exp with ``up!server reset``""")
					await ch.send(embed=embed)
				elif args[1] == "settings":
					embed = discord.Embed(
						title="Help - Server Settings",
						color=color,
						description="""Turn leveling message DM on/off with ``up!server dm on/off``
						\n \nChange the channel to send the leveling message with ``up!server channel mention(mention the channel you want to be the leveling message channel)``""")
					await ch.send(embed=embed)

def setup(bot):
	bot.add_cog(Help(bot))