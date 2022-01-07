# VibeBerry

import os
import musicbot
import server

import discord

bot = discord.Client()

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Music!"))
	await bot.change_presence(status=discord.Status.online)
	print(f'{bot.user.name} has started.')

@bot.event
async def on_message(ctx):
	message = ctx.content
	msg = message.split(" ")
	prefix = [
		"music",
		"vibe",
		"vibeberry",
		"vb"
	]

	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Music!"))

	if len(msg) < 2:
		return

	if msg[0].lower() in prefix:
		del msg[0]
		cmd = (str(msg[0]) + '').lower()

		cmd_input = ""
		if len(msg) > 1:
			del msg[0]
			cmd_input = " ".join(msg)

		await musicbot.trigger(ctx, cmd, cmd_input)

		if cmd == "help":
			embed = discord.Embed(
				title = "VibeBerry",
				color = 0x05cfde,
				description = "VibeBerry is a music bot."
			)
			
			embed.set_thumbnail(
				url='https://images-ext-2.discordapp.net/external/B3fan6_20nbG7ZQRdpRYKxTJcOQrASTBj75hN97IgUE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/895121185065562184/9e3b25a9f265d9c4de656df3aeffd5d5.webp'
			)
			
			embed.set_footer(
				text = "Services under Berry Foundations - Attachment Studios",
				icon_url = "https://images-ext-1.discordapp.net/external/x_dF_ppBthHmRPQi75iuRXLMfK0wuAW2sBLTdtNlXAc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/894098855220617216/d9b9a3b48a054b9847401bb9178ed438.webp"
			)

			hf = open('help.md', 'r')
			hd = hf.read()
			hf.close()
			
			bf = open('bug.md', 'r')
			bd = bf.read()
			bf.close()
			
			embed.add_field(
				name = "Help",
				value = str(hd),
				inline = False
			)

			await ctx.channel.send(embed = embed)

@bot.event
async def on_raw_reaction_add(payload):
	await musicbot.add_reaction_trigger(payload, bot)

@bot.event
async def on_raw_reaction_remove(payload):
	await musicbot.remove_reaction_trigger(payload, bot)

token = os.getenv('TOKEN')
try:
	server.super_run()
	bot.run(token)
except Exception as e:
	print(f"{e}")

