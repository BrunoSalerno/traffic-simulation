class CTM:
    def s(self, k):
        if qa(k) > pc:
            return q(k)
        else
            return c(k)

    def d(self, k):
        if (q(k) <= pc:
            return q(k)
        else:
            return c(k)

    def q0(self, k):
        return min(d(k-1),s(k))

    def q1(self, k):
        return min(d(k),s(k+1))
