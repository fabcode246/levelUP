elif args[0] == "update":
	c.execute("""CREATE TABLE users (
	          usertag text,
			  userid integer,
			  level integer,
			  exp integer,
			  guildid integer,
			  theme text,
			  cd integer)""")
	conn.commit()
	c.execute("SELECT * FROM user")
	all_users = c.fetchall()
	for i in all_users:
		user = {
		"usertag": i[0],
		"userid": i[1],
		"level": i[2],
		"exp": i[3],
		"guildid": i[4],
		"theme": i[5],
		"cd": 0
		}
		c.execute("DELETE FROM user WHERE userid = :userid", {"userid": i[1]})
		conn.commit()
		c.execute("INSERT INTO users VALUES (:usertag, :userid, :level, :exp, :guildid, :theme, :cd)", user)
		conn.commit()
	c.execute("DROP TABLE user")
	conn.commit()
	c.execute("""CREATE TABLE user (
	          usertag text,
			  userid integer,
			  level integer,
			  exp integer,
			  guildid integer,
			  theme text,
			  cd integer)""")
	c.execute("SELECT * FROM users")
	all_users = c.fetchall()
	for i in all_users:
		user = {
		"usertag": i[0],
		"userid": i[1],
		"level": i[2],
		"exp": i[3],
		"guildid": i[4],
		"theme": i[5],
		"cd": i[6]
		}
		c.execute("DELETE FROM users WHERE userid = :userid", {"userid": i[1]})
		conn.commit()
		c.execute("INSERT INTO user VALUES (:usertag, :userid, :level, :exp, :guildid, :theme, :cd)", user)
		conn.commit()
	c.execute("DROP TABLE users")
	await ch.send("Users are updated")