import asyncio
from team.dsa_team import get_dsa_team
from config.docker_utils import start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

team,docker = get_dsa_team()




async def main():
    
    try:
        await start_docker_container(docker)
        print("Docker container started successfully.")


        task = "write a python code to add two numbers"

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print("=="*20)
                print(message.source, ":" ,message.content)
            elif isinstance(message, TaskResult):
                print("Stop Reason", message.stop_reason)
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await stop_docker_container(docker)

if __name__ == "__main__":
    asyncio.run(main())
                        
    

