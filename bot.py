import asyncio
import os
import random
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands, tasks

# 1. إعداد سيرفر Flask لضمان التشغيل 24/7 على Render
app = Flask("")


@app.route("/")
def home():
  return "Zekr Bot is active 24/7!"


def run_flask():
  app.run(host="0.0.0.0", port=10000)


def keep_alive():
  t = Thread(target=run_flask)
  t.start()


# 2. إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=["!"], intents=intents)

# آيدي روم الأذكار المخصص الذي أرسلته
ZEKR_CHANNEL_ID = 1556562624421040208

# قائمة أذكار واسعة ومتنوعة مع آية الكرسي
AZKAR_LIST = [
    {
        "title": "آيَةُ الْكُرْسِي",
        "text": (
            "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا"
            " تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَهُ ما في السَّمَاواتِ وَما"
            " فِي الْأَرْضِ ۗ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا"
            " بِإِذْنِهِ ۚ يَعْلَمُ ما بَيْنَ أَيْدِيهِمْ وَما خَلْفَهُمْ ۖ"
            " وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِما شاءَ ۚ"
            " وَسِعَ كُرْسِيُّهُ السَّمَاواتِ وَالْأَرْضَ ۖ وَلا يَئُودُهُ"
            " حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ"
        ),
        "note": "من قرأها دبر كل صلاة لم يمنعه من دخول الجنة إلا أن يموت.",
    },
    {
        "title": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ",
        "text": "سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "note": "كلمتان خفيفتان على اللسان، ثقيلتان في الميزان، حبيبتان إلى الرحمن.",
    },
    {
        "title": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ",
        "text": "سُبْحَانَ اللَّهِ الْعَظِيمِ وَبِحَمْدِهِ",
        "note": "من قالها في يوم مائة مرة حطت خطاياه وإن كانت مثل زبد البحر.",
    },
    {
        "title": "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
        "text": "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ",
        "note": "كنز من كنوز الجنة.",
    },
    {
        "title": "سُبْحَانَ اللَّهِ، وَالْحَمْدُ لِلَّهِ، وَلَا إِلَهَ إِلَّا اللَّهُ، وَاللَّهُ أَكْبَرُ",
        "text": (
            "الباقيات الصالحات: سُبْحَانَ اللَّهِ، وَالْحَمْدُ لِلَّهِ، وَلَا"
            " إِلَهَ إِلَّا اللَّهُ، وَاللَّهُ أَكْبَرُ."
        ),
        "note": "هن أحب الكلام إلى الله وأفضله.",
    },
    {
        "title": "لَا إِلَهَ إِلَّا اللَّه وحدَهُ لَا شَرِيكَ لَهُ",
        "text": (
            "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ"
            " وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ."
        ),
        "note": "من قالها عشر مرات كان كمن أعتق أربعة أنفس من ولد إسماعيل.",
    },
    {
        "title": "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ وَأَتُوبُ إِلَيْهِ",
        "text": (
            "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ الَّذِي لَا إِلَهَ إِلَّا هو"
            " الحَيُّ القيوم وأتوب إليه."
        ),
        "note": "من لزم الاستغفار جعل الله له من كل هم فرجاً.",
    },
    {
        "title": "الصَّلَاةُ عَلَى النَّبِيِّ ﷺ",
        "text": (
            "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِينَا مُحَمَّدٍ وَعَلَى آله وصحب"
            " أجمعين."
        ),
        "note": "من صلى علي صلاة صلى الله عليه بها عشراً.",
    },
    {
        "title": "سَيِّدُ الِاسْتِغْفَارِ",
        "text": (
            "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا"
            " عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ..."
        ),
        "note": "من قالها موقناً بها ومات من ليله دخل الجنة.",
    },
    {
        "title": "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ",
        "text": (
            "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ"
            " رَبُّ الْعَرْشِ الْعَظِيمِ."
        ),
        "note": "من قالها كفاه الله ما أهمه من أمر الدنيا والآخرة.",
    },
]


# مهمة تلقائية لإرسال الأذكار كل ساعة
@tasks.loop(hours=1)
async def send_random_zekr():
  channel = bot.get_channel(ZEKR_CHANNEL_ID)
  if channel:
    zekr = random.choice(AZKAR_LIST)

    embed = discord.Embed(
        title=f"✨ {zekr['title']} ✨",
        description=f"📖 **الذكر:**\n{zekr['text']}\n\n💬 **الفضل:**\n{zekr['note']}",
        color=0x00FFCC,
    )
    embed.set_footer(
        text="تذكير تلقائي بالأذكار • اجعل لسانك رطباً بذكر الله 🤍"
    )

    await channel.send(embed=embed)


@send_random_zekr.before_loop
async def before_send_zekr():
  await bot.wait_until_ready()


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name} - Zekr Bot is Online!")
  if not send_random_zekr.is_running():
    send_random_zekr.start()


# أمر يدوي `/zekr` لإرسال ذكر فوراً عند الحاجة
@bot.tree.command(name="zekr", description="إرسال ذكر عشوائي فوراً في الروم")
async def slash_zekr(interaction: discord.Interaction):
  zekr = random.choice(AZKAR_LIST)

  embed = discord.Embed(
      title=f"✨ {zekr['title']} ✨",
      description=f"📖 **الذكر:**\n{zekr['text']}\n\n💬 **الفضل:**\n{zekr['note']}",
      color=0x00FFCC,
  )
  embed.set_footer(text=f"بواسطة: {interaction.user.display_name}")

  await interaction.channel.send(embed=embed)
  await interaction.response.send_message(
      "✅ تم إرسال الذكر بنجاح!", ephemeral=True
  )


# تشغيل البوت
keep_alive()
TOKEN = os.environ.get("ZEKR_TOKEN")
bot.run(TOKEN)
