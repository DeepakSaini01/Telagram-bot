import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from example import example

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = InferenceClient(token=HF_API_KEY)

example()

async def query_huggingface(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

@dp.message(Command(commands=["start", "help"]))
async def welcome(message: types.Message):
    await message.reply("👋 Hello! I'm a Genie🧞‍♂ chatbot. Ask me anything!")

@dp.message()
async def llama_reply(message: types.Message):
    await message.reply("🤔 Thinking...")
    reply = await query_huggingface(message.text)
    await message.reply(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
