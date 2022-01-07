# Music Bot

import youtubesearchpython
import pytube
import discord
import nacl
import os
import asyncio
import random

q = {}
pl = [[]]

async def reply(ctx, text:str, *image:bool):
	embed = discord.Embed(
		title = "VibeBerry",
		color = 0x05cfde,
		description = "VibeBerry is a music bot."
	)
	embed.set_thumbnail(
		url='https://images-ext-2.discordapp.net/external/B3fan6_20nbG7ZQRdpRYKxTJcOQrASTBj75hN97IgUE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/895121185065562184/9e3b25a9f265d9c4de656df3aeffd5d5.webp'
	)

	embed.add_field(
		name = 'Music Player',
		value = text
	)

	if image:
		embed.set_image(
			url = f"https://github.com/Attachment-Studios/VibeBerry/blob/master/player/{[1, 2, 3, 4][random.randint(0, 3)]}.gif?raw=true"
		)
	
	embed.set_footer(
		text = "Services under Berry Foundations - Attachment Studios",
		icon_url = "https://images-ext-1.discordapp.net/external/x_dF_ppBthHmRPQi75iuRXLMfK0wuAW2sBLTdtNlXAc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/894098855220617216/d9b9a3b48a054b9847401bb9178ed438.webp"
	)
	
	m = await ctx.channel.send(embed=embed)
	return m

async def download_video(ctx, video:dict):
	try:
		yt_video = pytube.YouTube(video['link'])
		video_streams = yt_video.streams.filter(progressive=True).order_by("resolution")
		video_streams[-1].download()
		return None
	except:
		return "FAIL"

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

			try:
				await ctx.delete()
			except:
				pass

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

			try:
				await ctx.delete()
			except:
				pass

async def play(ctx, command_input:str, repeat:bool):
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

			try:
				await ctx.delete()
			except:
				pass
			
			np = q[gid][0]
			while not(np == vbid):
				await asyncio.sleep(1)
				if len(q[gid]) == 0:
					try:
						await m.delete()
					except:
						pass
					return
				while voiceClient.is_playing():
					await asyncio.sleep(1)
				if len(q[gid]) == 0:
					try:
						await m.delete()
					except:
						pass
					return
				np = q[gid][0]
			await m.delete()
			
			m = await reply(ctx, f'Downloading `{video["title"]}`. This may take a few seconds or minutes. Be patient.')
			
			d____ = await download_video(ctx, video)
			if d____ == None:
				pass
			else:
				try:
					if len(q[gid]) > 0:
						del q[gid][0]
				except:
					pass
				try:
					await m.delete()
				except:
					pass
				await reply(ctx, f'Failed to download `{video["title"]}`.')

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
			
			if repeat == False:
				song = discord.FFmpegPCMAudio(f"{title}.mp4")
				voiceClient.play(song)
			
			try:
				await m.delete()
			except:
				pass
			
			loop = True

			__v = f"[`{video['title']}`]({video['link']})"
			if repeat:
				m = await reply(ctx, f'Now Looping {__v}.', True)
			else:
				m = await reply(ctx, f'Now Playing {__v}.', True)
			
			await m.add_reaction('⏸️')
			await m.add_reaction('⏭️')
			await m.add_reaction('⏹️')
			await m.add_reaction('🔁')
			
			player_img = f"https://github.com/Attachment-Studios/VibeBerry/blob/master/player/{[1, 2, 3, 4][random.randint(0, 3)]}.gif?raw=true"
			while loop:
				try:
					if repeat:
						if voiceClient.is_playing():
							voiceClient.stop()
						song = discord.FFmpegPCMAudio(f"{title}.mp4")
						voiceClient.play(song)
					if repeat == False:
						loop = False
					tc = 0
					tarc = (int(duration[0]) * 60) + int(duration[1])
					pcom = 0
					broken = False
					while tarc >= tc:
						await asyncio.sleep(1)
						__pcom = int( int( ( tc / tarc ) * 100 ) / 10 )
						try:
							if q[gid][0] == vbid:
								pass
							else:
								broken = True
								loop = False
								break
						except:
							broken = True
							break
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
							embed.set_image(
								url = player_img
							)
							if loop == False:
								await m.edit(embed=embed)
						if gid in pl[0]:
							pass
						else:
							tc += 1
					if broken:
						break
				except:
					break
			try:
				if len(q[gid]) > 0:
					if broken == False:
						del q[gid][0]
			except:
				pass
			try:
				os.remove(f'{title}.mp4')
			except:
				pass
			try:
				await m.delete()
			except:
				pass

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
				m = await reply(ctx, 'Paused music.')
				pl[0].append(ctx.guild.id)

				try:
					await ctx.delete()
				except:
					pass
				
				try:
					await asyncio.sleep(10)
					await m.delete()
				except:
					pass
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
				m = await reply(ctx, 'Resumed music.')
				pl[0].remove(ctx.guild.id)

				try:
					await ctx.delete()
				except:
					pass

				try:
					await asyncio.sleep(10)
					await m.delete()
				except:
					pass
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

				try:
					await ctx.delete()
				except:
					pass
			else:
				await reply(ctx, 'Can not stop. Not playing any music.')

