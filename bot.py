import discord
import os
import sys
import asyncio


class MyClient(discord.Client):
    async def on_ready(self):
        print('Angemeldet als %s auf %s Servern!\n' %
              (self.user, len(self.guilds)))

    async def on_message(self, message):
        if message.content in ["!invite", "!about", "!help"]:
            # Zeigt den About-Dialog
            embed = discord.Embed(color=0xffde28)
            embed.set_author(name=self.user.display_name,
                             icon_url=self.user.avatar_url)
            embed.add_field(
                name="Über diesen Bot",
                value="Dieser Bot ermöglicht das einfache Stummschalten aller Mitglieder in einem Sprachkanal über Reaktionen. Dies kann zum Beispiel für Among Us nützlich sein!",
                inline=False)
            embed.add_field(
                name="So funktioniert's:",
                value="Begib dich in einen öffentlichen Sprachkanal und gib in einem Textkanal den Befehl `!muteus` ein. Mit einem Klick auf die Reaktionen kannst du ganz einfach alle Mitglieder in deinem Sprachkanal laut - bzw. stummzuschalten.",
                inline=False)
            embed.add_field(
                name="Einladungslink:", value="https://discord.com/oauth2/authorize?client_id=766610562205089802&permissions=272723024&scope=bot", inline=True)
            embed.add_field(
                name="GitHub:", value="https://github.com/CrazyEasy/mute-us-discord-bot", inline=True)

            await message.channel.send(embed=embed)

        if message.content in ["!reload", "!restart"] and message.author.id == 219389750111502348:
            # Startet das Programm neu
            print("Bot per Befehl neugestartet.\n")
            await message.add_reaction("✅")
            os.execv(sys.executable, ['python'] + [sys.argv[0]])

        if message.content in ["!update", "!pull"] and message.author.id == 219389750111502348:
            # Lädt die neuste Version herunter
            print("Neuste Version wird heruntergeladen...\n")
            await message.add_reaction("⬇️")
            os.system("git pull https://github.com/CrazyEasy/mute-us-discord-bot")
            # Startet das Programm neu
            print("Neuste Version runtergeladen. Bot wird neugestartet.\n")
            await message.add_reaction("✅")
            os.execv(sys.executable, ['python'] + [sys.argv[0]])

        if message.content == "!muteus":
            # Findet den Sprachkanal, in dem sich der User befindet, der den Befehl ausführt
            voice_channel = None
            for vc in message.guild.voice_channels:
                if message.author in vc.members:
                    voice_channel = vc

            # Wenn sich der Benutzer in einem Sprachkanal befindet, wird die Nachricht mit den Reaktionen ausgegeben
            if voice_channel:
                embed = discord.Embed()
                embed.set_author(name=self.user.display_name,
                                 icon_url=self.user.avatar_url)
                embed.add_field(
                    name="🔈 %s" % voice_channel.name,
                    value="""Mute Us wurde erfolgreich aktiviert! Mit den Reaktionen unten
                            kann jeder den Sprachkanal **%s** laut- und stummschalten.""" % voice_channel.name,
                    inline=False)
                msg = await message.channel.send(embed=embed)
                await msg.add_reaction("🔈")
                await msg.add_reaction("🔇")

            # Fehlermeldung, wenn der Benutzer sich nicht in einem Sprachkanal befindet
            else:
                embed = discord.Embed(color=0xf61717)
                embed.set_author(name=self.user.display_name,
                                 icon_url=self.user.avatar_url)
                embed.add_field(
                    name="Fehler",
                    value="""Du musst dich in einem Sprachkanal befinden, um diesen
                             Befehl ausführen zu können!""",
                    inline=False)
                await message.channel.send(embed=embed)

    async def on_reaction_add(self, reaction, user):
        # Überprüfe, ob Reaktion auf Nachricht von Bot und nicht von Bot selber
        if reaction.message.author == self.user and user != self.user:

            # Entfernt die Reaktion
            await reaction.remove(user)

            # Findet den zur Nachricht passenden Sprachkanal
            voice_channel = discord.utils.get(
                reaction.message.guild.voice_channels, name=reaction.message.embeds[0].fields[0].name[2:])

            # Schaltet den Sprachkanal laut-/stumm
            for member in voice_channel.members:
                if reaction.emoji == "🔇" and not member.voice.mute:
                    await member.edit(mute=True, reason="Mute Us")
                    await asyncio.sleep(0.15)
                elif reaction.emoji == "🔈" and member.voice.mute:
                    await member.edit(mute=False, reason="Mute Us")
                    await asyncio.sleep(0.15)


client = MyClient()
client.run(os.environ["mute-us"])
