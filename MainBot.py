import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

deleted_channels = []  

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')

@bot.command()
async def clear_all_channels(ctx):
    if ctx.message.author.guild_permissions.administrator:
        for channel in ctx.guild.channels:
            # Vérifie si le canal n'a pas de catégorie parente
            if channel.category is None:
                await channel.delete()
        try:
            await ctx.send("Tous les canaux sans catégorie ont été supprimés.")
        except discord.NotFound:
            # Gestion de l'erreur si le canal d'origine a été supprimé
            pass
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

@bot.command()
async def createChannel(ctx):
    if ctx.message.author.guild_permissions.administrator:
        # Demande le nom du canal
        await ctx.send("Veuillez entrer le nom du canal:")
        
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel
        
        try:
            channel_name_msg = await bot.wait_for('message', check=check, timeout=30)
            channel_name = channel_name_msg.content
        except TimeoutError:
            await ctx.send("Temps écoulé. La création du canal a été annulée.")
            return

        # Demande le numéro du canal
        await ctx.send("Veuillez entrer le numéro du canal:")
        
        try:
            channel_number_msg = await bot.wait_for('message', check=check, timeout=30)
            channel_number = int(channel_number_msg.content)
        except (TimeoutError, ValueError):
            await ctx.send("Temps écoulé ou entrée invalide. La création du canal a été annulée.")
            return

        # Crée le canal avec le nom spécifié
        new_channel = await ctx.guild.create_text_channel(f'{channel_name}-{channel_number}')
        await ctx.send(f"Le canal '{new_channel.name}' a été créé avec succès.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")



@bot.command()
async def restore(ctx):
    if ctx.message.author.guild_permissions.administrator:
        global deleted_channels
        for channel in deleted_channels:
            await ctx.guild.create_text_channel(name=channel.name)  
            
        await ctx.send("Tous les canaux supprimés ont été restaurés.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

bot.run('MTE3MDAyMDI3NzgyOTI1NTIyOQ.GZBh3k.ScZaR4okKZKvGqmLw0Ks8tx-JFq_AD5Yu_ED8Q')
