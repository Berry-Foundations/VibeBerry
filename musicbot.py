# Music Bot

import youtubesearchpython
import pytube
import discord
import nacl
import os
import asyncio

q = {}
pl = [[]]

async def reply(ctx, text:str):
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

	embed.add_field(
		name = 'Music Player',
		value = text
	)

	m = await ctx.channel.send(embed=embed)
	return m

def download_video(video:dict):
	try:
		yt_video = pytube.YouTube(video['link'])
		video_streams = yt_video.streams.filter(progressive=True).order_by("resolution")
		video_streams[-1].download()
	except Exception as err:
		print(err)

async def connect(ctx):
	dm_connection = ctx.channel.type == discord.ChannelType.private
	
	if dm_connection:
		await reply(ctx, 'This command is exclusive to servers only.')
	else:
		voiceState = ctx.author.voice
		if voiceState == None:
			await reply(ctx, 'Please connect to a voice/stage channel in the server.')
			return 'no continue'
		else:
			channel = voiceState.channel
			await channel.connect()
			await reply(ctx, f'Connected to <#{channel.id}>.')

async def disconnect(ctx):
	dm_connection = ctx.channel.type == discord.ChannelType.private

	if dm_connection:
		await reply(ctx, 'This command is exclusive to servers only.')
	else:
		voiceState = ctx.guild.me.voice
		if voiceState == None:
			await reply(ctx, 'Connected to no voice/stage channels.')
		else:
			channel = voiceState.channel
			voiceClient = ctx.guild.voice_client
			await voiceClient.disconnect()
			await reply(ctx, f'Disconnected from <#{channel.id}>.')
			q[ctx.guild.id] = []

async def play(ctx, command_input:str):
	dm_connection = ctx.channel.type == discord.ChannelType.private

	if dm_connection:
		await reply(ctx, 'This command is exclusive to servers only.')
	else:
		voiceState = ctx.guild.me.voice
		if voiceState == None:
			await connect(ctx)
		
		if command_input.replace(" ", "") == "":
			await reply(ctx, 'Please provide a valid input like video name or url on YouTube.')
		else:
			video = video_search(str(command_input))
			
			duration = video['duration'].split(':')
			if len(duration) > 2:
				await reply(ctx, f'Song too long. `17(min):59(sec)` is the limit.')
				return
			else:
				if int(duration[0]) > 17:
					await reply(ctx, f'Song too long. `17(min):59(sec)` is the limit.')
					return
				else:
					pass
			
			voiceClient = None
			while voiceClient == None:
				voiceClient = ctx.guild.voice_client

			while voiceClient == None:
				await asyncio.sleep(1)
			
			gid = ctx.guild.id
			if gid in q:
				pass
			else:
				q.update(
					{
						gid : []
					}
				)
			
			vbid = len(q[gid])

			if vbid > 0:
				vbid = q[gid][-1] + 1
			
			q[gid].append(vbid)
			
			m = await reply(ctx, f'Added `{video["title"]}` to queue. A song already playing.')
			np = q[gid][0]
			while not(np == vbid):
				await asyncio.sleep(1)
				while voiceClient.is_playing():
					await asyncio.sleep(1)
				np = q[gid][0]
			await m.delete()
			
			m = await reply(ctx, f'Downloading `{video["title"]}`. This may take a few seconds or minutes. Be patient.')
			
			download_video(video)

			await asyncio.sleep(2)
			
			title = ""
			for ch in video['title'].lower():
				if ch in 'abcdefghijklmnopqrstuvwxyz 1234567890':
					title += str(ch)
				else:
					title += str(' ')
			
			while not(os.path.isfile(f'{title}.mp4')):
				await asyncio.sleep(2)
				for file in os.listdir('.'):
					if file.endswith('.mp4'):
						os.rename(file, f'{title}.mp4')
			
			song = discord.FFmpegPCMAudio(f"{title}.mp4")
			voiceClient.play(song)
			await m.delete()
			__v = f"[`{video['title']}`]({video['link']})"
			m = await reply(ctx, f'Now Playing {__v}.')
			tc = 0
			tarc = (int(duration[0]) * 60) + int(duration[1])
			pcom = 0
			while tarc >= tc:
				await asyncio.sleep(1)
				__pcom = int( int( ( tc / tarc ) * 100 ) / 10 )
				if __pcom == pcom:
					pass
				else:
					__t = video["title"]
					if len(__t) > 20:
						__t = __t[:20] + "..."
					pcom = __pcom
					progress_bar = "➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖".split(' ')
					progress_bar[pcom - 1] = "🔘"
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
					vlink = video["link"] + "?t=" + str(tc - 1)
					__v = f'[`{__t}`]({vlink})'

					embed.add_field(
						name = 'Music Player',
						value = f'Now Playing {__v}\n\n{"".join(progress_bar)}'
					)
					await m.edit(embed=embed)
				if gid in pl[0]:
					pass
				else:
					tc += 1
			if len(q[gid]) > 0:
				del q[gid][0]
			os.remove(f'{title}.mp4')
			await m.delete()

