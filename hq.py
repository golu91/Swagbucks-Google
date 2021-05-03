import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
#import Google_Search
import time
from datetime import datetime
from pytz import timezone
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import re
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed
import aniso8601
import aiohttp
import asyncio

webhook_url="https://discordapp.com/api/webhooks/838837824614432849/Na_4Sl4PAbGQppbloqyrt6VfkkBIY2gkdttiy9Purd_1NNOmrKjc_PM-nprXm-yJLDmB"

try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")
                    
def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
        print(response_data)
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%d/%m/%Y")
            x_inn = x_ind.strftime("%H:%M")
    
            prize = (response_data["nextShowPrize"])
            time.sleep(5)
            print(x_in)
            print(prize)
            embed=discord.Embed(title="Game is not Live", color=0x00ffff)
            hook.send(embed=embed)



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
            if message_data['type'] != 'interaction':
                print(message_data)
        
            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']
                embed=discord.Embed(title=f"Question {qcnt} out of {Fullcnt}", description=question, color=0x00ffff)
                hook.send(embed=embed)
                id1 = message_data["answers"][0]["answerId"]
                id2 = message_data["answers"][1]["answerId"]
                id3 = message_data["answers"][2]["answerId"]

            elif message_data['type'] == 'answered':
                name = message_data["username"]
                ansid = message_data["answerId"]
                if ansid == id1:
                    embed = discord.Embed(title=f"{name} went Option - 1", color=0x00ff00)
                    hook.send(embed=embed)
                elif ansid == id2:
                    embed = discord.Embed(title=f"{name} went Option - 2", color=0x00ff00)
                    hook.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"{name} went Option - 3", color=0x00ff00)
                    hook.send(embed=embed)
                

            elif message_data["type"] == "questionClosed":
                embed=discord.Embed(title="⏰ **| Time,s Up!**", color=0xa1fc03)
                hook.send(embed=embed)

"""
def open_browser(question):

    main_url = "https://www.google.co.in/search?q=" + question
    webbrowser.open_new(main_url)
"""

def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token

while True:
    if show_active():
        url = get_socket_url()
        token = get_auth_token()
        if token == 'NONE':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)
    else:
        show_not_on()
        time.sleep(300)
