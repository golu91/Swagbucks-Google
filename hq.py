import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
#import Google_Search
import time
from datetime import datetime, timedelta
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

webhook_url="https://discordapp.com/api/webhooks/856696688437755934/9NW-2w46XZp-Sd2TmZuJTAg2hz7FVFPVDt4VY_7ZnXf_5yhjB1yQHGFe_Eh23KXMj8aM"

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
    main_url = f"https://api.playswagiq.com/trivia/home?_uid="
    headers = {
               "Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent": "SwagIQ-Android/34 (okhttp/3.10.0)"
              }
    try:
        response_data = requests.post(url=main_url, headers=headers).json()
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)
    main_url = 'https://api.playswagiq.com/trivia/join?_uid='
    headers = {"Authorization": "Bearer BoevwXaFzGYgR3WKHrH8L_tmGb0j_3k6a-dMEN2Z4iQPZiTHQ0uO9QKaR4NMf7H95hNUvf0LMO3aKVi031S7gVoc4yP_2w",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    print(response_data["success"])
    if response_data["success"] == False:
        print("Show not on.")
        data = response_data
        title = data["episode"]["title"]
        prize = data["episode"]["grandPrizeDollars"]
        prize = '{:,}'.format(int(prize))
        time = data["episode"]["start"]
        r = datetime.fromtimestamp(time)
        time_change = timedelta(hours=5, minutes=30)
        new_time = r + time_change
        time = new_time.strftime("%d-%m-%Y %I:%M %p")
        embed=discord.Embed(title="**__SwagIQ Next Show Details !__**", description=f"**• Show Name : Swagbucks Live\n• Show Time : {time}\n• Prize Money : ${prize}**", color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/840841165544620062/843859541627764776/762971334774489111.png")
        hook.send(embed=embed)


def show_active():
    main_url = 'https://api.playswagiq.com/trivia/join?_uid='
    headers = {"Authorization": "Bearer BoevwXaFzGYgR3WKHrH8L_tmGb0j_3k6a-dMEN2Z4iQPZiTHQ0uO9QKaR4NMf7H95hNUvf0LMO3aKVi031S7gVoc4yP_2w",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    return response_data['success']


def get_socket_url():
    main_url = 'https://api.playswagiq.com/trivia/join?_uid='
    headers = {"Authorization": "Bearer BoevwXaFzGYgR3WKHrH8L_tmGb0j_3k6a-dMEN2Z4iQPZiTHQ0uO9QKaR4NMf7H95hNUvf0LMO3aKVi031S7gVoc4yP_2w",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    #if response_data["success"] != False:
    id = response_data["viewId"]
    socket_url = f"wss://api.playswagiq.com/sock/1/game/{id}?_uid="
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
            print(message_data)
            if "comments" not in message_data:
                print(message_data)
            if message_data["code"] == 41:
                qn = message_data["question"]["number"]
                tqn = message_data["question"]["totalQuestions"]
                embed=discord.Embed(title=f"Question {qn} out of {tqn}", color=0x00ffff)
                hook.send(embed=embed)
            if message_data["code"] == 42:
                correct = message_data["correctAnswerId"]
                s = 0
                for answer in message_data["answerResults"]:
                    if answer["answerId"] == correct:
                        ansNum = answer["numAnswered"]
                    else:
                        anNum = answer["numAnswered"] 
                        s = s + anNum
                embed=discord.Embed(title=f"Advancing Players : {ansNum}\nElimineted Players : {s}", color=0x00ffff)
                hook.send(embed=embed)
            if message_data["code"] == 49:
                sb = message_data["winners"][0]["sb"]
                embed = discord.Embed(title="**__Game Summary !__**", description=f"**• Payout : {sb}SB\n• Total Winners : {advancing}\n• Prize Money : {prize}**", color=0x00ffff)
                hook.send(embed=embed)


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
