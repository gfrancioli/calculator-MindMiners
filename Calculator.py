class Calculator:
    def __init__(self, mediumPrice=0, mediumQuantity=0, loss=0, ram=0):
        self.mediumPrice = mediumPrice
        self.mediumQuantity = mediumQuantity
        self.result = []
        self.loss = loss
        self.ram = ram
        self.bought = 0
        self.selled = 0
        self.mediumTax = []

    def recalculatePrice(self, price, quantity, correctionTax):
        self.mediumPrice = (self.mediumPrice * self.mediumQuantity + price * quantity
                            + correctionTax) / (self.mediumQuantity + quantity)
        self.mediumQuantity += quantity
        self.bought += quantity * price
        self.mediumTax.append(correctionTax)

    def calculateResult(self, sellPrice, quantity, correctionTax):
        value = (sellPrice - self.mediumPrice) * quantity - correctionTax
        self.result.append(value)
        if self.loss >= 0:
            self.loss -= min(sum(self.result), self.loss)
        else:
            self.loss += sum(self.result)
        self.mediumQuantity -= quantity
        self.selled += quantity * sellPrice
        self.mediumTax.append(correctionTax)

    def calculateRam(self):
        self.ram = sum(self.result)

    def calculateIR(self):
        ir = (self.ram - min(self.ram, self.loss)) * 0.15
        return ir

    def calculateRentability(self):
        tax = (1 - (sum(self.mediumTax) / (len(self.mediumTax) * 100)))
        grossRentability = (1 - ((self.selled / self.bought))) * self.bought
        rentability = ((1 - (self.selled / self.bought) * tax)) * self.bought
        if self.bought > self.selled:
            return -grossRentability, self.bought, self.selled, -rentability
        else:
            return grossRentability, self.bought, self.selled, rentability

