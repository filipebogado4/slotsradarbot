import telebot
import datetime
import random
import threading
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= CONFIG =================

TOKEN = "8688917336:AAEk-s_6nndT7DdjJgkvu7oyA09Lb9K_kio"

BOT_LINK = "https://t.me/SlotsRadarpro_Bot"
CANAL = "@divulga_toppp"
PLATAFORMA = "https://aa888.news/?a=evtrfjic"

GAMES = [
"🐴 Fortune Horse",
"🛡 Mythical Guardians",
"♠ Poker Kingdom Win",
"🧪 Forbidden Alchemy",
"🐯 Fortune Tiger",
"🐰 Fortune Rabbit",
"🐲 Fortune Dragon",
"🐂 Fortune Ox",
"🐍 Fortune Snake",
"🐭 Fortune Mouse",
"💰 Cash Mania",
"💎 Fortune Gems 2",
"🏆 Mr Treasure's Fortune",
"💎 Fortune Gems",
"💵 Money Coming",
"🐷 Fortune Pig",
"🎉 Pinata Wins",
"🤠 Wild Bounty Showdown",
"🌵 Wild Bandito",
"💎 Fortune Gems 500",
"🐱 Lucky Neko",
"👑 Midas Fortune",
"🐆 Lucky Jaguar 2",
"⚡ Anubis Wrath",
"🍹 Cocktail Nights",
"🐉 Dragon Hatch",
"🐆 Lucky Jaguar",
"🍀 Double Fortune",
"🦜 Wings of Iguazu",
"🏺 Treasures of Aztec",
"🐲 Yo Dragon",
"🪙 Fortune Coins"
]

bot = telebot.TeleBot(TOKEN)

# ================= HORÁRIOS =================

ultimos_horarios = {}
ultimo_horario_final = {}

def gerar_horarios():
    agora = datetime.datetime.now()
    minutos = random.sample(range(60),5)
    horarios = []
    for m in minutos:
        hora = agora.hour
        if m < agora.minute:
            hora = (hora + 1) % 24
        horarios.append(f"{hora:02d}:{m:02d}")
    return sorted(horarios)

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):
    usuarios_fake = random.randint(900,1800)
    markup = InlineKeyboardMarkup(row_width=2)
    for jogo in GAMES:
        markup.add(InlineKeyboardButton(jogo, callback_data=jogo))
    texto = f"""
🎰 *GERADOR DE HORÁRIOS PAGANTES*

👥 {usuarios_fake} usuários online agora

Escolha um jogo abaixo para gerar os sinais.

⚠️ Aguarde os horários passarem para gerar novos.
"""
    bot.send_message(
        message.chat.id,
        texto,
        parse_mode="Markdown",
        reply_markup=markup
    )

# ================= JOGOS =================

@bot.callback_query_handler(func=lambda call: call.data in GAMES)
def jogo(call):
    jogo = call.data
    agora = datetime.datetime.now()
    if jogo in ultimo_horario_final:
        ultimo = ultimo_horario_final[jogo]
        hora_final = datetime.datetime.strptime(ultimo,"%H:%M").time()
        if agora.time() < hora_final:
            horarios = ultimos_horarios[jogo]
        else:
            horarios = gerar_horarios()
            ultimos_horarios[jogo] = horarios
            ultimo_horario_final[jogo] = horarios[-1]
    else:
        horarios = gerar_horarios()
        ultimos_horarios[jogo] = horarios
        ultimo_horario_final[jogo] = horarios[-1]

    jogadores = random.randint(40,80)

    texto = f"""
🔥 *Horários Pagantes*

🎮 {jogo}
"""
    for h in horarios:
        texto += f"⏰ `{h}`\n"

    texto += f"""

🔥 {jogadores} jogadores usando esse sinal agora

Boa sorte 🍀
"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "🚀 Ir para Plataforma",
            url=PLATAFORMA
        )
    )
    botoes = [InlineKeyboardButton(g, callback_data=g) for g in GAMES]
    for i in range(0,len(botoes),2):
        markup.add(*botoes[i:i+2])

    bot.send_message(
        call.message.chat.id,
        texto,
        parse_mode="Markdown",
        reply_markup=markup
    )

    bot.answer_callback_query(call.id)

# ================= WINS AUTOMÁTICOS =================

nomes = [
"João","Pedro","Lucas","Carlos","Bruno",
"Marcos","Felipe","Rafael","André","Thiago",
"Matheus","Gabriel","Ricardo"
]

def enviar_wins():
    while True:
        nome = random.choice(nomes)
        jogo = random.choice(GAMES)
        valor = random.randint(100,900)
        texto = f"""
🎉 *WIN CONFIRMADO*

👤 {nome}

🎮 {jogo}

💰 Ganhou R${valor}

👇 Gere seu horário agora
"""
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                "🎰 GERAR HORÁRIOS",
                url=BOT_LINK
            )
        )
        try:
            bot.send_message(
                CANAL,
                texto,
                parse_mode="Markdown",
                reply_markup=markup
            )
        except:
            pass
        time.sleep(random.randint(120,300))

threading.Thread(target=enviar_wins).start()

# ================= START BOT =================

print("Bot rodando...")
bot.infinity_polling()
