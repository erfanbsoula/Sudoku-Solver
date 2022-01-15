import pulp as lp

rows = range(0,9)
cols = range(0,9)
values = range(1,10)
grids = range(0,9)

# get prefilled cell values from user
input_sudoku = [[0 for col in cols] for row in rows]
prefilled_count = int(input())
for _ in range(prefilled_count):
    buffer = input().split()
    value = int(buffer[0])
    row = int(buffer[1]) - 1
    col = int(buffer[2]) - 1
    input_sudoku[row][col] = value

# initialize the linear programming problem
problem = lp.LpProblem("Sudoku")
objective = lp.lpSum(0)
problem.setObjective(objective)

# if sudoku[row][col] == value => grid_vars[row][col][value] = 1
grid_vars = lp.LpVariable.dicts("grid_value", (rows,cols,values), cat='Binary')
# grid_vars[row][col][value] represents the existance of a number with given value
# in the cell at the [row][col] position

# constraint 1: only one value for each cell
for row in rows:
    for col in cols:
        problem.addConstraint(
            lp.LpConstraint(
                e=lp.lpSum([grid_vars[row][col][value] for value in values]),
                sense=lp.LpConstraintEQ, rhs=1
            )
        )

# constraint 2: each number is used only once in a row
for row in rows:
    for value in values:
        problem.addConstraint(
            lp.LpConstraint(
                e=lp.lpSum([grid_vars[row][col][value] for col in cols]),
                sense=lp.LpConstraintEQ, rhs=1
            )
        )

# constraint 3: each number is used only once in a column
for col in cols:
    for value in values:
        problem.addConstraint(
            lp.LpConstraint(
                e=lp.lpSum([grid_vars[row][col][value] for row in rows]),
                sense=lp.LpConstraintEQ, rhs=1
            )
        )

# constraint 4: each number is used only once in the 3x3 grid
for grid in grids:
    grid_row  = int(grid/3)
    grid_col  = int(grid%3)

    for value in values:
        problem.addConstraint(
            lp.LpConstraint(
                e=lp.lpSum(
                    [grid_vars[grid_row*3+row][grid_col*3+col][value]
                    for col in range(0,3) for row in range(0,3)]
                ),
                sense=lp.LpConstraintEQ, rhs=1
            )
        )

# set the prefilled values from input sudoku as constraints
for row in rows:
    for col in cols:
        if(input_sudoku[row][col] != 0):
            problem.addConstraint(
                lp.LpConstraint(
                    e=lp.lpSum([grid_vars[row][col][value]*value  for value in values]),
                    sense=lp.LpConstraintEQ, rhs=input_sudoku[row][col]
                )
            )
# lp.LpConstraintEQ means that the sum of every variable of the given array
# to the lp.lpSum(), form an "equality" that equals to 1 (right hand side)

problem.solve(lp.PULP_CBC_CMD(msg=0))
print(f'\nSolution Status = {lp.LpStatus[problem.status]}')

# extract solution to a simple array
solution = [[0 for col in cols] for row in rows]
for row in rows:
    for col in cols:
        for value in values:
            if lp.value(grid_vars[row][col][value]):
                solution[row][col] = value

# print the sudoku solution in agrid
print("\n+ ------- + ------- + ------- +", end='')
for row in rows:
    print("\n| ", end='')
    for col in cols:
        num_end = " | " if ((col+1)%3 == 0) else "  "
        print(solution[row][col], end=num_end)
    if ((row+1)%3 == 0):
        print("\n+ ------- + ------- + ------- +", end='')

print('\n')
