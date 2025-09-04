from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks

app = FastAPI()

# Store connected clients
clients = []

# Background task: log messages
def log_message(message: str):
    with open("chat_log.txt", "a") as f:
        f.write(message + "\n")

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket, bg: BackgroundTasks):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            # Receive a message
            data = await websocket.receive_text()

            # Log the message in background
            bg.add_task(log_message, data)

            # Broadcast message to all clients
            for client in clients:
                if client != websocket:
                    await client.send_text(f"User said: {data}")

    except WebSocketDisconnect:
        clients.remove(websocket)