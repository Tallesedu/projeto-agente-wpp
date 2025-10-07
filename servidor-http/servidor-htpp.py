from fastapi import FastAPI, Request
import websockets
import json
import uvicorn

app = FastAPI()
WS_URL = "ws://localhost:8765"

@app.post("/send_message")
async def send_message(request: Request):
    data = await request.json()
    print("Data recebida:", data)
    
    historico = data.get("historico", [])
    historico_formatado = json.dumps(historico, ensure_ascii=False, indent=2)
    user_message = data.get("message", "")
    user_number = data.get("user_number", "")
    user_name = data.get("user_name", "")
    
    print(f"Nome: {user_name}, Número: {user_number}, Mensagem: {user_message}")

    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps({
            "message": user_message,
            "user_number": user_number,
            "user_name": user_name,
            "historico": historico_formatado
        }))
        response = await ws.recv()
        print("Resposta do CrewAI:", response)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
