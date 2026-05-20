import pulp

# Maximization problem
print("Maximization Problem:")
lp_max_problem = pulp.LpProblem("Maximize_Z", pulp.LpMaximize)

# Define decision variables
x_max = pulp.LpVariable('x_max', lowBound=0, cat='Continuous')
y_max = pulp.LpVariable('y_max', lowBound=0, cat='Continuous')

# Objective function
lp_max_problem += 3 * x_max + 2 * y_max, "Objective_Function"

# Constraints
lp_max_problem += x_max + y_max <= 4, "Constraint_1"
lp_max_problem += 2 * x_max + y_max <= 5, "Constraint_2"

# Solve the maximization problem
lp_max_problem.solve()

# Output the maximization results
print(f"Status: {pulp.LpStatus[lp_max_problem.status]}")
print(f"x_max = {x_max.varValue}")
print(f"y_max = {y_max.varValue}")
print(f"Objective function value: {pulp.value(lp_max_problem.objective)}\n")

# Minimization problem
print("Minimization Problem:")
lp_min_problem = pulp.LpProblem("Minimize_Z", pulp.LpMinimize)

# Define decision variables
x_min = pulp.LpVariable('x_min', lowBound=0, cat='Continuous')
y_min = pulp.LpVariable('y_min', lowBound=0, cat='Continuous')

# Objective function
lp_min_problem += 3 * x_min + 2 * y_min, "Objective_Function"

# Constraints
lp_min_problem += x_min + y_min <= 4, "Constraint_1"
lp_min_problem += 2 * x_min + y_min <= 5, "Constraint_2"

# Solve the minimization problem
lp_min_problem.solve()

# Output the minimization results
print(f"Status: {pulp.LpStatus[lp_min_problem.status]}")
print(f"x_min = {x_min.varValue}")
print(f"y_min = {y_min.varValue}")
print(f"Objective function value: {pulp.value(lp_min_problem.objective)}")
