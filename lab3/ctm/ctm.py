import random

class Edge:
    def __init__(self, tau, v0, p_a, p_m, m, q_a, d_prevk, delta_t, delta_x, c):
        self.tau = tau
        self.v0 = v0
        self.p_a = p_a
        self.p_m = p_m
        self.m = m
        self.q_a = q_a
        self.d_prevk = d_prevk
        self.delta_t = delta_t
        self.delta_x = delta_x
        self.capacity = c # capacity

    # total
    def c(self):
        if self.capacity:
            return self.capacity
        return self.pc() * self.v0

    # total
    def pc(self):
        return 1/(self.v0 * self.tau + (1 / self.p_m))

    # per lane
    def q_e(self, p):
        p_m = self.p_m / self.m
        pc = self.pc() / self.m
        if p <= pc:
            return self.v0 * p
        elif p > pc and p <= p_m:
            return (1/self.tau) * (1 - (p/p_m))
        else:
            return 0

    # total
    def s(self):
        if self.p_a > self.pc():
            return self.q_a
        else:
            return self.c()

    # total
    def d(self):
        if self.p_a <= self.pc():
            return self.q_a
        else:
            return self.c()

    # total
    def q0(self):
        return min(self.d_prevk,self.s())

    # total
    def p_a_next(self, q1):
        return self.p_a + (1/self.delta_x) * (self.q0() - q1) * self.delta_t

    # total
    def q_a_next(self, q1):
        return self.m * self.q_e(self.p_a_next(q1)/self.m)

class Simulation:
    def __init__(self, edges, m, tau, n_iters, delta_t, delta_x, v0, p_m):
        self.edges = edges
        self.m = m
        self.tau = tau
        self.n_iters = n_iters
        self.delta_t = delta_t
        self.delta_x = delta_x
        self.v0 = v0
        self.p_m = p_m
        self.bottlenecks = {}

    # To create a bottleneck in any given edge
    # we just set p_m to a low value
    def add_bottleneck(self, edge, capacity, interval=None):
        self.bottlenecks[edge]={'capacity': capacity, 'interval': interval}

    def bottleneck_if_exist(self, edge, interval):
        if edge in self.bottlenecks:
            bottleneck = self.bottlenecks[edge]
            if bottleneck['interval']:
                return bottleneck['capacity'] if interval >= bottleneck['interval'] else None
            else:
                return bottleneck['capacity']
        else:
            return None

    def run(self, p_as_for_initial_edge = [], p_as_for_initial_iter=[], q_as_for_initial_edge = [], q_as_for_initial_iter = []):
        output = {}
        iterations = []

        for i in range(self.n_iters):
            edges_data = []
            for e in range(self.edges):
                prev_edge = edges_data[-1] if e > 0 else None
                edge_tminus1 = iterations[-1][e] if i > 0 else None
                prev_edge_tminus1 = iterations[-1][e-1] if i > 0 and e > 0 else None

                if e == 0:
                    p_a = p_as_for_initial_edge[i]
                    q_a = q_as_for_initial_edge[i]
                    d_prevk = q_a

                if i == 0 and e > 0:
                    p_a = p_as_for_initial_iter[e]
                    q_a = q_as_for_initial_iter[e]

                ## Bottleneck ############################
                bottleneck_capacity = self.bottleneck_if_exist(e, i)
                ##########################################

                if prev_edge:
                    d_prevk = prev_edge.d()

                if prev_edge and edge_tminus1:
                    q0 = prev_edge.q0()
                    q1 = edge.q0()
                    q1_tminus1 = edge_tminus1.q0()
                    q_a = prev_edge_tminus1.q_a_next(q1_tminus1)
                    p_a = prev_edge_tminus1.p_a_next(q1_tminus1)

                    print('q0',q0,'q1',q1,'q1_tminus1',q1_tminus1,'q_a',q_a,'p_a',p_a)
                    if not e in output:
                        output[e] = []
                    output[e].append({'p_a':p_a,'q0':q0,'q1':q1,'d': prev_edge.d(), 's': prev_edge.s(), 'q_a':q_a})

                edge = Edge(self.tau, self.v0, p_a, self.p_m, self.m, q_a, d_prevk, self.delta_t, self.delta_x, bottleneck_capacity)

                edges_data.append(edge)
            iterations.append(edges_data)

        return output
