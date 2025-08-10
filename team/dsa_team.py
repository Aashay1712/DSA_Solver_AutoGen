from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.code_executor_agent import get_code_executor_agent
from agents.problem_solver import get_problem_solver_agent
from config.constants import MAX_TURNS, TEXT_MENTION
    
problem_solver_agent = get_problem_solver_agent()
code_executor_agent, docker = get_code_executor_agent()
termination_condition = TextMentionTermination(TEXT_MENTION)

    
def get_dsa_team():

    
    team = RoundRobinGroupChat(
        participants=[problem_solver_agent,code_executor_agent],
        termination_condition=termination_condition,
        max_turns=MAX_TURNS
    )
    return team,docker