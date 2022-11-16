#######################################################################################################################################################
#Filename: tft.py                                                                                                                                     #
#Author(s): Jared De Los Santos                                                                                                                       #
#Date Last Updated: 11/15/22                                                                                                                          #
#Purpose of File: Practice with Riot API to get average placements in the last 30 matches                                                             #
#######################################################################################################################################################

import discord
from discord.ext import commands
from discord import File
import matplotlib.pyplot as plt
import numpy as np
import requests
import time
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
api_key = os.getenv('RIOT_TOKEN')

class TFT(commands.Cog, name = "Teamfight Tactics"):
    """Get a bar chart of your average placements in the recent matches."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def placements(self, ctx, *, name):
        """Takes your last 30 matches and puts your placement in a chart."""
        summoner_name = name

        try:
            player_dict = self.get_puuid_by_summoner_name(name)
            puuid = player_dict.get('puuid')

            embed = discord.Embed(title = f"Pulling matches for {summoner_name}.",
                                description = "Please hold... This can take between 1-5 minutes.",
                                color = 0xA020F0)

            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(title = f"ERROR",
                                description = f"Could not find {summoner_name}",
                                color = 0xFF0000)
            await ctx.send(embed=embed)
        
        matches_list = self.get_matches_by_puuid(puuid)

        placement = {}
        for match_ids in matches_list:
            match_stats_dict = self.get_match_by_match_id(match_ids)
            match_stats_info_dict = match_stats_dict['info']
            match_info_participants_list = match_stats_info_dict['participants']

            for i in match_info_participants_list:
                if i['puuid'] == puuid:
                    if (i['placement'] in placement):
                        placement[i['placement']] += 1
                    else:
                        placement[i['placement']] = 1

        placement_lists = sorted(placement.items())

        x, y = zip(*placement_lists)

        image = File("placement.png")
        placement_colors = ['#FFD700', '#C0C0C0', '#CD7F32', 'blue', '#000000', '#000000', '#000000', '#000000']
        plt.bar(x, y, color = placement_colors, width = 0.4)
        plt.xlabel('Placements')
        plt.ylabel('# of times placed')
        plt.title(f'Average placements for {name}')

        plt.savefig('placement.png')
        plt.close()

        embed = discord.Embed(title = "Average placements in the last 30 matches", color = 0xA020F0)
        await ctx.send(embed = embed)
        await ctx.send(file=image)

    #only set to work for NA1
    def get_puuid_by_summoner_name(self, summoner_name):

        api_url = f"https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{self.format_for_url(summoner_name)}?api_key={api_key}"

        #debug
        # print(api_url)

        #rate limit check
        while True:
            resp = requests.get(api_url)
            status_code = resp.status_code
            print("Status Code:", status_code)
            if status_code == 429:
                print("Rate Limit hit, stopping")
                break
            player_info = resp.json()
            return player_info

    #summoner name to be changed for the url in case there are spaces
    def format_for_url(self, summoner_name):
        formatted_summ_name = summoner_name.replace(" ", '%20')
        return formatted_summ_name

    def get_matches_by_puuid(self, puuid):
        api_url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=30&api_key={api_key}"

        #debug
        # print(api_url)

        #rate limit check
        while True:
            resp = requests.get(api_url)
            status_code = resp.status_code
            print("Status Code:", status_code)
            if status_code == 429:
                print("Rate Limit hit, stopping")
                break
            player_info = resp.json()
            return player_info

    def get_match_by_match_id(self, match_id):
        api_url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}"

        #debug
        # print(api_url)

        #rate limit check
        while True:
            resp = requests.get(api_url)
            status_code = resp.status_code
            print("Status Code:", status_code)
            if status_code == 429:
                print("Rate Limit hit, stopping")
                break
            player_info = resp.json()
            return player_info

"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(TFT(bot))
