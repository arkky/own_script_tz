from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json
import random
import asyncio


# в constants.json содержатся команды и цвета. использовав этот файл, можно легко добавить новые команды/цвета без дополнительного изменения кода
with open("constants.json", "rb") as f:
    constants = json.load(f)


# Инициализация экземпляра класса FastAPI
app = FastAPI()


# Создаю вебсокет на эндпоинте ws, получаю подлючение от клиентской части и отправляю им по очереди команды фонаря
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Принимаем новое подключение
    await websocket.accept()
    try:
        # Заранее определяем цвет, который будет отправлять сервер
        color = random.choice(constants['colors'])
        for command in constants['commands']:
            # Использовал тернарное выражение для добавление цвета, если команда COLOR, в противном случае пустая строка
            data = {"command": command, "metadata": (color if command == "COLOR" else "")} 
            # Сериализирую словарь в json, а затем кодирую в байты по кодировке utf-8
            bytes_data = json.dumps(data).encode('utf-8')
            await websocket.send_bytes(bytes_data)
            # точно знаю, что получу какой-то ответ от клиента и поэтому жду сообщение от него
            recv_data = await websocket.receive_text()
            print(recv_data)
        # после 5 секунд соединение с сервером успешно разорвётся
        await asyncio.sleep(5)
    # Обрабатываю отключение от вебсокета
    except WebSocketDisconnect:
        print("Connection was closed")
    # Если произошла неизвестная ошибка, то просто принтую её название
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # запуск сервера FastAPI через uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=9999, log_level="info", reload=True)