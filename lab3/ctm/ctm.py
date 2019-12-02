class Iteration:
    def __init__(self, c, tau, v0, p_m, m, q_a):
        self._q = []
        self._c = c
        self._q_a = q_a
        self.tau = tau
        self.v0 = v0
        self.p_m = p_m
        self.m = m

    def pc(self):
        return 1/(self.v0 * self.tau + 1 / self.p_m)

    def q(self, k):
        return self._q[k]

    def c(self, k):
        return self._c[k]

    def s(self, k):
        if self.q_a(k) > self.pc():
            return self.q_a(k)
        else
            return self.c(k)

    def d(self, k):
        if (q(k) <= this.pc:
            return q(k)
        else:
            return c(k)

    def q0(self, k):
        return min(d(k-1),s(k))

    def q1(self, k):
        return min(d(k),s(k+1))

    def p_a_next(self, k):

    def q_e(self, p):
        if p <= self.pc():
            return self.v0 * p
        else
            return 1/self.tau * (1 - p/self.p_m)

    def q_a(self, k):
        return self._q_a[k]

    def q_a_next(self, k):
        return self.m * self.q_e(self.p_a_next(k)/self.m) # p_a(t+1) ?
