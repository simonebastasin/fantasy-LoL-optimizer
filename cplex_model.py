from pyomo.environ import *


# 1st Model: pyomo -> CPLEX


def cap_salary_rule(model):
    return sum(model.Weights[i] * model.x[i] for i in model.Items) <= model.SalaryCap


def cap_players_rule(model):
    return sum(model.x[i] for i in model.Items) == model.RolesCap


def cap_roles_rule(model):
    return sum(model.Roles[i] * model.x[i] for i in model.Items) == 111111


def build_model(n, budget, limit_roles, roles, points, weights):
    # Model
    model = ConcreteModel()
    # sets
    model.Items = RangeSet(0, n-1)
    # params
    model.Roles = Param(model.Items, initialize=lambda model, j: roles[j])
    model.Profits = Param(model.Items, initialize=lambda model, j: points[j])
    model.Weights = Param(model.Items, initialize=lambda model, j: weights[j])
    model.SalaryCap = budget
    model.RolesCap = limit_roles
    # variables
    model.x = Var(model.Items, domain=Boolean)
    # objective
    model.obj = Objective(expr = sum(model.Profits[i] * model.x[i] for i in model.Items), sense=maximize)
    # constraints
    model.cap_sal = Constraint(rule=cap_salary_rule)
    model.cap_ply = Constraint(rule=cap_players_rule)
    model.cap_rol = Constraint(rule=cap_roles_rule)
    return model


# 2nd Model: pyomo -> CPLEX


def cap_points_rule(model):
    return sum(model.Profits[i] * model.x[i] for i in model.Items) <= model.PointsCap


def build_model_2(n, budget, limit_roles, roles, points, weights, temp_points):
    # Model
    model = build_model(n, budget, limit_roles, roles, points, weights)
    # another param
    model.PointsCap = temp_points - 0.001
    # another constraint
    model.cap_pts = Constraint(rule=cap_points_rule)
    return model