async def pause(ctx):
	dm_connection = ctx.channel.type == discord.ChannelType.private

	if dm_connection:
		await reply(ctx, 'This command is exclusive to servers only.')
	else:
		voiceState = ctx.guild.me.voice
		if voiceState == None:
			await reply(ctx, 'Can not pause. Not playing any music.')
		else:
			voiceClient = ctx.guild.voice_client
			if voiceClient.is_playing():
				voiceClient.pause()
				await reply(ctx, 'Paused music.')
				pl[0].append(ctx.guild.id)
			else:
				await reply(ctx, 'Can not pause. Not playing any music.')

async def resume(ctx):
	dm_connection = ctx.channel.type == discord.ChannelType.private

	if dm_connection:
		await reply(ctx, 'This command is exclusive to servers only.')
	else:
		voiceState = ctx.guild.me.voice
		if voiceState == None:
			await reply(ctx, 'Can not resume. Not paused any music.')
		else:
			voiceClient = ctx.guild.voice_client
			if voiceClient.is_paused():
				voiceClient.resume()
				await reply(ctx, 'Resumed music.')
				pl[0].remove(ctx.guild.id)
			else:
				await reply(ctx, 'Can not resume. Not paused any music.')

async def stop(ctx):
	dm_connection = ctx.channel.type == discord.ChannelType.private

	if dm_connection:
		await reply(ctx, 'This command is exclusive to servers only.')
	else:
		voiceState = ctx.guild.me.voice
		if voiceState == None:
			await reply(ctx, 'Can not stop. Not playing any music.')
		else:
			voiceClient = ctx.guild.voice_client
			if voiceClient.is_playing():
				voiceClient.stop()
				await reply(ctx, 'Stopped music.')
				q[ctx.guild.id] = []
			else:
				await reply(ctx, 'Can not stop. Not playing any music.')

def video_search(query:str):
	video_search = youtubesearchpython.VideosSearch(str(query), limit = 1)
	video_raw_data = video_search.result()['result'][0]
	
	video_data = {}
	required_entities = [
		'title',
		'duration',
		'link'
	]
	
	for data_type in video_raw_data:
		if str(data_type) in required_entities:
			video_data.update(
				{
					str(data_type) : str(video_raw_data[data_type])
				}
			)
	
	return video_data

async def skip(ctx):
	gid = ctx.guild.id
	if len(q[gid]) > 0:
		del q[gid][0]
		voiceClient = ctx.guild.voice_client
		if voiceClient.is_playing():
			voiceClient.pause()
			await reply(ctx, "Skipped.")
		else:
			await reply(ctx, "Failed to skip.")
	else:
		await reply(ctx, "Failed to skip.")

async def volume(ctx, command_input:str):
	vs = ctx.guild.me.voice
	if vs == None:
		await reply(ctx, 'Not connected to any channel.')
	else:
		vc = ctx.guild.voice_client
		if vc.is_playing():
			try:
				vol = float((int(command_input.split(' ')[0]) % 100) / 100)
				audio = vc.source
				vc.source = discord.PCMVolumeTransformer(audio)
				vc.source.volume = 2.0
				vc.source.volume = vol
				await reply(ctx, f'Volume set to {vol*100}%')
			except:
				await reply(ctx, 'Volume not in number format.')
		else:
			await reply(ctx, 'Not playing anything.')

async def trigger(ctx, command:str, command_input:str):
	if command == "connect":
		await connect(ctx)
	elif command == "disconnect":
		await disconnect(ctx)
	elif command == "play":
		await play(ctx, command_input)
	elif command == "skip":
		await skip(ctx)
	elif command == "pause":
		await pause(ctx)
	elif command == "resume":
		await resume(ctx)
	elif command == "stop":
		await stop(ctx)

