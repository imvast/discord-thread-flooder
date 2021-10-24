import aiohttp, discord, os, time, requests, asyncio
from threading import Thread
from colorama import Fore as C
from discord.ext import commands
os.system('cls')

print("! FROM THE SMALL CHANCE THERE IS, I AM NOT RESPONSIBLE FOR ANYTHING THAT COULD HAPPEN TO YOUR ACCOUNT. USE AT YOUR OWN RISK. !")
token = input("? User Token -> ")
prefix = input("? Prefix -> ")
questioning=True
while questioning==True:
    threadnames = input("? Thread Names -> ")
    if len(threadnames) >= 20: print("! Thread names should be under 20 characters.")
    else: questioning=False

      
bot = commands.Bot(command_prefix=prefix, self_bot=True)


def MassThread(ctx, maxamount):
    while maxamount >= 0:
        r = requests.post(f"https://canary.discord.com/api/v9/channels/{ctx.channel.id}/threads", json={"name": f"{threadnames}", "type": 11, "auto_archive_duration": 60, "location": "Slash Command"}, headers={"Authorization": f"{token}"})
        if r.status_code != int(201):
            print(f"{C.RED}{r.status_code} {C.LIGHTBLACK_EX}~{C.RED} {r.json()}{C.RESET}")
            if r.json()['retry_after'] >= 200:
                print(f"{C.LIGHTBLACK_EX}!{C.LIGHTRED_EX} higher than 200 seconds, attemping to end loop.{C.RESET}")
                break
        elif r.status_code == int(404):
            print(f"{C.LIGHTBLACK_EX}!{C.LIGHTRED_EX} channel deleted, attemping to end loop.{C.RESET}")
            break
        elif r.status_code == int(429):
            print(f"{C.LIGHTBLACK_EX}!{C.LIGHTRED_EX} damn g u got api banned :({C.RESET}")
            break
        else:
            print(f"{C.GREEN}{r.status_code} {C.LIGHTBLACK_EX}~{C.GREEN} CREATED{C.RESET}")
            maxamount - 1
        continue



@bot.command(name="threadspam", description="Spams threads", usage="threadspam [maxamount]", brief="abuse")
async def threadspam(ctx, maxamount:int=50):
    try: await ctx.message.delete()
    except: pass
    threads = []
    for i in range(maxamount):
        thread = Thread(target=MassThread, args=(ctx, maxamount,)).start()
        threads.append(thread)



@bot.event
async def on_connect():
  print(f"\n {C.LIGHTGREEN_EX}+ {C.LIGHTBLACK_EX}Connected. Prefix is: {C.YELLOW}%s{C.RESET}\n\n" % bot.command_prefix)

bot.run(token, bot=False)
