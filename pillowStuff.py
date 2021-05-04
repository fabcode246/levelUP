from PIL import Image, ImageDraw, ImageFont
import io
import sqlite3

filename = "C:\\Users\\JERSON\\Videos\\FabCode resources\\FabTech Logo.png"

def level_up(name, level, theme):
	newImage = Image.new(mode="RGB", size=(350,100), color=theme["bg"])
	draw = ImageDraw.Draw(newImage)
	head_font = ImageFont.truetype("framd.ttf",40)
	child_font = ImageFont.truetype("framd.ttf",25)
	lvl_text = f"Level: {level-1} → {level}"
	draw.text((15, 10), name, font=head_font, fill=theme["textcolor"])
	draw.text((20, 60), lvl_text, font=child_font, fill=theme["textcolor"])
	byte = io.BytesIO()
	newImage.save(byte, format="PNG")
	return byte


def	lvl_info(name, level, exp, rank, theme):
	newImage = Image.new(mode="RGB", size=(400,150), color=theme["bordercolor"])
	draw = ImageDraw.Draw(newImage)
	draw.rectangle((5,5,395,145),fill=theme["bg"])
	head_font = ImageFont.truetype("framd.ttf",40)
	child_font = ImageFont.truetype("framd.ttf",25)
	exp_font = ImageFont.truetype("framd.ttf",20)
	lvl_text = f"Rank: {rank} | Level: {level}"
	draw.text((10, 10), name, font=head_font, fill=theme["textcolor"])
	draw.text((15, 55), lvl_text, font=child_font, fill=theme["textcolor"])
	exp_max = (level+1) * 50
	exp_percentage = (exp/exp_max)*100
	exp_text = f"Exp: {exp}/{exp_max}"
	draw.text((15, 80), exp_text, font=exp_font, fill=theme["textcolor"])
	draw.rectangle((15,110,215,130),fill=theme["textcolor"])
	x_progress_bar = exp_percentage*2+10
	if exp_percentage != 0:
		draw.rectangle((20,115,x_progress_bar,125),fill=theme["progresscolor"])
	byte = io.BytesIO()
	newImage.save(byte, format="PNG")
	return byte

def themer(user_th, guild_th):
	datafile = "dat.db"
	theme = ""
	user_theme = user_th.split(" ")
	guild_theme = guild_th.split(" ")
	user_power = 1
	guild_power = 0
	if "forced" in user_theme:
		user_power = 3
	if "forced" in guild_theme:
		guild_power = 2
	if guild_power > user_power:
		theme_name = guild_theme[-1]
	if user_power > guild_power:
		theme_name = user_theme[-1]
	conn = sqlite3.connect(datafile)
	c = conn.cursor()
	c.execute("SELECT * FROM theme WHERE name = :name",{"name": theme_name})
	fetched_theme = c.fetchall()
	theme = {
		"bg": fetched_theme[0][1].split("-"),
		"textcolor": fetched_theme[0][2].split("-"),
		"progresscolor": fetched_theme[0][3].split("-"),
		"bordercolor": fetched_theme[0][4].split("-"),
	}
	for colors in theme:
		num = 0
		for c in theme[colors]:
			theme[colors][num] = int(theme[colors][num])
			num += 1
	for color in theme:
		theme[color] = tuple(theme[color])
	return theme
