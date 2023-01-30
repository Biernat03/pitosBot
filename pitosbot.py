import discord
from discord.ext import commands
from discord.utils import get
import json

#start
def run_discord_bot():
    #client
    #load token
    f = open('token.json', 'r', encoding='utf-8')
    data = json.load(f)
    TOKEN = data['token']
    f.close()
    
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)
    #on join
    on_join = True
    on_join_channel = 1068874871808991344
    on_leave = True
    on_leave_channel = 1068874871808991344
#activity
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        #setting custom activity
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='p!help'))
        
#join message
    @client.event
    async def on_member_join(member):
        if on_join == True:
            channel = client.get_channel(on_join_channel)
            await channel.send(f'{member.mention} just joined!')     
    
#leave message
    @client.event
    async def on_member_remove(member):
        if on_leave == True:
            channel = client.get_channel(on_leave_channel)
            await channel.send(f'{member.mention} just left!')
        
#messages
    @client.event
    async def on_message(message):
            
        #loop fix
        if message.author == client.user:
            return
        else:
            #config load
            f = open('config.json', 'r', encoding='utf-8')
            data = json.load(f)
            prefix = data['prefix']
            for i in data['roles']:
                adminRoleId = i['admin']
                clearRole = i['clear']
            f.close()
            
            #users
            username = str(message.author)
            user_message = str(message.content)
            
            #prefix
            prefixLength = len(prefix)
            prefixMax = 3
            prefixMin = 1
            
            #channels
            channelName = str(message.channel)
            channelMessage = message.channel.id
            acceptedchannel = 1068273626903748800
            channel = message.channel
            
            #servers
            commandGuild = message.guild
            acceptedchannelName = 'pitos'
            guild = client.guilds[1]
            
            #admin role
            adminRoleName = commandGuild.get_role(adminRoleId)
            
            #prefix lower
            p_message = message.content.lower()
            
            #messages / prefix check
            if channelMessage == acceptedchannel or channelName == acceptedchannelName or p_message[prefixLength:] == 'clear':
                userRoles = message.author.roles
                for i in userRoles:
                    if i == adminRoleName:
                        isAdmin = True
                    else:
                        isAdmin = False
                    if i == clearRole:
                        isClear = True
                    else:
                        isClear = False
                if p_message.startswith(prefix) or p_message == 'p!help':
                    #console log
                    print(f'User: "{username}", texted: "{message.content}", on server: "{commandGuild}", on channel: "{channelName}"')
                    #help
                    if p_message[prefixLength:] == 'help' or p_message == 'p!help':
                        await message.channel.send(f'```Actual prefix is "{prefix}"\n{prefix}myid - to show your discord id\n{prefix}prefixset [new prefix]```')
                    #myid
                    elif p_message[prefixLength:] == 'myid':
                        await message.channel.send(f'```{username}```')
                    #prefix check
                    elif p_message[prefixLength:] == 'prefix':
                        await message.channel.send(f'```Actual prefix is "{prefix}"```')
                    #prefix change
                    elif p_message[prefixLength:prefixLength+9] == 'prefixset' and isAdmin:
                        if message.author.guild.owner:
                            commandLength = prefixLength + 10
                            prefixNew = p_message[commandLength:]
                            prefixNewLength = len(prefixNew)
                            if prefixNewLength >= prefixMin and prefixNewLength <= prefixMax:
                                f = open("config.json", 'w', encoding='utf-8')
                                data['prefix'] = prefixNew
                                json.dump(data, f)
                                f.close()
                                await message.channel.send(f'```Prefix changed to "{prefixNew}"```')
                            else:
                                await message.channel.send("```Prefix length is incorrect (1-3)```")
                    #channel clear
                    elif p_message[prefixLength:prefixLength+9] == 'clear' and (message.author.guild_permissions.manage_messages or isAdmin or isClear):
                        if message.author.guild_permissions.administrator:
                            await channel.purge()
                    #fail command
                    else:
                        await message.channel.send(f"```I don't understand, try {prefix}help```")

    client.run(TOKEN)