import discord
from discord.ext import commands
import os
import asyncio

# Configuration - using environment variables is safer!
USER_TOKEN = os.getenv('DISCORD_USER_TOKEN', "your_user_token_here")
AUTO_RESPONSE = "Hi there! 😊 I’m currently asleep, but I’ll reply as soon as I wake up. Thanks for your patience!"

class SelfBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", 
            self_bot=True,
            help_command=None
        )

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        
        # Set custom DND status with sleeping message
        await self.change_presence(
            status=discord.Status.dnd,
            activity=discord.CustomActivity(
                name="I'm currently sleeping 💤",  # The 💤 adds a sleeping emoji
                state="zzz..."  # Some clients may show this as secondary text
            )
        )

    async def on_message(self, message):
        if message.author == self.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            print(f"New DM from {message.author}: {message.content[:50]}...")
            try:
                await message.reply(AUTO_RESPONSE)
                print(f"Successfully replied to {message.author}")
            except discord.Forbidden:
                print(f"Couldn't reply to {message.author} (blocked or no permissions)")
            except Exception as e:
                print(f"Error replying to {message.author}: {str(e)}")

bot = SelfBot()

try:
    bot.run(USER_TOKEN)
except discord.LoginFailure:
    print("Invalid token - please check your USER_TOKEN")
except Exception as e:
    print(f"Error: {e}")