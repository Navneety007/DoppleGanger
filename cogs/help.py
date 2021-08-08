import discord
import random
from discord.ext import commands

colours = [':blue_circle:',':green_circle:',':orange_circle:',':purple_circle:',':red_circle:',':yellow_circle:',':black_circle:',':brown_circle:',':white_circle:',':blue_circle:',':green_circle:',':orange_circle:',':purple_circle:',':red_circle:',':yellow_circle:',':black_circle:',':brown_circle:',':white_circle:',':blue_circle:',':green_circle:',':orange_circle:',':purple_circle:',':red_circle:',':yellow_circle:',':black_circle:',':brown_circle:',':white_circle:']
colors = [0x0dd2ff,0x03f5ff,0x2affa9,0x18e6ff,0x17ffc2,0x03f5ff,0x30e79d]

class HelpCommand(commands.HelpCommand):
    """
    An Embed help command
    Based on https://gist.github.com/Rapptz/31a346ed1eb545ddeb0d451d81a60b3b
    """

    color = 0x2F3136

    def get_ending_note(self):
        return "Use {0}{1} [command] for more info on a command.".format(
            self.clean_prefix, self.invoked_with
        )

    def get_command_signature(self, command):
        return "{0.qualified_name} {0.signature}".format(command)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Bot Commands", color=self.color)
        embed.set_thumbnail(url = "https://cdn.discordapp.com/avatars/781737639321141268/f1596855aaf148e5eab77ca9a3553649.webp?size=1024")
        description = self.context.bot.description
        if description:
            embed.description = description
        counter = 0
        for cog, cmds in mapping.items():
            if cog is None or cog.qualified_name == "Jishaku":
                continue
            name = cog.qualified_name
            filtered = await self.filter_commands(cmds, sort=True)
            if filtered:
                value = "\t\t   ".join(f"`{c.name}`" for c in cmds)
                if cog and cog.description:
                    value = "{0}\n{1}".format(cog.description, value)

                embed.add_field(name=f"{colours[counter]}   {name}", value=value)
                counter+=1

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title="{0.qualified_name} Commands".format(cog), color=random.choice(colors)
        )
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        counter = 0
        for command in filtered:
            embed.add_field(
                name=f"{colours[counter]}  {command.qualified_name}",
                value=command.short_doc or "..."
            )
            counter+=1

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name, color=self.color)
        if group.help:
            embed.description = group.help

        filtered = await self.filter_commands(group.commands, sort=True)
        for command in filtered:
            embed.add_field(
                name=command.qualified_name,
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.qualified_name, color=random.choice(colors))
        embed.add_field(name="Signatute", value=self.get_command_signature(command))
        if command.aliases:
            embed.add_field(name="Alternatives/Aliases", value="   ".join([f"`{i}`" for i in command.aliases]),inline=False)
        if command.help:
            embed.description = command.help

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)


def setup(bot: commands.Bot):
    bot.help_command = HelpCommand()
