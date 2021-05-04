import discord
from discord.ext import commands
import sqlite3

class LeaderBoard(commands.Cog):
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
			if args[0] in ("leaderboard","leadboard", "rankboard","lb"):
				all_members = guild.members
				member_list = []
				for i in all_members:
					user_id = i.id
					c.execute("SELECT * FROM user WHERE userid = :userid", {"userid": user_id})
					fetched_user = c.fetchall()
					if len(fetched_user) != 0:
						user_dict = {
						"username": str(i),
						"level": fetched_user[0][2],
						"exp": fetched_user[0][3]
						}
						member_list.append(user_dict)

				def check(e):
					return e["exp"]
				member_list.sort(reverse=True,key=check)

				page = 1
				pagemax = int(len(member_list)/10)
				if len(args) != 1:
					page = int(args[1])
					if page <= 0:
						page = 1
					if page > 0:
						if page > pagemax:
							page = pagemax
				if page == 1:
					start = 0
					end = (page*10)+1
				elif page == pagemax:
					start = (page-1)*10
					end = len(member_list)
				else:
					start = (page-1)*10
					end = (page*10)+1
				string = ""
				for m in member_list[start:end]:
					string += f"**{member_list.index(m)+1}**-**{m['username']}**(lvl:{m['level']}|exp:{m['exp']})\n"
				color = discord.Colour.from_rgb(154,223,176)
				embed = discord.Embed(
					title=f"{guild.name} leaderboard",
					description=f"**page:{page}/{pagemax}**\n \n{string}",
					color=color)
				embed.set_footer(text=f"Requested by: {author.name}", icon_url=author.avatar_url)
				await ch.send(embed=embed)

def setup(bot):
	bot.add_cog(LeaderBoard(bot))