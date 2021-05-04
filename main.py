import discord
from discord.ext import commands
import sqlite3
import json
from random import randint
from pillowStuff import level_up, lvl_info, themer
import io
import os
from asyncio import sleep

with open("tok.json", "r")as file:
	junk = json.load(file)

datafile = "dat.db"

invite_link = "https://discord.com/api/oauth2/authorize?client_id=815209232898064414&permissions=268520449&scope=bot"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='up!', intents=intents)

@bot.event
async def on_ready():
	print("bot is ready")

@bot.event
async def on_message(message):
	guild = message.guild
	author = message.author
	ch = message.channel
	conn = sqlite3.connect(datafile)
	c = conn.cursor()
	c.execute("SELECT userid FROM admin WHERE data = 1")
	data_admins = c.fetchall()
	c.execute("SELECT userid FROM admin")
	admins = c.fetchall()
	c.execute(f"SELECT * FROM guild WHERE guildid = :guildid", {"guildid": message.guild.id})
	fetched_server = c.fetchall()
	if message.content[:3] == "up!":
		args = message.content[3:].split(" ")
		if args[0] in ("setup", "set") and len(args) == 3:
			role_id = int(args[1][3:-1])
			role = guild.get_role(role_id)
			lvl = args[2]
			role_data = {
				"rolename": role.name,
				"roleid": role.id,
				"guildid": guild.id,
				"level": lvl
			}
			c.execute("INSERT INTO role VALUES (:rolename, :roleid, :guildid, :level)", role_data)
			await ch.send(f"Added {role.name} role as level {lvl} reward")
		elif args[0] in ("register","reg") and len(fetched_server) == 0:
			guild_data = {
				"guildid": guild.id,
				"lvlchid": 0,
				"theme": "light",
				"dm": 1
			}
			c.execute("INSERT INTO guild VALUES (:guildid, :lvlchid, :theme, :dm)", guild_data)
			await ch.send("Your Server has been registered. The bot will start working from now on")
		elif args[0] in ("invite", "inv"):
			await ch.send(embed=discord.Embed(
				title="Add levelUP to your Server",
				description=f"[Invite Link]({invite_link})"))
		elif args[0] in ("ignore-channel", "ignore-ch") and author.guild_permissions.administrator == True:
			if len(args) == 1:
				await ch.send("Add a channel to the ignore list so users cant gain exp by chatting on those channels")
			else:
				if args[1] == "add":
					channel_id = int(args[2][2:-1])
					try:
						channel = guild.get_channel(channel_id)
						await ch.send(f"Added {channel.mention} to ignore list")
						c.execute("INSERT INTO channel VALUES (:chid, :guildid)", {"chid": channel_id, "guildid": guild.id})
					except Exception as e:
						await ch.send("Channel doesn't exist\nPlease mention an existing channel when using the command")
				elif args[1] == "remove":
					channel_id = int(args[2][2:-1])
					c.execute("DELETE FROM channel WHERE channelid = :chid", {"chid": channel_id})
					await ch.send("Removed channel from ignore list")
		elif args[0] in ("theme", "thm", "t"):
			if len(args) == 1:
				await ch.send("Change the theme of your level messages and level cards\nThemes:\nlight(default)\ndark\n \nForced theme allows you to have different theme than the server theme\nuse forced theme by ``up!theme forced dark``\nif you want forced light theme do ``up!theme forced light``")
			else:
				forced = False
				theme = "light"
				if args[1] == "forced":
					forced = True
				if "dark" in args:
					theme = "dark"
				if forced:
					theme = f"forced {theme}"
				c.execute("UPDATE user SET theme = :theme WHERE guildid = :guildid AND userid = :userid", {"theme": theme, "guildid": guild.id, "userid": author.id})
				await ch.send("Your theme has been successfully updated :)")
		elif args[0] == "searchbytag" and author.id in data_admins:
			c.execute("SELECT * FROM user WHERE usertag = :usertag", {"usertag": args[1]})
			fetched_user = c.fetchall()
			if len(fetched_user) == 0:
				await ch.send("User not found")
			else:
				if len(args) == 2:
					color = discord.Colour.from_rgb(154,223,176)
					embed = discord.Embed(title=f"{fetched_user[0][0][:-5]}'s Profile")
					embed.add_field(name="UserTag", value=fetched_user[0][0], inline=False)
					embed.add_field(name="UserID", value=fetched_user[0][1], inline=False)
					embed.add_field(name=f"Servers", value=len(fetched_user), inline=False)
					await ch.send(embed=embed)
				elif args[2] in ("invite","inv"):
					if len(args) == 3:
						inv = 0
					else:
						inv = int(args[3])-1
					server = bot.get_guild(fetched_user[inv][4])
					channel = server.text_channels[0]
					invite = await channel.create_invite(unique=False)
					await ch.send(content=f"Invite: {invite.url}")
				elif args[2] in ("srvr", "server"):
					string = ""
					for s in fetched_user:
						server = bot.get_guild(s[4])
						string = f"{server.name}({server.id})\n"
					color = discord.Colour.from_rgb(154,223,176)
					await ch.send(embed=discord.Embed(
						title=f"{fetched_user[0][0][:-5]}'s Servers",
						description=string,
						color=color))
		elif args[0] == "add-theme" and author.id in admins:
			if len(args) == 1:
				await ch.send("Format: ``up!add-theme name bg tc pc bc``\nbg - background color\ntc - text color\npc - progress bar color\nbc - border color\neach color should be like ``r-g-b``")
			else:
				name = args[1]
				bg = args[2]
				tc = args[3]
				pc = args[4]
				bc = args[5]
				theme = {
					"name": name,
					"bg": bg,
					"tc": tc,
					"pc": pc,
					"bc": bc
				}
				c.execute("INSERT INTO theme VALUES (:name, :bg, :tc, :pc, :bc)", theme)
				await ch.send(f"Theme {name} has been saved\nbg = {bg}\ntc = {tc}\npc = {pc}\nbc = {bc}")
		elif args[0] == "add-admin" and author.id == 678484214311682130:
			if len(args) == 2:
				access = 0
			elif args[2] in ("data", "access", "data-perm", "data-access"):
				access = 1
			c.execute("INSERT INTO admin VALUES (:userid, :data)", {"userid": int(args[1]), "data": access})
			await ch.send("Added admin")
		elif args[0] == "remove-admin" and author.id == 678484214311682130:
			c.execute("DELETE FROM admin WHERE userid = :userid", {"userid": int(args[1])})
			await ch.send("Removed admin")
		conn.commit()
		conn.close()
	elif not author.bot and len(fetched_server) != 0:
		conn = sqlite3.connect(datafile)
		c = conn.cursor()
		c.execute("SELECT * FROM user WHERE guildid = :guildid AND userid = :userid", {"guildid": guild.id, "userid": author.id})
		fetched_result = c.fetchall()
		if len(fetched_result) != 0:
			c.execute("SELECT * FROM channel WHERE guildid = :guildid", {"guildid": guild.id})
			fetched_channels = c.fetchall()
			flag = True
			for channel in fetched_channels:
				if channel[0] == ch.id:
					flag = False
					break
			if flag and fetched_result[0][6] == 0:
				exp = randint(3, 9)
				exp += fetched_result[0][3]
				lvl = fetched_result[0][2]
				if exp >= (lvl+1)*50:
					lvl += 1
					theme = themer(fetched_result[0][5], fetched_server[0][2])
					image = level_up(author.name, lvl, theme)
					image.seek(0)
					if fetched_server[0][3] == 1:
						await author.send(file=discord.File(fp=image ,filename="level_up.png"))
					else:
						if fetched_server[0][1] == 0:
							await ch.send(author.mention)
							await ch.send(file=discord.File(fp=image ,filename="level_up.png"))
						else:
							channel = guild.get_channel(fetched_server[0][1])
							await channel.send(author.mention)
							await channel.send(file=discord.File(fp=image ,filename="level_up.png"))
					c.execute("SELECT * FROM role WHERE guildid = :guildid", {"guildid": guild.id})
					fetched_roles = c.fetchall()
					if len(fetched_roles) != 0:
						for r in fetched_roles:
							if lvl == r[3]:
								role = guild.get_role(r[1])
								await author.add_roles(role)
								await author.send(f"You got {r[0]} role from {guild.name} server")
				user_data = {
					"usertag": fetched_result[0][0],
					"userid": fetched_result[0][1],
					"level": lvl,
					"exp": exp,
					"guildid": fetched_result[0][4],
					"theme": fetched_result[0][5],
					"cd": 1
				}
				c.execute("DELETE FROM user WHERE guildid = :guildid AND userid = :userid", {"guildid": guild.id, "userid": author.id})
				conn.commit()
				c.execute("INSERT INTO user VALUES (:usertag, :userid, :level, :exp, :guildid, :theme, :cd)", user_data)
				conn.commit()
				await sleep(10)
				c.execute("UPDATE user SET cd = 0 WHERE guildid = :guildid AND userid = :userid", {"guildid": guild.id, "userid": author.id})
				conn.commit()
		else:
			user_data = {
				"usertag": str(author),
				"userid": author.id,
				"level": 0,
				"exp": 0,
				"guildid": guild.id,
				"theme": "light",
				"cd": 0
			}
			c.execute("INSERT INTO user VALUES (:usertag, :userid, :level, :exp, :guildid, :theme, :cd)", user_data)
			conn.commit()
		conn.close()

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(junk[0])