def video_search(query:str):
	try:
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
	except Exception as e:
		print(e)
		video_search = youtubesearchpython.VideosSearch("Rickroll", limit = 1)
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
			m = await reply(ctx, "Skipped.")

			try:
				await ctx.delete()
			except:
				pass
			
			try:
				await asyncio.sleep(10)
				await m.delete()
			except:
				pass
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
				m = await reply(ctx, f'Volume set to {vol*100}%')
				
				try:
					await ctx.delete()
				except:
					pass
				
				try:
					await asyncio.sleep(10)
					await m.delete()
				except:
					pass
			except:
				await reply(ctx, 'Volume not in number format.')
		else:
			await reply(ctx, 'Not playing anything.')

async def galaxy(ctx, command_input:str):
	if command_input.strip(' ') == "":
		if os.path.isfile(f'playlists/{ctx.author.id}.csv'):
			pass
		else:
			m = await reply(ctx, f'[`{ctx.author.name}\'s Galaxy`](https://discord.com/users/{ctx.author.id}) is empty.')
			try:
				await ctx.delete()
			except:
				pass
			await asyncio.sleep(15)
			try:
				await m.delete()
			except:
				pass
	else:
		pass

async def trigger(ctx, command:str, command_input:str):
	if command == "connect":
		await connect(ctx)
	elif command == "disconnect":
		await disconnect(ctx)
	elif command == "play":
		await play(ctx, command_input, False)
	elif command == "loop":
		await play(ctx, command_input, True)
	elif command == "galaxy":
		await galaxy(ctx, command_input)
	elif command == "skip":
		await skip(ctx)
	elif command == "pause":
		await pause(ctx)
	elif command == "resume":
		await resume(ctx)
	elif command == "stop":
		await stop(ctx)

async def add_reaction_trigger(payload, client):
	user = payload.member
	if user == None:
		user = await client.fetch_user(payload.user_id)
	emoji = payload.emoji.name
	channel = await client.fetch_channel(payload.channel_id)

	if user.bot:
		return
	
	pause = '⏸️'
	skip = '⏭️'
	stop = '⏹️'
	loop = '🔁'
	
	if emoji == pause:
		await channel.send('vibe pause')
	if emoji == skip:
		await channel.send('vibe skip')
	if emoji == stop:
		await channel.send('vibe stop')
	if emoji == loop:
		message = await channel.fetch_message(payload.message_id)
		embed = message.embeds[0]
		for field in embed.fields:
			if field.name == "Music Player":
				url = field.value.split('](')[-1].split(')')[0].split('?t=')[0]
				await channel.send(f'vibe loop {url}')

async def remove_reaction_trigger(payload, client):
	user = payload.member
	if user == None:
		user = await client.fetch_user(payload.user_id)
	emoji = payload.emoji.name
	channel = await client.fetch_channel(payload.channel_id)

	if user.bot:
		return
	
	pause = '⏸️'
	
	if emoji == pause:
		await channel.send('vibe resume')

