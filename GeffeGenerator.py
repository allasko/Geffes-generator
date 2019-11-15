class GeffeGenerator:
    LFSR1 = []
    LFSR2 = []
    LFSR3 = []
    output = []

    def __init__(self, _LFSR1, _LFSR2, _LFSR3):
        self.LFSR1 = _LFSR1
        self.LFSR2 = _LFSR2
        self.LFSR3 = _LFSR3

    def generateGeffe(self, lfsr1, lfsr2, lfsr3):
        notLfsr1 = self.myNOT(lfsr1)
        andLfsr1Lfsr3 = self.myAND(lfsr1, lfsr3)
        andNotLfsr1Lfsr2 = self.myAND(notLfsr1, lfsr2)
        res = self.myOR(andLfsr1Lfsr3, andNotLfsr1Lfsr2)
        self.output.append(res)

        return self.output

    def myAND(self, lfsr1, lfsr2):
        res = []
        for i in range(len(lfsr1)):
            if lfsr1[i] is 0 and lfsr2[i] is 0:
                res.append(0)
            elif lfsr1[i] is 0 and lfsr2[i] is 1:
                res.append(0)
            elif lfsr1[i] is 1 and lfsr2[i] is 0:
                res.append(0)
            elif lfsr1[i] is 1 and lfsr2[i] is 1:
                res.append(1)
        return res

    def myNOT(self, lfsr1):
        res = []
        for i in range(len(lfsr1)):
            if lfsr1[i] is 0:
                res.append(1)
            else:
                res.append(0)
        return res

    def myOR(self, lfsr1, lfsr2):
        res = []
        for i in range(len(lfsr1)):
            if lfsr1[i] is 0 and lfsr2[i] is 0:
                res.append(0)
            elif lfsr1[i] is 0 and lfsr2[i] is 1:
                res.append(1)
            elif lfsr1[i] is 1 and lfsr2[i] is 0:
                res.append(1)
            elif lfsr1[i] is 1 and lfsr2[i] is 1:
                res.append(1)
        return res