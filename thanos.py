import asyncio
import discord
import random
from config import config

client = discord.Client()

@client.event
async def on_ready():
    print('Connected as: {}'.format(client.user.name))
    print('Discord.py Version: {}'.format(discord.__version__))
    await client.change_presence(game=discord.Game(name='Balancing The Universe'))

@client.event
async def on_server_join(server):
    print('Added to server: {}'.format(server.name))

@client.event
async def on_server_leave(server):
    print('Removed from server: {}'.format(server.name))

@client.event
async def on_message(message):
    if message.content.lower().startswith('!snap') and not message.author.bot:
        if message.channel.is_private:
            return

        if not message.author.server_permissions.administrator:
            await client.send_message(message.channel, "You need the Administrator Stone to do that")
            return

        server = message.server
        members = list(server.members)
        member_count = int(server.member_count / 2)
        members = random.sample(members, member_count)

        thanos_id = client.user.id
        thanos_member = None

        for member in server.members:
            if member.id == thanos_id:
                thanos_member = member

        thanos_roles = list(thanos_member.roles)
        thanos_role = thanos_roles[0]

        if len(thanos_roles) > 1:
            for role in thanos_roles:
                if role > thanos_role:
                    thanos_role = role

        if not thanos_member.server_permissions.ban_members and not thanos_member.server_permissions.administrator:
            await client.send_message(message.channel, "I require the Administrator or Ban Members Stone to do that")
            return

        for member in members:
            if member.id == thanos_id:
                continue

            user_roles = list(member.roles)
            user_role = user_roles[0]

            if len(user_roles) > 1:
                for role in user_roles:
                    if role > user_role:
                        user_role = role

            if thanos_role > user_role:
                try:
                    await client.send_message(member, '{0}... you have my respect. I hope the people of Earth will '
                            'remember you.'.format(member.name))
                    await client.ban(member, delete_message_days=0)
                    print('Banning {0}'.format(member.name))
                except:
                    print('Cannot ban {0}'.format(member.name))
            else:
                print('Cannot ban {0}: Need higher permission level'.format(member.name))

        await client.send_message(message.channel, "***Snaps*** Fun isn't something one considers while balancing "
                "the universe, but this... does put a smile on my face.")


client.run(config.token)
