**Tallbot** is a bot for [discord](https://discordapp.com/) that handles dice rolling and music playing over voice chat. Made with [discord.py](https://github.com/Rapptz/discord.py). Requires Python 3.

To use simply fill example_config.py with the relevant information, rename it to "config.py", and run tallbot.py.

All commands start with "tallbot".

## Public Commands
These commands will be read from any channel on any server tallbot is on, and in DMs. 

###`roll [num]d[sides]+-[modifier]`
Rolls dice notation of the form AdB+-C, where A is the number of dice, B is the number of sides on the dice, and C is the optional modifier. Example: `tallbot roll 3d6+3`

##Private Commands
These commands can only be run through DMs with tallbot by users specified in the `admins` variable of config.py.

###`play [file] [loop]`
Plays [file] from `music_dir` specified in config.py. Examples: `tallbot play mantis_battle.mp3 loop` to loop or `tallbot play dogsong.mp3` to play once.

###`volume [volume]`
Sets tallbot's playback volume to [volume], where 1 is 100% volume, 0.5 is 50% volume, etc. Example: `tallbot volume 0.5`.

###`stop`
Stops playback from tallbot immediately.