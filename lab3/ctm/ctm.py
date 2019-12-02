class Edge:
    def __init__(self, tau, v0, p_m, m, q_a, c, c_nextk):
        self.tau = tau
        self.v0 = v0
        self.p_m = p_m
        self.m = m
        self.q_a = q_a
        self.c = c
        self.c_nextk = c_nextk

    def pc(self):
        return 1/(self.v0 * self.tau + 1 / self.p_m)

    def q_e(self, p):
        if p <= self.pc():
            return self.v0 * p
        else
            return 1/self.tau * (1 - p/self.p_m)

    def s(self, k):
        if self.q_a > self.pc():
            return self.q_a
        else
            return self.c(k)

    def d(self, k):
        if (self.q_a <= this.pc:
            return self.q_a
        else:
            return self.c

    def q0(self, k):
        return min(d(k-1),s(k))

    def q1(self, k):
        return min(d(k),s(k+1))

    def p_a_next(self, k, delta_x = 1, delta_t = 5 / 60):
        p = 0
        return p + 1/delta_x * (self.q0() - self.q1()) * delta_t

    def q_a_next(self, k):
        return self.m * self.q_e(self.p_a_next(k)/self.m) # p_a(t+1) ?
