from os import getenv
from dotenv import load_dotenv
from pyrogram import Client
from asyncio import run
import json

import NBA
import futebol

load_dotenv()

app = Client(
    'Mediasesportivas_bot',
    api_id = getenv('TELEGRAM_APP_ID'),
    api_hash = getenv('TELEGRAM_API_HASH'),
    bot_token = getenv('TELEGRAM_BOT_TOKEN')
)

def formataBasquete(lista):
    return f'{lista[0]} x {lista[1]} \nData: {lista[2]} \nMedia de pontos: {lista[3]} \n'

def formataFutebol(lista):
    return f'{lista[0]} x {lista[1]} \nData: {lista[2]} \nMedia de Gols: {lista[3]} \n'

async def main():
    user1 = 'Libianno'
    user2 = 'wellingtonloki'
    #user2 = 'pitbulldaCC'

    liga, jogos = NBA.main()
    #strJogos = json.dumps(matches, indent=2)
    strJogos = '\n'.join([formataBasquete(jogo) for jogo in jogos])

    await app.start()
    await app.send_message(user1, liga)
    await app.send_message(user1, strJogos)
    
    await app.send_message(user2, liga)
    await app.send_message(user2, strJogos)

    run = futebol.main()
    try:
        while 1:

            liga, rodada, jogos = next(run)
            #strJogos = json.dumps(matches, indent=2)
            strJogos = '\n'.join([formataFutebol(jogo) for jogo in jogos])

            await app.send_message(user1, liga)
            await app.send_message(user1, rodada)
            await app.send_message(user1, strJogos)

            await app.send_message(user2, liga)
            await app.send_message(user2, rodada)
            await app.send_message(user2, strJogos)

    except StopIteration:
        pass

    await app.stop()

run(main())

