import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_agentchat.agents import AssistantAgent
from dotenv import load_dotenv
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",
    api_key=api_key
)



async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir="/tmp",
        timeout=120
    )

    code_executor_agent = CodeExecutorAgent(
        name = "CodeExecutor",
        code_executor=docker
    )
    problem_solver_agent = AssistantAgent(
        name = "DSA_problem_solver",
        description="An agent that solves DSA problems",
        model_client=model_client,
        system_message='''
        You are a problem solver agent that is an expert in solving DSA problems.
        You will be working with code executor agent to execute code.
        You will be given a task and you should.
        At the begining of your response you have to specify your plan to solve the task.
        Then you should give the code in a code block.(Python)
        You should write code in one code block at a time and the pass it to the code executor agent to execute it.
        Make sure to have atleast 3 test cases for the code you write.
        Once the code is executed and if the same has been done successfully, you have the results.
        You should explain the code execution result.

        I the end once the code is executed successfully. you have to say "STOP" to stop the conversation.
        '''
    )
    termination_condition = TextMentionTermination("STOP")
    team = RoundRobinGroupChat(
        participants=[problem_solver_agent,code_executor_agent],
        termination_condition=termination_condition,
        max_turns=10
    )
    
    try:
        await docker.start()
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
        await docker.stop()

if __name__ == "__main__":
    asyncio.run(main())
    


