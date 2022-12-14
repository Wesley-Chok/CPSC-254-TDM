# Project part 2 for 254!
# TDM: A Discord Bot made with discord.py

A project made through CPSC 254. Focused on using Python, along with the discord.py library to create a bot for Discord.

#### Members
- Javier Perez
- Vincent Nguyen

## Requirements:
- You need to be using Windows.
- You need a Discord account. https://discord.com/ 
- You need a Riot Games Developer account. https://developer.riotgames.com/ 
- An IDE where you can set up an environment for Python. (preferably Visual Studio Code, unless you know how to set it up)
- Python 3.9/3.10; either is fine
- You need to install ffmpeg and add it to your PATH Environment Variable. https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z **Clarified at Step 5**

## Instructions:
#### Steps in order to run project locally:



Steps in order to be able to run our project locally:
1. Follow this link to gain your own token for a bot: https://www.writebots.com/discord-bot-token/ 
   - If any issues arise with obtaining the token; just reset it no problem.
   - Make sure to save the token somewhere safe.
2. Head to this link to create a developer account for Riot Games: https://developer.riotgames.com/ 
   - Copy the development API key on the main page.
   - Make sure to save the token somewhere safe.
3. Clone our repository for the Discord bot. Within the files, there is one specific file provided called “.env”. This is where we will store our tokens. 
   - Under TOKEN, you want to fill in the empty space with the Discord token we pulled from step 1, and under RIOT_TOKEN, we are filling it with the Riot API key we pulled from step 2.
   - Note: no quotations needed.
4. Type this in your environment console or command prompt or wherever you placed the directory for the bot.
```bash
pip install -r requirements.txt
```
or 
```bash
python -m pip install -r requirements.txt
```
**If neither work, you might have to research how to `pip install` yourself.**

5. ffmpeg requires you to do a couple of things; as it is essential for our music feature.
Once you have downloaded the ffmpeg from the requirements at the top, extract it anywhere you’d like as long as you remember the location. It is preferable that you just store it in your C:\ drive. So your folder could look like: `C:\ffmpeg`. 
   - When originally extracting, you can rename the `ffmpeg{lots of numbers}` to just `ffmpeg`.
   - Add `C:\ffmpeg\bin` to your Path environment variables 
     - Or wherever the bin folder is withing your ffmpeg folder.



6. Restart your IDE and environment, double check to make sure all the packages and libraries are there from requirements.txt. 
`pip list`

7. Head to the Discord application and create a server, so that you can invite the bot to this server. It is recommended you have a sub-account or a friend in the same server so that you can test out the moderation features.

8. Head back to the Discord Developer Portal page and select the application you created earlier at Step 1.

9. Head to URL Generator and select `bot` under `SCOPES` and `Administrator` under `BOT PERMISSIONS`:

10. Scroll down and click on the generated URL and select your newly created server so that the bot can join.

11. Head back to your IDE and then run the main.py file and you have finally activated the bot; assuming that everything was done correctly.
    - Our bot's prefix is “.” so every command starts with that. To get started with the commands please type “.help”. 
      - If you need more assistance with a command, please type “.help [command]”.
