#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pulp

# Define tasks
tasks = {
    "A": [],
    "B": [],
    "C": ["A"],
    "D1": ["A"],
    "D2": ["D1"],
    "D3": ["D1"],
    "D4": ["D2", "D3"],
    "D5": ["D4"],
    "D6": ["D4"],
    "D7": ["D6"],
    "D8": ["D5", "D7"],
    "E": ["B", "C"],
    "F": ["D8", "E"],
    "G": ["A", "D8"],
    "H": ["F", "G"]
}

# Task durations for best case, expected, and worst case in hours
task_durations = {
    "A": {"best": 4, "expected": 5, "worst": 6},
    "B": {"best": 8, "expected": 10, "worst": 12},
    "C": {"best": 4, "expected": 5, "worst": 6},
    "D1": {"best": 8, "expected": 10, "worst": 12},
    "D2": {"best": 16, "expected": 20, "worst": 24},
    "D3": {"best": 20, "expected": 25, "worst": 30},
    "D4": {"best": 24, "expected": 30, "worst": 36},
    "D5": {"best": 16, "expected": 20, "worst": 24},
    "D6": {"best": 20, "expected": 25, "worst": 30},
    "D7": {"best": 24, "expected": 30, "worst": 36},
    "D8": {"best": 12, "expected": 15, "worst": 18},
    "E": {"best": 16, "expected": 20, "worst": 24},
    "F": {"best": 4, "expected": 5, "worst": 6},
    "G": {"best": 12, "expected": 15, "worst": 18},
    "H": {"best": 8, "expected": 10, "worst": 12}
}


# In[2]:


hourly_rate = 55  # Hourly rate of employees


# In[3]:


# Create LP problem
prob = pulp.LpProblem("Scheduling", pulp.LpMinimize)


# In[4]:


# Define decision variables
start_time = {task: {scenario: pulp.LpVariable(f"Start_Time_{task}_{scenario}", lowBound=0, cat='Continuous') 
                     for scenario in ["best", "expected", "worst"]} for task in tasks}
end_time = {task: {scenario: pulp.LpVariable(f"End_Time_{task}_{scenario}", lowBound=0, cat='Continuous') 
                   for scenario in ["best", "expected", "worst"]} for task in tasks}


# In[5]:


# Define objective function 
prob += pulp.lpSum((end_time["H"][scenario] - start_time["H"][scenario]) * hourly_rate for scenario in ["best", "expected", "worst"])


# In[6]:


# Add constraints for each scenario
for task in tasks:
    for pred_task in tasks[task]:
        for scenario in ["best", "expected", "worst"]:
            prob += end_time[pred_task][scenario] <= start_time[task][scenario]
    for scenario in ["best", "expected", "worst"]:
        prob += end_time[task][scenario] - start_time[task][scenario] == task_durations[task][scenario]


# In[7]:


# Solve 
prob.solve()

# Print results 
for scenario in ["best", "expected", "worst"]:
    print(f"Optimal Schedule ({scenario} case):")
    total_cost = 0
    for task in tasks:
        duration = task_durations[task][scenario]
        cost = duration * hourly_rate
        total_cost += cost
        print(f"{task}: Start Time = {start_time[task][scenario].varValue}, End Time = {end_time[task][scenario].varValue}, Cost = {cost}")

    print(f"Total project cost ({scenario} case):", total_cost)

