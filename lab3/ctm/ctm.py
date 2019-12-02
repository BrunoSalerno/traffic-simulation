class Edge:
    def __init__(self, tau, v0, p_m, m, q_a, c, c_nextk, d_prevk):
        self.tau = tau
        self.v0 = v0
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
        else:
            return 1/self.tau * (1 - p/self.p_m)

    def s(self):
        if self.q_a > self.pc():
            return self.q_a
        else:
            return self.c()

    def d(self):
        if self.q_a <= self.pc():
            return self.q_a
        else:
            return self.c

    def q0(self):
        return min(self.d_prevk,self.s())

    def p_a_next(self, q1, delta_x = 1, delta_t = 5 / 60):
        p = 40
        return p + 1/delta_x * (self.q0() - q1) * delta_t

    def q_a_next(self, q1):
        return self.m * self.q_e(self.p_a_next(q1)/self.m)

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

    for i in range(12):
        print('Min:',i)
        prev_edge = None
        for e in range(edges):
            edge = Edge(tau, v0, p_m, m, q_a, c, c_nextk, d_prevk)
            if prev_edge:
                print(prev_edge.q0())
                q_a = prev_edge.q_a_next(edge.q0())
                d_prevk = prev_edge.d()
            prev_edge = edge
