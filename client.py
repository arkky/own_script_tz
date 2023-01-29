import websockets
import asyncio
import json
import argparse
from websockets.exceptions import ConnectionClosedOK


# в constants.json содержатся команды и цвета. использовав этот файл, можно легко добавить новые команды/цвета без дополнительного изменения кода
with open("constants.json", "rb") as f:
    constants = json.load(f)


# подключение к серверу FastAPI через вебсокеты
async def client():
    async with websockets.connect(f"ws://{args.host}:{args.port}/ws") as ws:
        while True:
            try:
                # получаю байты от сервера и декодирую их
                data = await ws.recv()
                data = json.loads(data.decode('utf-8'))
                print("Recieved:", data)
                if data:
                    if data['command'] in constants['commands']:
                        # поскольку я не знаю какие ответы точно отправлять обратно, просто заранее описал текстом каждую команду
                        message = constants['commands'][data['command']]
                        await ws.send(message)
                        print("Sended:", message)
                        print("---"*17)
            # Обрабатываю отключение от сервера
            except ConnectionClosedOK:
                break


if __name__ == "__main__":
    # добавляю аргументы
    parser = argparse.ArgumentParser(description="Example: python3 client.py --host 127.0.0.1 --port 9999")
    parser.add_argument("--host", help="Укажите HOST сервера")
    parser.add_argument("--port", help="Укажите порт сервера")
    args = parser.parse_args()

    # запускаю асинхронную функцию
    asyncio.run(client())
