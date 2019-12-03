import numpy as np

from ctm import Edge

if __name__ == '__main__':
    edges = 5
    tau = 1
    v0 = 40
    p_m = 50
    m = 3
    q_a = 3000
    c = 5000
    c_nextk = 5000
    d_prevk = 10
    p_a = 40

    data = []

    iterations = []
    for i in range(12):
        print('Min:',i)

        edges_data = []
        for e in range(edges):

            edge_tminus1 = iterations[-1][e] if i > 0 else None
            prev_edge = edges_data[-1] if e > 0 else None

            if edge_tminus1:
                p_a = edge_tminus1.p_a_next(p_a, q1)
                q_a = edge_tminus1.q_a_next(p_a, q1)

            if prev_edge:
                q0 = prev_edge.q0()
                q1 = edge.q0()
                print('p_a:', p_a, 'q0:', q0, 'q1:', q1)
                data.append((p_a,q0,q1))
                d_prevk = prev_edge.d()

            edge = Edge(tau, v0, p_m, m, q_a, c, c_nextk, d_prevk)
            c_nextk = edge.c

            edges_data.append(edge) #= np.append(edges_data, edge)
        iterations.append(edges_data)# = np.append(iterations, edges_data)
