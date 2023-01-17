import discord
from discord.ext import commands
from discord import app_commands

sound_selected = "None"
sounds_path = "/home/Tintin/discord_bot/SoundBot/sounds/"

class main(commands.Cog):
    
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.voice = None
        self.channel = None
        
    # Commande executée au démarrage du Bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("Démarrage du SoundBot")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,
                                                                                               name="Tu veux du pain en boucle."))
        
    @commands.Cog.listener()
    async def on_message(self, message):
        msg_str = str(message.content)
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message) and message.mention_everyone == False:
            await message.channel.send(f"Hello {message.author.mention}, les commandes sont indiquées quand tu écrit '/' dans le chat.")
            
    
    # Pour synchroniser les commandes slash
    @commands.command()
    async def sync(self, ctx) -> None:
        ctx.bot.tree.clear_commands(guild=ctx.guild)
        
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} commandes ont été synchronisées.")
        
    
    # Connexion au salon vocal de l'utilisateur
    @app_commands.command(name="connect", description="Ajoute le bot dans ton channel vocal.")
    async def connect_voice(self, interaction: discord.Interaction) -> None:
        try:
            self.channel = interaction.user.voice.channel
        except:
            await interaction.response.send_message("Tu n'est pas connecté dans un salon vocal")
            return
        
        guild = interaction.guild
        self.voice = discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        
        if self.voice == None:
            await self.channel.connect()   
            self.voice = discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
            
        await interaction.response.send_message(f"Connecté dans le salon **{self.channel.name}**")
            
    # Déconnecte le bot du salon vocal actuel
    @app_commands.command(name="disconnect", description="Retire le bot de ton channel vocal.")
    async def disconnect_voice(self, interaction: discord.Interaction) -> None:
        if self.voice.is_playing():
            self.voice.stop()
        
        try:
            await self.voice.disconnect()
            await interaction.response.send_message("Déconnecté")
        except:
            await interaction.response.send_message("Le bot n'est connecté dans aucun salon vocal.")
        
    # Joue un son parmi dans la liste
    @app_commands.command(name="sound", description="Jouer un son dans un salon vocal.")
    @app_commands.describe(son="Sélectionnez un son")
    @app_commands.choices(son=[
        discord.app_commands.Choice(name="C'est nul !", value="1"),
        discord.app_commands.Choice(name="Fart Reverb SFX", value="2"),
        discord.app_commands.Choice(name="Salut mon pote !", value="3"),
        discord.app_commands.Choice(name="SEEEEEEEEGS", value="4"),
        discord.app_commands.Choice(name="Tu veux du pain ?", value="5"),
        discord.app_commands.Choice(name="Une blague sur les noirs", value="6"),
        discord.app_commands.Choice(name="Pouf", value="7")])
    async def sound_command(self, interaction: discord.Interaction, son: discord.app_commands.Choice[str]):
        
        try:
            self.channel = interaction.user.voice.channel
        except:
            await interaction.response.send_message("Tu n'est pas connecté dans un salon vocal.")
            return
        
        guild = interaction.guild
        self.voice = discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        
        if self.voice == None:
            await self.channel.connect()   
            self.voice = discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
            
        if self.voice.is_playing():
            self.voice.stop()
        self.voice.play(discord.FFmpegPCMAudio(f"{sounds_path}{son.name}.mp3"))
        
        await interaction.response.send_message(f"Lecture du son: '{son.name}'.")

async def setup(bot):
    await bot.add_cog(main(bot))