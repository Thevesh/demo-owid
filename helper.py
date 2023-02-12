import telegram

from constants import TOKEN_BOT_OWID, ID_GROUP_OWID

# Initialize bot
bot = telegram.Bot(token=TOKEN_BOT_OWID)

async def send_message(chat_id=ID_GROUP_OWID, text=None):
    await bot.send_message(chat_id=chat_id, text=text)

async def send_image(chat_id=ID_GROUP_OWID, image_path=None, caption=None):
    with open(image_path, 'rb') as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption)

# Send a message with a file to the specified chat ID
async def send_file(chat_id=ID_GROUP_OWID, file_path=None, caption=None):
    with open(file_path, 'rb') as file:
        await bot.send_document(chat_id=chat_id, document=file, caption=caption)
