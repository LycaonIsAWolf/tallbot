import discord, asyncio, re, random, threading, config, math, os

client = discord.Client()

voice = None
player = None
break_loop = False
volume = 1
song_file = ""

dice_notation = re.compile(r'[0-9]+d[0-9]+((\+|\-)[0-9]+)*')
file_regex = re.compile(r'[A-z0-9]+\.[A-z0-9]+')
volume_regex = re.compile(r'[0-9]+\.*[0-9]*')
dm_notation = r'(\+|\-)+([0-9]+)+'


def roll_dice(num, die, dm):
	total = 0
	for i in range(num):
		total += random.randint(1, die)

	return (total+dm, total)

def loop_player():
	global player, song_file, break_loop, volume
	if player.is_done() and not break_loop:
		player = voice.create_ffmpeg_player('./music/{:s}'.format(song_file))
		player.volume = volume
		player.start()

	if not break_loop:
		threading.Timer(0.05, loop_player).start()


@client.event
async def on_ready():
	global voice
	print('Logged in as')
	print(client.user.name)

	await client.join_voice_channel(client.get_server(config.server_id).get_channel(config.voice_channel_id))	
	connected = client.is_voice_connected(client.get_server(config.server_id))
	print("voice connected: {}".format(connected))
	voice = list(client.voice_clients)[0]

	print('------')

@client.event
async def on_message(message):
	global player, song_file, break_loop, volume
	upper_message = message.content.upper()
	tokens = upper_message.split(" ")

	if upper_message.startswith("TALLBOT"):
		print("received message: {:s}".format(message.content))

		if len(tokens) > 1:
			if "ROLL" in upper_message:
				match = dice_notation.search(message.content)
				if match is not None:
					dice = match.group(0)
					print("found dice notation, rolling {:s}".format(dice))
					split = dice.split('d')
					num = split[0]
					die = ""
					dm = 0

					die = split[1][0]
					dm_strings = re.findall(dm_notation, split[1])
					for s in dm_strings:
						if s[0] == '+':
							dm += int(s[1])
						elif s[0] == '-':
							dm -= int(s[1])

					result = roll_dice(int(num), int(die), dm)
					max_roll = (int(die) * int(num)) + dm

					good_roll = result[0] >= math.floor(max_roll - (max_roll/10))
					bad_roll = result[0] <= math.ceil(max_roll/10)

					msg = ""

					if dm != 0:
						msg = "{} rolled **{:d}** *({:d} + {:d})* on {:s}.".format(message.author.mention, result[0], result[1], dm, dice)
					else:
						msg = "{} rolled **{:d}** on {:s}.".format(message.author.mention, result[0], dice)

					if config.emojis and bad_roll:
						msg += " " + random.choice(config.bad_emojis)
					elif config.emojis and good_roll:
						msg += " " + random.choice(config.good_emojis)

					await client.send_message(message.channel, msg)
				else:
					print("no dice notation found.")
					await client.send_message(message.channel, "No dice notation found.")
			if type(message.channel) is discord.channel.PrivateChannel and message.author.name in config.admins:
				if "PLAY" in upper_message:
					song_file = file_regex.search(message.content)

					if song_file is not None and os.path.isfile('./{}/{}'.format(config.music_dir, song_file.group(0))):
						song_file = song_file.group(0)
						if player is not None and player.is_playing():
							break_loop = True
							player.stop()

						if len(tokens) >= 3:
							loop = "LOOP" in upper_message
							await client.send_message(message.channel, "playing {:s}".format(song_file))
							player = voice.create_ffmpeg_player('./{:s}/{:s}'.format(config.music_dir, song_file))
							player.volume = volume
							player.start()

							if loop:
								break_loop = False
								threading.Timer(0.05, loop_player()).start()
					elif song_file is None:
						await client.send_message(message.channel, "No filename.")
					else:
						await client.send_message(message.channel, "File does not exist.")

				if "STOP" in upper_message and player is not None:
					break_loop = True
					player.stop()

				if "VOLUME" in upper_message and player is not None:
					match = volume_regex.search(upper_message).group(0)
					if match is not None:
						volume = float(match)
						player.volume = volume
					else:
						await client.send_message("No volume parameter.")

		print('------')

	elif upper_message == "HI TALLBOT" or upper_message == "HELLO TALLBOT" or upper_message == "HEY TALLBOT" or upper_message == "WHAT'S UP TALLBOT":
		await client.send_message(message.channel, random.choice(config.greetings))

	elif upper_message == "THANKS TALLBOT":
		await client.send_message(message.channel, "no problem my dude")


client.run(config.token)
