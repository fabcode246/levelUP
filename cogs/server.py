import discord
from discord.ext import commands
import sqlite3

class Server(commands.Cog):
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
		c.execute("SELECT * FROM guild WHERE guildid = :guildid", {"guildid": guild.id})
		fetched_server = c.fetchall()
		if message.content[:3] == "up!":
			args = message.content[3:].split(" ")
			if args[0] in ("srvr", "server") and len(fetched_server) != 0 and author.guild_permissions.administrator == True:
				c.execute("SELECT * FROM user WHERE guildid = :guildid", {"guildid": guild.id})
				all_members = c.fetchall()
				if args[1] == "reset":
					for m in all_members:
						user_data = {
							"usertag": m[0],
							"userid": m[1],
							"level": 0,
							"exp": 0,
							"guildid": m[4],
							"theme": m[5]
						}
						c.execute("DELETE FROM user WHERE guildid = :guildid AND userid = :userid", {"guildid": guild.id, "userid": m[1]})
						conn.commit()
						c.execute("INSERT INTO user VALUES (:usertag, :userid, :level, :exp, :guildid, :theme)", user_data)
					await ch.send("The levels and exp of everyone has been resetted")
				elif args[1] == "theme":
					if len(args) == 2:
						await ch.send("Change the theme of your level messages and level cards\nThemes:\nlight(default)\ndark\n \nForced theme allows you to have different theme than the server theme\nuse forced theme by ``up!theme forced dark``\nif you want forced light theme do ``up!theme forced light``")
					else:
						forced = False
						theme = "light"
						if args[2] == "forced":
							forced = True
						if "dark" in args:
							theme = "dark"
						if forced:
							theme = f"forced {theme}"
						c.execute("UPDATE guild SET theme = :theme WHERE guildid = :guildid", {"theme": theme, "guildid": guild.id})
						conn.commit()
						await ch.send("Server theme has updated successfully. GG")
				elif args[1] == "dm":
					if len(args) == 2:
						await ch.send("If you wanna the bot to dm users level up message say ``up!server dm yes``\nElse say ``up!server dm no``")
					else:
						if args[2] in ("yup","yes","y","ya","ye","yeah","on"):
							dm = 1
						elif args[2] in ("no","nah","nope","off","n"):
							dm = 0
						if dm == 0:
							answer = "off"
						elif dm == 1:
							answer = "on"
						c.execute("UPDATE guild SET dm = :dm WHERE guildid = :guildid", {"dm": dm, "guildid": guild.id})
						conn.commit()
						await ch.send(f"DM setting of the bot has been turned {answer}")
				elif args[1] == "channel":
					if len(args) == 2:
						await ch.send("To make bot to send level up messages to a particular channel\ndo: ``ch!server channel #general``\nif you wanna bring this to the default then say ``up!server channel none``")
					else:
						chid = 0
						works = False
						if args[2] not in ("nil","none"):
							chid = int(args[2][3:-1])
						if chid == 0:
							c.execute("UPDATE guild SET lvlchid = :ch WHERE guildid = :guildid", {"ch": ch, "guildid": guild.id})
							conn.commit()
							works = True
						else:
							try:
								await guild.get_channel(chid)
								c.execute("UPDATE guild SET lvlchid = :ch WHERE guildid = :guildid", {"ch": chid, "guildid": guild.id})
								conn.commit()
								works = True
							except:
								await ch.send("ping a proper channel(must be a channel in this server and must be a text channel")
						if works:
							await ch.send("Level message channel set\nNote: this wont work if you haven't turned off dm setting of the bot")

def setup(bot):
	bot.add_cog(Server(bot))