import asyncio
import websockets
import json
from crewai import Agent, LLM, Crew, Process, Task

ollama=LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434")

atendimento = Agent(
    role="Especialista em atendimento online",
    llm=ollama,
    verbose=True,
    goal="Fornecer suporte detalhado e eficiente aos clientes que entram em contato via chat ou formulário",
    backstory="Você é um especialista em atendimento online, com foco em atendimento cordial, eficiente e personalizado. Conhece práticas de suporte ao cliente, resolução de dúvidas e orientação sobre produtos ou serviços."
)

task_atendimento = Task(
    description="""
    Responda às mensagens do cliente de forma clara e profissional. 
    Coleta informações necessárias para resolver o problema do cliente, 
    forneça instruções detalhadas ou encaminhe o caso para o setor apropriado, 
    se necessário.
    Nome do usuário: {user_name}
    Mensagem: {message}
    """,
    expected_output="Resposta do usuário",
    agent=atendimento
)

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        print(data)

        user_message = data.get("message", "")
        user_number = data.get("user_number", "")
        user_name = data.get("user_name", "")
        historico = data.get("historico", "")

        print(user_name)
        
        equipe = Crew(
            agents=[atendimento],
            tasks=[task_atendimento],
            process= Process.sequential
        )

        resultado = equipe.kickoff(inputs={
            'message': user_message,
            'user_number': user_number,
            'user_name': user_name,
            'historico': historico,
        })

        resposta_texto = str(resultado)

        """ # envia apenas string via websocket
        await websocket.send(resposta_texto) """

        await websocket.send(json.dumps({"response": str(resultado), "number": user_number}))
        

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket rodando em ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
