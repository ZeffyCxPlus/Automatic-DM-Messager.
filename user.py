import discord
from discord.ext import commands
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")
AUTO_RESPONSE = "Hi there! 😊 I’m currently asleep, but I’ll reply as soon as I wake up. Thanks for your patience!"

class SelfBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", 
            self_bot=True,
            help_command=None
        )

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            logger.info(f"New DM from {message.author}: {message.content[:50]}{'...' if len(message.content) > 50 else ''}")
            try:
                await message.reply(AUTO_RESPONSE)
                logger.info(f"Sent auto-response to {message.author}")
            except discord.HTTPException as e:
                logger.error(f"Failed to send reply: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")

def main():
    if not USER_TOKEN:
        logger.error("No Discord user token provided. Set the DISCORD_USER_TOKEN environment variable.")
        return

    bot = SelfBot()
    
    try:
        bot.run(USER_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid token - please check your DISCORD_USER_TOKEN")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()