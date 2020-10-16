import discord
import os


class MyClient(discord.Client):
    async def on_ready(self):
        print('Angemeldet als %s auf %s Servern!\n' %
              (self.user, len(self.guilds)))

    async def on_message(self, message):
        if message.content == "!invite":
            embed = discord.Embed()
            embed.set_author(name=self.user.display_name,
                             icon_url=self.user.avatar_url)
            embed.add_field(
                name="Einladungslink:", value="https://discord.com/oauth2/authorize?client_id=766610562205089802&permissions=272723024&scope=bot", inline=False)

            await message.channel.send(embed=embed)

        if message.content == "!muteus":
            voice_channel = None
            for vc in message.guild.voice_channels:
                if message.author in vc.members:
                    voice_channel = vc

            if voice_channel:
                embed = discord.Embed()
                embed.set_author(name=self.user.display_name,
                                 icon_url=self.user.avatar_url)
                embed.add_field(
                    name="🔈 %s" % voice_channel.name,
                    value="""Mute Us wurde erfolgreich aktiviert! Mit den Reaktions-Buttons
                             unten kann jeder den Sprachkanal **%s** laut- und stummschalten.""" % voice_channel.name,
                    inline=False)
                msg = await message.channel.send(embed=embed)
                await msg.add_reaction("🔈")
                await msg.add_reaction("🔇")

            else:
                embed = discord.Embed(color=0xf50000)
                embed.add_field(
                    name="Fehler",
                    value="""Du musst dich in einem Sprachkanal befinden, um diesen
                             Befehl ausführen zu können.""",
                    inline=False)
                await message.channel.send(embed=embed)

    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.user and user != self.user:
            await reaction.remove(user)
            voice_channel = discord.utils.get(
                reaction.message.guild.voice_channels, name=reaction.message.embeds[0].fields[0].name[2:])

            for member in voice_channel.members:
                if reaction.emoji == "🔇":
                    await member.edit(mute=True, reason="Mute Us")
                elif reaction.emoji == "🔈":
                    await member.edit(mute=False, reason="Mute Us")


client = MyClient()
client.run(os.environ["token"])
