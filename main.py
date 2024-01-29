from pulp import *

from part import Part

Names = [
    "Shark",
    "Unkiu",
    "Whale",
    "Coelacanth",
    "Syldra",
    "MShark",
    "MUnkiu",
    "MWhale",
    "MCoelacanth",
    "MSyldra"
]
Types = [
    "Hull",
    "Stern",
    "Bow",
    "Bridge"
]
Parts = [
    [ # Shark
        Part(-10, 30, 20, 40, 20, 5),
        Part(-30, 20, 60, 30, 15, 5),
        Part(50, 40, 10, -20, 15, 5),
        Part(20, 20, 20, 20, 20, 5)
    ],
    [ # Unkiu
        Part(15, 10, 0, 60, 15, 9),
        Part(15, 0, 30, 40, 25, 9),
        Part(60, 20, 20, -15, 10, 9),
        Part(25, 5, 25, 30, 30, 9),
    ],
    [ # Whale
        Part(-15, 55, 35, 15, 20, 12),
        Part(15, 20, 0, 55, 15, 12),
        Part(25, 60, -15, 20, 15, 12),
        Part(0, 25, 20, 45, 40, 12),
    ],
    [ # Coelacanth
        Part(40, -10, 25, 40, 25, 14),
        Part(10, 25, 35, 25, 25, 14),
        Part(65, 10, -10, 30, 0, 14),
        Part(55, 20, 35, -15, 50, 14),
    ],
    [ # Syldra
        Part(10, 75, 30, -15, 5, 17),
        Part(20, 60, 35, -15, 5, 17),
        Part(45, 30, -15, 40, 40, 17),
        Part(55, 20, -5, 30, 60, 17)
    ],
    [ # M-Shark
        Part(-5, 40, 25, 45, 35, 20),
        Part(-25, 25, 70, 35, 25, 20),
        Part(55, 50, 15, -15, 25, 20),
        Part(25, 25, 30, 25, 35, 20)
    ],
    [ # M-Unkiu
        Part(20, 15, 5, 65, 25, 20),
        Part(20, 5, 35, 45, 35, 20),
        Part(65, 25, 25, -10, 20, 20),
        Part(30, 10, 30, 35, 40, 20),
    ],
    [ # M-Whale
        Part(-10, 55, 40, 20, 30, 20),
        Part(20, 20, 5, 65, 20, 20),
        Part(25, 65, -10, 25, 25, 20),
        Part(0, 30, 25, 50, 45, 20),
    ],
    [ # M-Coelacanth
        Part(40, -5, 30, 40, 30, 20),
        Part(10, 25, 40, 30, 30, 20),
        Part(70, 15, -10, 30, 5, 20),
        Part(60, 20, 35, -10, 55, 20),
    ],
    [ # M-Syldra
        Part(10, 80, 30, -15, 10, 20),
        Part(20, 60, 35, -10, 10, 20),
        Part(45, 30, -10, 40, 40, 20),
        Part(60, 20, -5, 30, 60, 20)
    ]
]
Parts = makeDict([Names, Types], Parts, 0)

problem = LpProblem('Submarine_optimization', LpMaximize)

base_surveillance = 0
base_retrieval = 0
base_speed = 0
base_range = 0
base_favor = 0

capacity = 43

target_surveillance = 0
target_retrieval = 0
target_speed = 0
target_range = 0
target_favor = 0

weight_surveillance = 5
weight_retrieval = 1
weight_speed = 10
weight_range = 5
weight_favor = 1

Combinations = [(n, t) for n in Names for t in Types]

variables = LpVariable.dicts("Part", (Names, Types), 0, 1, LpInteger)

problem += (
    lpSum([(weight_surveillance * variables[n][t] * Parts[n][t].surveillance) +
           (weight_retrieval * variables[n][t] * Parts[n][t].retrieval) +
           (weight_speed * variables[n][t] * Parts[n][t].speed) +
           (weight_range * variables[n][t] * Parts[n][t].range) +
           (weight_favor * variables[n][t] * Parts[n][t].favor) for (n, t) in Combinations]
          ),
    "Sum_of_stats"
)

for t in Types:
    problem += (
        lpSum([variables[n][t] for n in Names]) == 1,
        f"Only_one_part_per_category_{t}"
    )

problem += (
    lpSum([variables[n][t] * Parts[n][t].surveillance for n in Names for t in
           Types]) + base_surveillance >= target_surveillance,
    "Target_surveillance"
)
problem += (
    lpSum([variables[n][t] * Parts[n][t].retrieval for n in Names for t in Types]) + base_retrieval >= target_retrieval,
    "Target_retrieval"
)
problem += (
    lpSum([variables[n][t] * Parts[n][t].speed for n in Names for t in Types]) + base_speed >= target_speed,
    "Target_speed"
)
problem += (
    lpSum([variables[n][t] * Parts[n][t].range for n in Names for t in Types]) + base_range >= target_range,
    "Target_range"
)
problem += (
    lpSum([variables[n][t] * Parts[n][t].favor for n in Names for t in Types]) + base_favor >= target_favor,
    "Target_favor"
)
problem += (
    lpSum([variables[n][t] * Parts[n][t].cost for n in Names for t in Types]) <= capacity,
    "Capacity_limiter"
)

# The problem is solved using PuLP's choice of Solver
problem.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[problem.status])

final_surveillance = base_surveillance
final_retrieval = base_retrieval
final_speed = base_speed
final_range = base_range
final_favor = base_favor
final_cost = 0

hull = ''
stern = ''
bow = ''
bridge = ''

# Each of the variables is printed with it's resolved optimum value
for v in problem.variables():
    if v.varValue == 1:
        n, t = v.name.replace("Part_", "").split("_")
        final_surveillance += Parts[n][t].surveillance
        final_retrieval += Parts[n][t].retrieval
        final_speed += Parts[n][t].speed
        final_range += Parts[n][t].range
        final_favor += Parts[n][t].favor
        final_cost += Parts[n][t].cost

        if 'Hull' == t:
            hull = n
        elif 'Stern' == t:
            stern = n
        elif 'Bow' == t:
            bow = n
        elif 'Bridge' == t:
            bridge = n

        # print(v.name)
    # print(v.name, "=", v.varValue)

print("\nFinal stats")
print(f"Surveillance {final_surveillance}")
print(f"Retrieval {final_retrieval}")
print(f"Speed {final_speed}")
print(f"Range {final_range}")
print(f"Favor {final_favor}")
print(f"Cost {final_cost}")
print(f"\n| {'hull':^12} | {'stern':^12} | {'bow':^12} | {'bridge':^12} |")
print(f"| {hull:^12} | {stern:^12} | {bow:^12} | {bridge:^12} |")
