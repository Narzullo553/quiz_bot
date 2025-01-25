from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")
import os

print("Environment Variables:")
print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))
print("ADMINS:", os.getenv("ADMINS"))
print("IP:", os.getenv("ip"))

  # Xosting ip manzili
