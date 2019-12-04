class Edge:
    def __init__(self, tau, v0, p_a, p_m, m, q_a, c, c_nextk, d_prevk):
        self.tau = tau
        self.v0 = v0
        self.p_a = p_a
        self.p_m = p_m
        self.m = m
        self.q_a = q_a
        self.c = c
        self.c_nextk = c_nextk
        self.d_prevk = d_prevk

    def pc(self):
        return 1/(self.v0 * self.tau + 1 / self.p_m)

    def q_e(self, p):
        if p <= self.pc():
            return self.v0 * p
        elif p > self.pc() and p <= self.p_m:
            return 1/self.tau * (1 - p/self.p_m)
        else:
            return 0

    def s(self):
        if self.q_a > self.pc():
            return self.q_a
        else:
            return self.c_nextk

    def d(self):
        if self.q_a <= self.pc():
            return self.q_a
        else:
            return self.c

    def q0(self):
        return min(self.d_prevk,self.s())

    def p_a_next(self, q1, delta_x = 1, delta_t = 5.0 / 60):
        return self.p_a + 1/delta_x * (self.q0() - q1) * delta_t

    def q_a_next(self, q1):
        return self.m * self.q_e(self.p_a_next(q1)/self.m)

class Simulation:
    def __init__(self, edges, m, tau, n_iters):
        self.edges = edges
        self.m = m
        self.tau = tau
        self.n_iters = n_iters

    def run(self):
        v0 = 40.0
        p_m = 100.0
        c = 3000.0
        d_prevk = 3000.0

        p_a = 40
        q_a = 3000

        output = {}

        iterations = []
        for i in range(self.n_iters):
            edges_data = []
            for e in range(self.edges):
                if e == 0:
                    p_a = 40
    
                prev_edge = edges_data[-1] if e > 0 else None
                edge_tminus1 = iterations[-1][e] if i > 0 else None 
                prev_edge_tminus1 = iterations[-1][e-1] if i > 0 and e > 0 else None

                edge = Edge(self.tau, v0, p_a, p_m, self.m, q_a, c, c, d_prevk)

                if prev_edge and edge_tminus1:
                    q0 = prev_edge.q0()
                    q1 = edge.q0()
                    q1_tminus1 = edge_tminus1.q0()
                    next_q_a = prev_edge_tminus1.q_a_next(q1_tminus1)
                    if next_q_a > 0:
                        q_a = next_q_a
                    
                    p_a = prev_edge_tminus1.p_a_next(q1_tminus1)

                    if not e in output:
                        output[e] = []
                    output[e].append({'p_a':p_a,'q0':q0,'q1':q1,'d': prev_edge.d(), 's': prev_edge.s(), 'q_a':q_a})

                    d_prevk = prev_edge.d()

                edges_data.append(edge) #= np.append(edges_data, edge)
            iterations.append(edges_data)# = np.append(iterations, edges_data)

        return output
