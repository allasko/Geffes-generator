class LFSR:
    lengthOfRegister = int
    register = []
    polynomial = []
    output = []

    def __init__(self, _lengthOfRegister, _initRegister, _polynomial):
        self.lengthOfRegister = _lengthOfRegister
        self.register = _initRegister
        self.polynomial = _polynomial
        if len(_initRegister) < _polynomial[0] - 1:
            raise ValueError("Polynomial degree is too small!")

    def makeLFSR(self, n):
        output = []
        for i in range(n):
            sum = 1
            for x in self.polynomial:
                sum += self.register[len(self.register) - x - 1]
            first = self.register[0]
            output = [first] + output
            self.register.pop(0)
            self.register.append(sum % 2)
        print(str(output))
        zeros = 0
        ones = 0
        for i in output:
            if i == 1:
                ones += 1
            else:
                zeros += 1
        print("Zeros: " + str(zeros / len(output)))
        print("Ones: " + str(ones / len(output)))

        return output

    def getLen(self):
        return self.lengthOfRegister
