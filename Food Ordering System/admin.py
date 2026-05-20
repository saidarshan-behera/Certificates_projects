from pulp import LpProblem, LpMaximize, LpVariable, LpStatus, value

# Create a linear programming problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision Variables
A = LpVariable('A', lowBound=0, cat='Continuous')  # Quantity of Product A
B = LpVariable('B', lowBound=0, cat='Continuous')  # Quantity of Product B

# Objective Function: Maximize z = 40A + 30B
problem += 40 * A + 30 * B, "Total_Profit"

# Constraints
problem += 2 * A + B <= 100, "Labor_Constraint"  # Labor constraint
problem += A + 2 * B <= 80, "Material_Constraint"  # Material constraint

# Solve the problem
problem.solve()

# Output the results
print(f"Status: {LpStatus[problem.status]}")
print(f"Optimal quantity of Product A: {value(A):.2f}")
print(f"Optimal quantity of Product B: {value(B):.2f}")
print(f"Maximum Profit: {value(problem.objective):.2f}")