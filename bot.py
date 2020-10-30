import discord
import os
import sys
import asyncio


def embed_not_muted_default(self, voice_channel, user=None):
    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name=self.user.display_name,
                     icon_url=self.user.avatar_url)
    embed.add_field(name="🔈 %s" % voice_channel.name,
                    value="Mute Us wurde erfolgreich aktiviert! Mit den Reaktionen unten kann jeder den Sprachkanal **%s** laut- und stummschalten." % voice_channel.name,
                    inline=False)
    return embed


def embed_muted_default(self, voice_channel, user=None):
    embed = discord.Embed(color=discord.Color.red())
    embed.set_author(name=self.user.display_name,
                     icon_url=self.user.avatar_url)
    embed.add_field(name="🔇 %s" % voice_channel.name,
                    value="Mute Us wurde erfolgreich aktiviert! Mit den Reaktionen unten kann jeder den Sprachkanal **%s** laut- und stummschalten." % voice_channel.name,
                    inline=False)
    return embed


def embed_not_muted(self, voice_channel, user):
    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name=self.user.display_name,
                     icon_url=self.user.avatar_url)
    embed.add_field(name="🔈 %s" % voice_channel.name,
                    value="Mute Us wurde erfolgreich aktiviert! Mit den Reaktionen unten kann jeder den Sprachkanal **%s** laut- und stummschalten." % voice_channel.name,
                    inline=False)
    embed.set_footer(text="%s wurde von %s lautgeschaltet." %
                     (voice_channel.name, user.display_name))
    return embed


def embed_muted(self, voice_channel, user):
    embed = discord.Embed(color=discord.Color.red())
    embed.set_author(name=self.user.display_name,
                     icon_url=self.user.avatar_url)
    embed.add_field(name="🔇 %s" % voice_channel.name,
                    value="Mute Us wurde erfolgreich aktiviert! Mit den Reaktionen unten kann jeder den Sprachkanal **%s** laut- und stummschalten." % voice_channel.name,
                    inline=False)
    embed.set_footer(text="%s wurde von %s stummgeschaltet." %
                     (voice_channel.name, user.display_name))
    return embed


def embed_disabled(self):
    embed = discord.Embed(color=discord.Color.dark_grey())
    embed.set_author(name=self.user.display_name,
                     icon_url=self.user.avatar_url)
    embed.add_field(name="Mute Us deaktiviert",
                    value="Dieses Widget wurde deaktiviert, da sich niemand mehr in dem dazugehörigen Voicechannel befindet, ein neueres Widget existiert oder der Bot neugestartet wurde.\n\nMit dem Befehl `!muteus` kannst du jederzeit ein neues Widget erstellen!",
                    inline=False)
    return embed


async def is_muted(self, voice_channel):
    if voice_channel == None:
        return False
    for channel in voice_channel.guild.text_channels:
        try:
            async for message in channel.history(limit=100):
                try:
                    if message.author == self.user and message.embeds[0].fields[0].value.startswith("Mute Us wurde erfolgreich aktiviert!"):
                        if message.embeds[0].fields[0].name[2:] == voice_channel.name and message.embeds[0].fields[0].name[:1] == "🔇":
                            return True
                except IndexError:
                    pass
        except discord.errors.Forbidden:
            pass
    return False


