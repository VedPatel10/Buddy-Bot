# Buddy-Bot
Discord bot that I made on Replit which can be used as a music player and sports stats know-it-all. The bot stays online by using a Flask server and randomly pinging itself. All commands are detected when users type "!" + command_name in a Discord server. 

## Music

__!join & !leave__ - make bot join and leave voice channel

__!play + YouTube URL__ - starts playing the video's audio in voice channel. Bot joins user's voice channel if it is not in one already 

__!pause & !resume__ - pause and resume the bot from playing audio

__!skip__ - skip current video that the bot is playing

__!search + video name__ - search YouTube for options depending on what you search

![image](https://user-images.githubusercontent.com/86941088/188288574-98667565-4955-4f5a-8df3-c3daa5d87764.png)

__!#__ - used to select a video from the search to play 

## Sports
Currently, the bot can scrape stats for current and former Nba, Nhl, and Mlb players of all positions thanks to https://www.sports-reference.com/.

__!league + player name + year (optional)__ - returns player stats neatly formatted. If no year is provided, career stats are used.

![image](https://user-images.githubusercontent.com/86941088/188287810-ee1b9d5b-f7ad-4a8a-84da-4875f48a0edf.png)

![image](https://user-images.githubusercontent.com/86941088/188288590-df5cce2d-7598-401e-8cf3-ab82f17395c3.png)

![image](https://user-images.githubusercontent.com/86941088/188288564-84bfddd6-d4ef-4613-a161-3acae869bfe7.png)
