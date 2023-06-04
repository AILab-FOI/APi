from uuid import uuid4

"""
Gets operator of an agent (operator is non-alphabetic char that follows the agent specification)
"""
def get_agent_operator(remaining_sequence):
    if len(remaining_sequence) > 0 and len(remaining_sequence[0]) == 1 and not remaining_sequence[0].isalpha():
        return remaining_sequence[0]

    return None

"""
Getting the next agent from the current one (so that we know which are dependant ones)
"""
def get_next_agent(remaining_sequence):
    if len(remaining_sequence) > 0 and remaining_sequence[0].isidentifier():
        return remaining_sequence[0]
    elif len(remaining_sequence) > 1 and remaining_sequence[1].isidentifier():
        return remaining_sequence[1]

    return None

"""
Resolving execution plan expression -> finding agents, their dependencies, and operators
"""
def get_agents_and_operations(sequence_args):
    sequence, args = sequence_args
    # sequence_split = list(sequence)
    sequence_split = sequence.split(" ")
    agents = {}

    i = 0

    curr_id = uuid4().hex
    next_id = None
    while i < len(sequence_split):
        curr_agent = sequence_split[i]
        operator = get_agent_operator(sequence_split[i+1:])
        next_agent = get_next_agent(sequence_split[i+1:])
        if next_agent:
            next_id = uuid4().hex
        
        if operator:
            i += 2
        else:
            i += 1

        args_by_agent = args.get(curr_agent, None)
        agent_args = args_by_agent.pop(0) if args_by_agent is not None else None

        agent = {
            'id': curr_id,
            'name': curr_agent,
            'operator': operator,
            'succeeding_agent_id': next_id,
            'status': 'ready_to_start',
            'args': agent_args
        }

        agents[curr_id] = agent

        if next_id:
            curr_id = next_id
        else:
            curr_id = uuid4().hex
        next_id = None

    return agents

"""
Finding out what are the initial agents that need to be run
"""
def get_initial_agents_to_run(parallel_flows):
    return [list(flow.keys())[0] for flow in parallel_flows]

def extract_brackets(flow):
    brackets = []

    arg_list_start_index = None
    for i in range(0, len(flow)):
        curr_c = flow[i]
        prev_c = flow[i - 1] if i > 0 else None

        if curr_c == "(":
            if prev_c == " " or prev_c is None:
                brackets.append(i)
            else:
                arg_list_start_index = i
        elif curr_c == ")":
            if arg_list_start_index:
                brackets.append((arg_list_start_index, i))
                arg_list_start_index = None
            else:
                brackets.append(i)

    return brackets

def extract_args(flow, brackets):
    args_by_agent = {}
    for brackets_pair in brackets:
        if type(brackets_pair) != tuple:
            continue
        
        start, end = brackets_pair
        start_index = start - 1
        
        while start_index >= 0:
            c = flow[start_index]
            if c == " ":
                start_index = start_index + 1
                break

            start_index = start_index - 1

        start_index = max(start_index, 0)

        name = flow[start_index:start]
        args_str = flow[start+1:end]
        args = args_str.split(" ")
        
        if name not in args_by_agent:
            args_by_agent[name] = []    

        args_by_agent[name].append(args)

    return args_by_agent

def clean_up_flow(flow, brackets):
    new_flow = flow
    removed_chars = 0
    for brackets_pair in brackets:
        if type(brackets_pair) == tuple:
            start, end = brackets_pair
            new_flow = new_flow[:start-removed_chars] + new_flow[end-removed_chars+1:]
            removed_chars = removed_chars + (end - start + 1)
        else:
            start = brackets_pair
            new_flow = new_flow[:start-removed_chars] + new_flow[start-removed_chars+1:]
            removed_chars = removed_chars + 1

    return new_flow

def extract_args_and_clean_up(flow):
    brackets = extract_brackets(flow)
    args_by_agent = extract_args(flow, brackets)
    new_flow = clean_up_flow(flow, brackets).strip()
    
    return new_flow, args_by_agent


"""
Converting execution plan
"""
def resolve_execution_plan(execution_plan):
    # find out paralel flows
    parallel = execution_plan.split('|')
    
    # trim and remove unused chars
    cleaned_exp = [extract_args_and_clean_up(exp) for exp in parallel]

    # resolve agents and operations
    parallel_flows = [get_agents_and_operations(item) for item in cleaned_exp]

    # get initial agents to run
    initial_agents = get_initial_agents_to_run(parallel_flows)

    # flattening all agents across different parallel flows into a high-level map (no nesting)
    agents = {}
    for flow in parallel_flows:
        agents = {**agents, **flow}

    return {"id": uuid4().hex, "plan": agents, "initial_agents_to_run": initial_agents, "started": False}

# execution_plans = ['bla_file_stdout bla_file_stdout']
# execution_plans = ['bla_file_stdout(c) bla_file_stdout(c)']
# execution_plans = ['a(c a) a(b r) | (b c)']
# execution_plans_resolved = [resolve_execution_plan(plan) for plan in execution_plans]
# print(execution_plans_resolved)

"""
Getting execution plan by id
"""
def get_execution_plan_by_id(plan_id):
    for p_id, agents, i_agents in execution_plans_resolved:
        if p_id == plan_id:
            return (p_id, agents, i_agents)

    return None

"""
Update agent status
"""
def set_agent_status(plan_id, agent_id, status):
    execution_plan = get_execution_plan_by_id(plan_id)
    if execution_plan:
        _, agents, _ = execution_plan
        agents[agent_id]['status'] = status

"""
Start agent
"""
def start_agent(plan_id, agent_id):
    set_agent_status(plan_id, agent_id, "started")

"""
Start execution plans
"""
def start_execution_plans(execution_plans):
    for plan_id, agents, initial_agents in execution_plans:
        for a_id in initial_agents:
            start_agent(plan_id, a_id)

# start_execution_plans(execution_plans_resolved)
# print(execution_plans_resolved)

"""
Agent has finished up
"""
def agent_finished(plan_id, agent_id, status_code):
    execution_plan = get_execution_plan_by_id(plan_id)
    if execution_plan:
        _, agents, _ = execution_plan
        agent = agents[agent_id]
        operator = agent['operator']
        succeeding_a_id = agent['succeeding_agent_id']

        agent['status'] = 'finished'
        if succeeding_a_id:
            # succeeding agent is free to start no matter the status code
            if not operator or (operator == "&" and status_code == 1) or (operator == "!" and status_code == 0):
                start_agent(plan_id, succeeding_a_id)
            elif operator == "+":
                start_agent(plan_id, agent_id)

# for plan_id, agents, initial_agents in execution_plans_resolved:
#     for a_id in initial_agents:
#         agent_finished(plan_id, a_id, 105)

# print(execution_plans_resolved)