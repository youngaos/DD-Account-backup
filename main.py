import os

try:
    os.system("pip install -r requirements.txt")
except:
    os.system("pip3 install -r requirements.txt")

import aiohttp, pystyle, asyncio, colorama
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from colorama import init, Fore


banner = r"""

██████  ██████      ██████   █████   ██████ ██   ██ ██    ██ ██████  ███████ ██████  
██   ██ ██   ██     ██   ██ ██   ██ ██      ██  ██  ██    ██ ██   ██ ██      ██   ██ 
██   ██ ██   ██     ██████  ███████ ██      █████   ██    ██ ██████  █████   ██████  
██   ██ ██   ██     ██   ██ ██   ██ ██      ██  ██  ██    ██ ██      ██      ██   ██ 
██████  ██████      ██████  ██   ██  ██████ ██   ██  ██████  ██      ███████ ██   ██ 
                                                                                     

By; YoungAOS
- DeadDestroyers
Say NeverDies
"""[1:]



init(autoreset=True)
#============URL DE API BASE==============
BASE_URL = "https://discord.com/api/v9"
#============LOS LOGS===============
def log_success(message):
    print(f"{Fore.GREEN}[+] {message}")

def log_failure(message):
    print(f"{Fore.RED}[-] {message}")

#===========FUNCION DE GUARDAR AMIGOS==================
async def save_friends(token):
    headers = {'Authorization': token}

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/users/@me/relationships", headers=headers) as resp:
            if resp.status == 200:
                friends = await resp.json()
                with open("friends.txt", "w", encoding="utf-8") as f:
                    for friend in friends:
                        if friend['type'] == 1:  
                            f.write(f"{friend['user']['username']} - {friend['user']['id']}\n")
                log_success("Saved friends' names and IDs. ")
                print("Saving servers invites (THIS TAKE LONG).....")
            else:
                log_failure("Failed to fetch friends.")
#==========FUNCION DE GUARDAR SERVIDORES==============
async def save_servers(token):
    headers = {'Authorization': token}
    invites = []

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/users/@me/guilds", headers=headers) as resp:
            if resp.status == 200:
                servers = await resp.json()
                with open("servers.txt", "w", encoding="utf-8") as f:
                    for server in servers:
                        f.write(f"{server['id']} - {server['name']}\n")

                for server in servers:
                    async with session.get(f"{BASE_URL}/guilds/{server['id']}/channels", headers=headers) as channel_resp:
                        if channel_resp.status == 200:
                            channels = await channel_resp.json()
                            for channel in channels:
                                if channel['type'] == 0: 
                                    async with session.post(f"{BASE_URL}/channels/{channel['id']}/invites", headers=headers, json={"max_age": 0}) as invite_resp:
                                        if invite_resp.status == 200:
                                            invite = await invite_resp.json()
                                            invites.append(f"https://discord.gg/{invite['code']} - {server['id']} - {server['name']}")
                                            break 

                with open("invites.txt", "w", encoding="utf-8") as f:
                    for invite in invites:
                        f.write(f"{invite}\n")
                log_success("Saved servers' IDs, names, and invites.")
            else:
                log_failure("Failed to fetch servers.")

#==================FUNCION DE GUARDAR PFP==================
async def save_profile_picture(token):
    headers = {'Authorization': token}

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/users/@me", headers=headers) as resp:
            if resp.status == 200:
                user = await resp.json()
                avatar_url = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.{'gif' if user['avatar'].startswith('a_') else 'png'}"
                async with session.get(avatar_url) as resp_image:
                    image_data = await resp_image.read()
                    ext = ".gif" if user['avatar'].startswith('a_') else ".png"
                    with open(f"profile_picture{ext}", "wb") as f:
                        f.write(image_data)
                log_success("Saved profile picture.")
            else:
                log_failure("Failed to fetch profile picture.")
#===================FUNCION DE GUARDAR MDS===================
async def save_dms(token):
    headers = {'Authorization': token}

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/users/@me/channels", headers=headers) as resp:
            if resp.status == 200:
                dms = await resp.json()
                if not os.path.exists('dms'):
                    os.makedirs('dms')
                
                for dm in dms:
                    recipient_name = dm['recipients'][0]['username']
                    with open(f"dms/{recipient_name}.txt", "w", encoding="utf-8") as f:
                        async with session.get(f"{BASE_URL}/channels/{dm['id']}/messages?limit=100", headers=headers) as resp_dm_messages:
                            if resp_dm_messages.status == 200:
                                messages = await resp_dm_messages.json()
                                for message in messages:
                                    f.write(f"{message['author']['username']}: {message['content']}\n")
                log_success("Saved DMs.")
            else:
                log_failure("Failed to fetch DMs.")
#=====================INICIO==============================
async def main():
    print(Colorate.Vertical(Colors.white_to_red, banner, 1))
    token = input("[>] Account Token: ")

    headers = {'Authorization': token}

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/users/@me", headers=headers) as resp:
            if resp.status != 200:
                log_failure("Invalid token.")
                return

    save_friends_option = input("[>] Save friends name + id (y/n): ").strip().lower() == "y"
    save_servers_option = input("[>] Save servers id + name (y/n): ").strip().lower() == "y"
    save_pp_option = input("[>] Save profile picture (y/n): ").strip().lower() == "y"
    save_dms_option = input("[>] Save DMs (y/n): ").strip().lower() == "y"

    if save_friends_option:
        await save_friends(token)
    if save_servers_option:
        await save_servers(token)
    if save_pp_option:
        await save_profile_picture(token)
    if save_dms_option:
        await save_dms(token)

    log_success("Operation completed.")

asyncio.run(main())