class MyClient(discord.Client):
    async def on_ready(self):
        print('Angemeldet als %s auf %s Servern!\n' %
              (self.user, len(self.guilds)))

        # Entferne alte Mute Us-Widgets
        for guild in self.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=100):
                        try:
                            if message.author == self.user and message.embeds[0].fields[0].value.startswith("Mute Us wurde erfolgreich aktiviert!"):
                                await message.edit(embed=embed_disabled(self))
                                await message.clear_reactions()
                        except IndexError:
                            pass
                except discord.errors.Forbidden:
                    pass

    async def on_message(self, message):
        if message.content in ["!invite", "!about", "!help", "!info", "!hilfe", "!github", "!commands", "!befehle", "!einladung", "!einladungslink", "!add", "!link"]:
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
                if await is_muted(self, voice_channel):
                    msg = await message.channel.send(embed=embed_muted_default(self, voice_channel))
                else:
                    msg = await message.channel.send(embed=embed_not_muted_default(self, voice_channel))
                await msg.add_reaction("🔈")
                await msg.add_reaction("🔇")

                # Überprüfe ob bereits ein Mute Us-Widget existiert, entferne dieses

                for channel in message.guild.text_channels:
                    try:
                        async for message in channel.history(limit=100):
                            try:
                                if message.author == self.user and message != msg and message.embeds[0].fields[0].name[2:] == voice_channel.name and message.embeds[0].fields[0].value.startswith("Mute Us wurde erfolgreich aktiviert!"):
                                    await message.edit(embed=embed_disabled(self))
                                    await message.clear_reactions()
                            except IndexError:
                                pass
                    except discord.errors.Forbidden:
                        pass

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

            # Überprüfe ob Reaktionen vom Bot vorhanden sind (Cooldown)
            cooldown = False
            for r in reaction.message.reactions:
                if r.me and r.emoji == "🔈":
                    cooldown = True
                    break

            if user in voice_channel.members and cooldown:
                # Sprachkanal stumm
                if reaction.emoji == "🔇" and reaction.message.embeds[0].fields[0].name[:1] != "🔇":
                    await reaction.message.clear_reactions()
                    await reaction.message.edit(embed=embed_muted(self, voice_channel, user))

                    # Push-to-Talk
                    # await voice_channel.set_permissions(reaction.message.guild.default_role, use_voice_activation=False, reason="Benutzer %s hat alle stummgeschaltet (Mute Us-Bot)." % user)

                    # Force Mute
                    for member in voice_channel.members:
                        if not member.voice.mute:
                            await member.edit(mute=True, reason="Benutzer %s hat alle stummgeschaltet (Mute Us-Bot)." % user)
                            await asyncio.sleep(0.2)

                    print("Der Sprachkanal %s wurde von %s stummgeschaltet." %
                          (voice_channel, user))

                    await reaction.message.add_reaction("🔈")
                    await reaction.message.add_reaction("🔇")

                # Sprachkanal laut
                elif reaction.emoji == "🔈" and reaction.message.embeds[0].fields[0].name[:1] != "🔈":
                    await reaction.message.clear_reactions()
                    await reaction.message.edit(embed=embed_not_muted(self, voice_channel, user))

                    # Disable Push-to-Talk
                    # await voice_channel.set_permissions(reaction.message.guild.default_role, use_voice_activation=None, reason="Benutzer %s hat alle lautgeschaltet (Mute Us-Bot)." % user)

                    # Disable Force Mute
                    for member in voice_channel.members:
                        if member.voice.mute:
                            await member.edit(mute=False, reason="Benutzer %s hat alle lautgeschaltet (Mute Us-Bot)." % user)
                            await asyncio.sleep(0.2)

                    print("Der Sprachkanal %s wurde von %s lautgeschaltet." %
                          (voice_channel, user))

                    await reaction.message.add_reaction("🔈")
                    await reaction.message.add_reaction("🔇")

    async def on_voice_state_update(self, member, before, after):
        # Mute Mitglieder, die gemuteten Channel betreten
        if before.channel != after.channel and await is_muted(self, after.channel) and not member.voice.mute:
            await member.edit(mute=True, reason="Benutzer hat gemuteten Sprachkanal betreten (Mute Us-Bot).")
            await asyncio.sleep(0.2)

        # Entmute Mitglieder, die nicht-gemuteten Channel betreten
        if before.channel != after.channel and not await is_muted(self, after.channel) and member.voice.mute:
            await member.edit(mute=False, reason="Benutzer hat gemuteten Sprachkanal verlassen (Mute Us-Bot).")
            await asyncio.sleep(0.2)

            # Entferne Widget wenn Channel leer
        if before.channel != after.channel and before.channel != None:
            # Überprüft ob der verlassene Sprachkanal nun leer ist
            if len(before.channel.members) == 0:
                # Suche ob ein Mute Us Widget für diesen Channel existiert und entferne es
                for channel in before.channel.guild.text_channels:
                    try:
                        async for message in channel.history(limit=100):
                            try:
                                if message.author == self.user and message.embeds[0].fields[0].name[2:] == before.channel.name and message.embeds[0].fields[0].value.startswith("Mute Us wurde erfolgreich aktiviert!"):
                                    await message.edit(embed=embed_disabled(self))
                                    await message.clear_reactions()
                            except IndexError:
                                pass
                    except discord.errors.Forbidden:
                        pass


client = MyClient()
client.run(os.environ["mute-us"])
