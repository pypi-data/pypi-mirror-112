# Test whether pyMCFSimplex is installed correctly
from pyMCFSimplex import MCFSimplex, new_darray, darray_get

def test_mcf_simplex():
    mcf = MCFSimplex()
    mcf.LoadDMX(sample_dmx)
    mcf.SolveMCF()
    if mcf.MCFGetStatus() == 0:
        cost = mcf.MCFGetFO()
        assert cost == 9.0, "Optimal solution has cost 9"

        solution = get_solution(mcf)
        assert solution == [1.0, 1.0, 1.0, 2.0, 0.0]
    else:
        assert False, "No MCF solution found"


def get_solution(mcf: MCFSimplex):
    """
    Retrieve solution darray and turn into Python list
    """
    length = mcf.MCFm()
    solution = new_darray(length)
    mcf.MCFGetX(solution)
    return [darray_get(solution, i) for i in range(length)]


sample_dmx = """
c
c 'c' lines are comments
c 'p' line indicates problem type, amount of nodes, and amount of arcs
c
p min 5 5
c
c 'n' lines are node ids followed by their demands
c node ids go from 1 to <number of nodes>
c missing nodes get 0 demand
c
n 1 3
n 4 -3
c
c 'a' lines describe arcs / directed edges
c The amount of arcs lines must be exactly equal to the indicated amount of arcs
c An arc consists of start node, end node, min flow, max flow, cost
c
a 1 2 0 2 3
a 2 3 0 2 1
a 3 4 0 2 1
a 1 4 0 2 2
a 1 5 0 2 5
"""
