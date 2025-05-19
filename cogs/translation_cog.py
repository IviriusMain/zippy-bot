from discord.ext import commands
import aiohttp
import urllib.parse


class TranslationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translate_emoji_id = 1374028281682202734

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if the reaction is the translation emoji
        if payload.emoji.id != self.translate_emoji_id:
            return

        # Get the channel and message
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        # Check if the bot has already reacted with the translate emoji
        for reaction in message.reactions:
            if (
                reaction.emoji
                and hasattr(reaction.emoji, "id")
                and reaction.emoji.id == self.translate_emoji_id
            ):
                users = [user async for user in reaction.users()]
                if any(user.id == self.bot.user.id for user in users):
                    return  # Bot has already reacted, so skip

        # Check if there's content to translate
        if not message.content:
            return

        # Show typing indicator to indicate processing
        async with channel.typing():
            try:
                # Translate the message
                translated_text = await self.translate_text(message.content)

                # Send the translated message as a reply
                await message.reply(
                    f"**Translation:** {translated_text}", mention_author=False
                )

                # Add the translate emoji reaction to indicate successful translation
                translate_emoji = f"<:translate:{self.translate_emoji_id}>"
                await message.add_reaction(translate_emoji)

            except Exception as e:
                print(f"Translation error: {e}")

    async def translate_text(self, text):
        """Translate text to English using pollinations.ai API (aiohttp)"""
        # URL encode the text and system prompt
        encoded_text = urllib.parse.quote(text)
        system_prompt = urllib.parse.quote(
            "You are an excellent translator. Translate the following text to English. Only return the translated text without any explanations."
        )

        # Prepare API URL
        url = f"https://text.pollinations.ai/{encoded_text}?model=openai&system={system_prompt}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    error_text = await response.text()
                    raise Exception(
                        f"Translation API returned status code {response.status}: {error_text}"
                    )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Translation cog ready")


async def setup(bot):
    await bot.add_cog(TranslationCog(bot))
    print("Loaded translation_cog.py")
