import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
from time import strftime

bot = commands.Bot(command_prefix = "p/", description = "Le 1er bot en Python de xis3000 !")
ownerList = ["758555031670358056", "717817882720862248", "620679739929133110"]
status = ["Ce bot est fait par xis3000", 
        "Je sert à la modération du SpaceShop", 
        "Le SpaceShop est le meuilleur market de Paladium", 
        "Merci pour tout",
        "Ce status change toutes les 30 secondes"]

#function du roles mute

async def createMutedRoles(ctx):
    mutedRole = await ctx.guild.create_role(name = "Mute by SpaceModération", permissions = discord.Permissions(
                                                                                send_messages = False,
                                                                                speak = False,))
                                                                                
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
        return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Mute by SpaceModération":
            return role
    await createMutedRoles()


#events

@bot.event
async def on_ready():
    print("Pret !")
    changeStatus.start()

#tasks

@tasks.loop(seconds = 30)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status = discord.Status.dnd, activity = game)

#commandes 


@bot.command()
async def coucou(ctx):
    
    await ctx.send("Coucou")

@bot.command()
async def ping(ctx):
    await ctx.send('Ma latence: {0} ms !'.format(round(bot.latency, 3)))

@bot.command()
async def servInfo(ctx):
    server = ctx.guild
    numberT = len(server.text_channels)
    numberV = len(server.voice_channels)
    desc = server.description
    nbPerson = server.member_count
    name = server.name
    msg = f"Voici les informations du server **{name}**:\n Membres: **{nbPerson}**. \n Salons écrits: **{numberT}**. \n Salons vocaux: **{numberV}**"
    await ctx.send(msg)
  
@bot.command()
async def say(ctx, *txt):
   
    await ctx.send(" ".join(txt))

@bot.command()
async def maj(ctx, *txt):
    maj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    majTxt = []
    for word in txt:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = maj[index]
                majTxt.append(transformed)
            else:
                majTxt.append(char) 
        majTxt.append(" ")  
    await ctx.send("".join(majTxt)) 
    
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *, reason = "Aucune n'en a été donnée"):
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} a été kick pour la raison: **{reason}**")
   
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for msg in messages:
        await msg.delete()
    
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason = "Aucune n'en a été donnée"):
    await ctx.guild.ban(user, reason = reason)
    banEmbeds = discord.Embed(title = "**Banissement**", description = "Un membre a été banni !", color = 0x0082ff)
    banEmbeds.set_author(name = user.name, icon_url = user.avatar_url)
    banEmbeds.set_thumbnail(url = "https://cdn.discordapp.com/attachments/972586267151851580/972586839384915998/recrutement_modo_.png")
    banEmbeds.add_field(name = "Membre banni", value = user.name, inline = True)
    banEmbeds.add_field(name = "Raison", value = reason, inline = True)
    banEmbeds.add_field(name = "Modérateur", value = ctx.author.name, inline = False)

    await ctx.send(embed = banEmbeds)
    
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user):
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user)
            await ctx.send(f"{user} a été unban")
            return
    await ctx.send(f"L'utilisateur {user} n'a pas été trouvé")   
   
@bot.command()
@commands.has_permissions(manage_messages = True)
async def mute(ctx, user : discord.User):
    mutedRole = getMutedRole(ctx) 
    await user.add_roles(mutedRole)
    await ctx.send(f"{user} a été mute par {ctx.author.name} ")

@bot.command()
async def helpmenu(ctx):
    helpEmbed = discord.Embed(title = "Menu d'aide", description = "Voici le menu d'aide aux commandes, vous trouverez si dessous toutes les commandes:", color = 0x0082ff)
    helpEmbed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/972586267151851580/972586841108783114/Logo_SpaceShop.png")
    helpEmbed.add_field(name = "Commandes accessibles à tous", value = "-ping: donne la latence du bot \n -maj: met ton message en majuscule \n -say: fait parler le bot \n -servInfo: donne les informations sur le serveur", inline = False)
    helpEmbed.add_field(name = "Pour les modérateurs:", value = "-kick [membre] [raison]: exclu le membre mentionné \n -ban [membre] [raison]: banni le membre mentionné \n -unban [pseudo + tag]: déban la personne \n -clear [nombre]: efface le nombre de messages demander", inline = False)
    await ctx.send(embed = helpEmbed)

bot.run("Votre token")
