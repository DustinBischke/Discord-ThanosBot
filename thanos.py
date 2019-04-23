import asyncio
import discord
import random
from config import gauntlet

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
        channel = message.channel

        if channel.is_private:
            return

        if not message.author.server_permissions.administrator:
            await client.send_message(channel, 'You need the Administrator Stone to do that.')
            return

        server = message.server
        members = list(server.members)

        thanos_member = None

        for member in members:
            if member.id == client.user.id:
                thanos_member = member
                break

        thanos_roles = list(thanos_member.roles)
        thanos_role = thanos_roles[0]

        if len(thanos_roles) > 1:
            for role in thanos_roles:
                if role > thanos_role:
                    thanos_role = role

        if not thanos_member.server_permissions.ban_members and not thanos_member.server_permissions.administrator:
            await client.send_message(channel, 'I require the Administrator or Ban Members Stone to do that.')
            return

        ban_members = []

        for member in members:
            if member == thanos_member:
                continue

            if member == server.owner:
                continue

            # Thanos snap wouldn't affect bots. Prove me wrong.
            if member.bot:
                continue

            roles = list(member.roles)
            bannable = True

            if any(role > thanos_role for role in roles):
                bannable = False

            if bannable:
                ban_members.append(member)

        if len(ban_members) == 0:
            await client.send_message(channel, '{0} is already balanced.'.format(server.name))
            return

        if len(ban_members) >= (server.member_count / 2):
            ban_members = random.sample(ban_members, int(server.member_count / 2))

        print('Banning {0} members from {1}'.format(len(ban_members), server.name))

        for member in ban_members:
            try:
                await client.send_message(member, '{0}... you have my respect. I hope the people of {1} will '
                        'remember you.'.format(member.name, server.name))
                await client.ban(member, delete_message_days=0)
                print('Banning {0}'.format(member.name))
            except:
                print('Cannot ban {0}'.format(member.name))

        await client.send_message(channel, "***Snaps*** Fun isn't something one considers while balancing "
                "the universe, but this... does put a smile on my face.")


client.run(gauntlet.token)
