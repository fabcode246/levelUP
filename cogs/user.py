import discord
from discord.ext import commands
import sqlite3
from pillowStuff import level_up, lvl_info, themer

class UserCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		guild = message.guild
		author = message.author
		ch = message.channel
		datafile = "dat.db"
		conn = sqlite3.connect(datafile)
		c = conn.cursor()
		c.execute(f"SELECT * FROM guild WHERE guildid = {guild.id}")
		fetched_server = c.fetchall()
		if message.content[:3] == "up!":
			args = message.content[3:].split(" ")
			if args[0] in ("lvl", "level", "rank") and len(fetched_server) != 0:
				target_user_id = author.id
				if len(args) == 2:
					target_user_id = int(args[1][3:-1])
				c.execute(f"SELECT * FROM user WHERE userid = {target_user_id} AND guildid = {guild.id}")
				fetched_result = c.fetchall()
				if len(fetched_result) != 0:
					all_members = guild.members
					fetched_list = []
					for i in all_members:
						user_id = i.id
						c.execute("SELECT * FROM user WHERE userid = :userid", {"userid": user_id})
						fetched_user = c.fetchall()
						if len(fetched_user) != 0:
							user_dict = {
							"userid": user_id,
							"username": str(i),
							"level": fetched_user[0][2],
							"exp": fetched_user[0][3]
							}
							fetched_list.append(user_dict)

					def check(e):
						return e["exp"]
					fetched_list.sort(reverse=True, key=check)

					rank = 1
					for i in fetched_list:
						if i["userid"] == target_user_id:
							break
						rank+=1

					user = guild.get_member(target_user_id)

					theme = themer(fetched_result[0][5], fetched_server[0][2])
					image = lvl_info(user.name, fetched_result[0][2], fetched_result[0][3], rank,theme)
					image.seek(0)
					await ch.send(file=discord.File(fp=image ,filename="level_info.png"))
				else:
					await ch.send("You are not registered yet lmao. chat a bit and check out later")

def setup(bot):
	bot.add_cog(UserCommands(bot))