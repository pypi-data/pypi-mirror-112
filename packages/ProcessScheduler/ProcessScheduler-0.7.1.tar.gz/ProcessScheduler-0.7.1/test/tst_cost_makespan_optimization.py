import processscheduler as ps

problem = ps.SchedulingProblem("Excavator7:MultiObjectiveOptimization")

# three tasks
dig_small_hole = ps.VariableDurationTask("DigSmallHole", work_amount=3, priority=1)
dig_medium_hole = ps.VariableDurationTask("DigMediumHole", work_amount=7, priority=10)
dig_huge_hole = ps.VariableDurationTask("DigHugeHole", work_amount=15, priority=100)

# two workers
small_exc = ps.Worker(
    "SmallExcavator", productivity=4, cost=ps.ConstantCostPerPeriod(5)
)
medium_ex = ps.Worker(
    "MediumExcavator", productivity=6, cost=ps.ConstantCostPerPeriod(10)
)

dig_small_hole.add_required_resource(
    ps.SelectWorkers([small_exc, medium_ex], 1, kind="min")
)
dig_medium_hole.add_required_resource(
    ps.SelectWorkers([small_exc, medium_ex], 1, kind="min")
)
dig_huge_hole.add_required_resource(
    ps.SelectWorkers([small_exc, medium_ex], 1, kind="min")
)

problem.add_objective_makespan()
problem.add_objective_resource_cost([small_exc, medium_ex])
problem.add_objective_priorities()

solver = ps.SchedulingSolver(problem, optimize_priority="pareto")
solution = solver.solve()
solution.render_gantt_matplotlib()
