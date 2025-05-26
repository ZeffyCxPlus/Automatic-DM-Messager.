import discord
from discord.ext import commands
import os
import asyncio

# Configuration using environment variables (for Railway)
USER_TOKEN = os.getenv('DISCORD_USER_TOKEN')  # Get token from environment variables
AUTO_RESPONSE = os.getenv('AUTO_RESPONSE', "Hi there! 😊 I'm currently asleep, but I'll reply as soon as I wake up. Thanks for your patience!")

class SelfBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", 
            self_bot=True,
            help_command=None
        )

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        # Set DND status with custom status
        await self.change_presence(
            status=discord.Status.dnd,
            activity=discord.CustomActivity(name="I'm currently sleeping 💤")
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

def main():
    if not USER_TOKEN:
        print("Error: DISCORD_USER_TOKEN environment variable not set!")
        return

    bot = SelfBot()
    
    try:
        print("Starting bot...")
        bot.run(USER_TOKEN)
    except discord.LoginFailure:
        print("Invalid token - please check your DISCORD_USER_TOKEN")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        print("Bot has stopped")

if __name__ == "__main__":
    main()