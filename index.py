from Calculator import Calculator
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./stocks-dataset.csv')
df = data.rename(columns={'Data da operação': 'Data', 'Operação': 'Operacao'}, inplace=False)


def monthSeparate(df):
    old = False
    monthDf = pd.DataFrame()

    # separate by month
    for index, item in enumerate(df.values):
        if old and item[0][-2:] < old[-2:]: break
        dfRow = pd.DataFrame(df.loc[index]).transpose()
        monthDf = pd.concat([monthDf, dfRow])
        old = item[0]
        df = df.drop([index], axis=0)

    df.to_csv('./stocks-dataset.csv', index=False)
    return monthDf


def calculateMonth(month):
    monthOne = Calculator()
    for item in month.values:
        if item[1] == 'Compra':
            monthOne.recalculatePrice(item[3], item[4], item[5])
        else:
            monthOne.calculateResult(item[3], item[4], item[5])
    monthOne.calculateRam()
    ir = monthOne.calculateIR()
    grossRentability, bought, selled, rentability = monthOne.calculateRentability()
    output = pd.DataFrame({'Mes': [month['Data'][0][-5:-3]],
                           'Valor Compra - R$': [bought],
                           'Valor Venda - R$': [selled],
                           'Rendimento Bruto Absoluto': [grossRentability],
                           'Imposto devido - R$': [ir],
                           'Rendimento Liquido Absoluto': [rentability]})
    return output, bought, selled, rentability


def plotData(bought, selled, rentability):
    plt.axhline(0)
    plt.bar([0, 1, 2], [bought, selled, rentability],
            tick_label=['Bought', 'Selled', 'Rentability'],
            width=0.5,
            color=['green', 'red', 'blue'],
            align='center')
    plt.xlabel('Operation')
    plt.ylabel('R$')
    plt.title('Rentability in R$ comparing with bought and selled actions')
    plt.show()


uniqueMonth = monthSeparate(df)
dfResponse, bought, selled, rentability = calculateMonth(uniqueMonth)
plotData(bought, selled, rentability)
dfResponse.to_csv('./output.csv')
