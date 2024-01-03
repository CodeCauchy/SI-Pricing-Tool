import numpy as np
import scipy.special
from scipy.stats import binom
import matplotlib.pyplot as plt

class EuropeanClaimCRR:
    """
    Die Klasse EuropeanClaimCRR beinhaltet für alle (erbenden) Klassen
    wichtige Methoden (z.B. die Berechnung der Wahrscheinlichkeitsparameter).
    Das Motiv ist das Einsparen von Code-Zeilen.
    """
    
    def calcMartingalMeasure(self, interestRate, up, down):
        """
        Die Methode berechnet die Wahrscheinlichkeitsparameter für ein CRR-Modell
        (unter Berücksichtigung der Arbitragefreiheit).
        
        Args:
            interestRate (float größer -1): "Risikoloser" Zins (z.B. für ein Tagesgeldkonto)
            up (float mit interestRate < up): Die Rendite für das Szenario, dass der Preis eines Assets steigt.
            down (float mit down < interestRate): Die Rendite für das Szenario, dass der Preis eines Assets fällt.
        
        Returns:
            Array: Der Array enthält zwei Einträge des Datentyps float, die größer als 0 sind und kleiner als 1.
            Der erste Eintrag beinhaltet die Wahrscheinlichkeit für einen Up, der zweite für einen Down.
        """
    
        probabilityUp = (interestRate - down) / (up - down)
        probabilityDown = 1.0 - probabilityUp
        return [probabilityUp, probabilityDown]

class CallOption(EuropeanClaimCRR):
    
    def payoff(self, assetPrice, strike):
        """
        Die Methode berechnet die Auszahlung einer europäischen Call-Option.
        
        Args:
            assetPrice (float größer 0): Preis des Assets.
            strike (float größer 0): Parameter einer europäischen Call-Option und bestimmt die Schranke, 
            ab welcher eine Auszahlung stattfindet.
        
        Returns:
            Float (größer/gleich 0): Die Auszahlung für den Eigentümer einer Europäischen Call-Option nach
            Ablauf der Laufzeit.
        """
        
        return max(assetPrice - strike,0)
    
    def calcPrice(self, interestRate, up, down, maturity, startPrice, strike):
        """
        Die Methode berechnet den Preis einer europäischen Call-Option gem. klassischer Arbitragetheorie im
        arbitragefreien CRR-Modell.
        
        Args:
            interestRate (float größer -1): "Risikoloser" Zins (z.B. für ein Tagesgeldkonto)
            up (float mit interestRate < up): Die Rendite für das Szenario, dass der Preis eines Assets steigt.
            down (float mit down < interestRate): Die Rendite für das Szenario, dass der Preis eines Assets fällt.
            maturity (int größer 0): Laufzeit der Call-Option.
            startPrice (float größer 0): Startpreis des Assets.
            strike (float größer 0): Parameter einer europäischen Call-Option und bestimmt die Schranke, 
            ab welcher eine Auszahlung stattfindet.
        
        Returns:
            Float (größer/gleich 0): Der (arbitragefreie) Preis für eine europäische Call-Option zum gegenwärtigen
            Zeitpunkt.
        """
        
        upReturn = 1.0 + up
        downReturn = 1.0 + down
        expectedValue = 0.0
        probUp = super().calcMartingalMeasure(interestRate, up, down)[0]
        
        for numberUps in range(maturity):
            numberDowns = maturity - numberUps
            scenarioReturn = (upReturn ** numberUps) * (downReturn ** numberDowns)
            pay = self.payoff(startPrice * scenarioReturn, strike)
            expectedValue = expectedValue + binom.pmf(numberUps, maturity, probUp) * pay
        return expectedValue / ((1.0 + interestRate) ** maturity)

class PutOption(EuropeanClaimCRR):
    def payoff(self, assetPrice, strike):
        """
        Die Methode berechnet die Auszahlung einer europäischen Put-Option.
        
        Args:
            assetPrice (float größer 0): Preis des Assets.
            strike (float größer 0): Parameter einer europäischen Put-Option und bestimmt die Schranke, 
            ab welcher eine Auszahlung stattfindet.
        
        Returns:
            Float (größer/gleich 0): Die Auszahlung für den Eigentümer einer Europäischen Put-Option nach
            Ablauf der Laufzeit.
        """
        
        return max(strike - assetPrice,0)
    
    def calcPrice(self, interestRate, up, down, maturity, startPrice, strike):
        """
        Die Methode berechnet den Preis einer europäischen Put-Option gem. klassischer Arbitragetheorie im
        arbitragefreien CRR-Modell.
        
        Args:
            interestRate (float größer -1): "Risikoloser" Zins (z.B. für ein Tagesgeldkonto)
            up (float mit interestRate < up): Die Rendite für das Szenario, dass der Preis eines Assets steigt.
            down (float mit down < interestRate): Die Rendite für das Szenario, dass der Preis eines Assets fällt.
            maturity (int größer 0): Laufzeit der Put-Option.
            startPrice (float größer 0): Startpreis des Assets.
            strike (float größer 0): Parameter einer europäischen Put-Option und bestimmt die Schranke, 
            ab welcher eine Auszahlung stattfindet.
        
        Returns:
            Float (größer/gleich 0): Der (arbitragefreie) Preis für eine europäische Put-Option zum gegenwärtigen
            Zeitpunkt.
        """
        
        upReturn = 1.0 + up
        downReturn = 1.0 + down
        expectedValue = 0.0
        probUp = super().calcMartingalMeasure(interestRate, up, down)[0]
        
        for numberUps in range(maturity):
            numberDowns = maturity - numberUps
            scenarioReturn = (upReturn ** numberUps) * (downReturn ** numberDowns)
            pay = self.payoff(startPrice * scenarioReturn, strike)
            expectedValue = expectedValue + binom.pmf(numberUps, maturity, probUp) * pay
        return expectedValue / ((1.0 + interestRate) ** maturity)

class UICallOption(EuropeanClaimCRR):
    
    def payoff(self, assetPrices, strike, barriere):
        """
        Die Methode berechnet die Auszahlung einer europäischen Up & In Call-Option.
        
        Args:
            assetPrices (Array mit floats größer 0): Preise des Assets (vom Zeitpunkt 0 bis zum Ende der Laufzeit).
            Dabei ist repräsentiert der Eintrag t im Array den Zeitpunkt t.
            strike (float größer 0): Bestimmt die Schranke, ab welcher eine Auszahlung stattfindet (falls die
            Barriere erreicht wird).
            barriere (float größer strike): Die Barriere ist eine Schranke, die einmal (bevor die Laufzeit
            endet) erreicht werden muss, damit grundsätzlich die Möglichkeit einer Auszahlung besteht. 
        
        Returns:
            Float (größer/gleich 0): Die Auszahlung für den Eigentümer einer Europäischen Up & In Call-Option nach
            Ablauf der Laufzeit.
        """
        
        if self.checkBarriere(assetPrices, barriere):
            return max(assetPrices[len(assetPrices)] - strike,0)
        else:
            return 0
    
    def checkBarriere(self, assetPrices, barriere):
        """
        Die Methode prüft, ob ein Asset die Barriere einmal durchbrechen konnte.
        
        Args:
            assetPrices (Array mit floats größer 0): Preise des Assets (vom Zeitpunkt 0 bis zum Ende der Laufzeit).
            Dabei ist repräsentiert der Eintrag t im Array den Zeitpunkt t.
            barriere (float größer strike): Die Barriere ist eine Schranke, die einmal (bevor die Laufzeit
            endet) erreicht werden muss, damit grundsätzlich die Möglichkeit einer Auszahlung besteht. 
        
        Returns:
            Boolean: Der Default-Wert ist False. Wurde die Barriere einmal erreicht, wird der Wert auf True gesetzt.
        """
        
        check = False
        for time in range(len(assetPrices)):
            if assetPrices[time] >= barriere:
                check = True
                break
        return check
    
    def barrierLimits(self, up, maturity, startPrice, barriere):
        """
        Die Methode berechnet die Anzahl der Ups, die notwendig ist, damit ein Asset den Wert der Barriere annimmt
        (Downs gibt es nicht). Wichtig ist, dass die Parameter entsprechend gewählt werden, damit das möglich ist
        (das ist eine Voraussetzung des Modells). Aktuell werden ungünstige Parameter nicht abgefangen. Dies ist unbedingt
        vom Anwender zu berücksichtigen (Fehler werden grundsätzlich in keiner Klasse abgefangen). Der Wert wird für
        das Pricing des Derivates benötigt.
        
        Args:
            up (float mit interestRate < up): Die Rendite für das Szenario, dass der Preis eines Assets steigt.
            maturity (int größer 0): Laufzeit der Put-Option.
            startPrice (float größer 0): Startpreis des Assets.
            barriere (float größer strike): Die Barriere ist eine Schranke, die einmal (bevor die Laufzeit
            endet) erreicht werden muss, damit grundsätzlich die Möglichkeit einer Auszahlung besteht.
        
        Returns:
            Int (größer 0): Die Anzahl der Ups, die notwendig ist, damit ein Asset den Wert der Barriere annimmt
        (Downs gibt es nicht).
        """
        
        upReturn = 1.0 + up
        for numberUps in range(maturity):
            if barriere == startPrice * (upReturn ** numberUps):
                limit = numberUps
                break
        return limit
    
    def calcPriceSum1(self, interestRate, up, down, maturity, startPrice, strike, barriere):
        """
        Für die Berechnung des Preises (im arbitragefreien CRR-Modell) müssen zwei Summanden berechnet
        werden. Präziser müssen zwei Erwartungswerte für bestimmte Szenarien berechnet werden (hier
        ist der Endwert des Assets größer oder gleich der Barriere).
        
        Args:
            interestRate (float größer -1): "Risikoloser" Zins (z.B. für ein Tagesgeldkonto)
            up (float mit interestRate < up): Die Rendite für das Szenario, dass der Preis eines Assets steigt.
            down (float mit down < interestRate): Die Rendite für das Szenario, dass der Preis eines Assets fällt.
            maturity (int größer 0): Laufzeit der Put-Option.
            startPrice (float größer 0): Startpreis des Assets.
            strike (float größer 0): Bestimmt die Schranke, ab welcher eine Auszahlung stattfindet (falls die
            Barriere erreicht wird).
            barriere (float größer strike): Die Barriere ist eine Schranke, die einmal (bevor die Laufzeit
            endet) erreicht werden muss, damit grundsätzlich die Möglichkeit einer Auszahlung besteht.
        
        Returns:
            Float (größer/gleich 0): Ein Summand für die Berechnung des (arbitragefreien) Preises für eine
            Up & In Call-Option zum gegenwärtigen Zeitpunkt.
        """
        
        upReturn = 1.0 + up
        sum1 = 0.0
        probUp = super().calcMartingalMeasure(interestRate, up, down)[0]
        
        for numberUps in range(maturity):
            endPrice = startPrice * (upReturn ** (2.0 * numberUps - maturity))
            if endPrice >= barriere:
                sum1 = sum1 + max(endPrice - strike, 0) * binom.pmf(numberUps, maturity, probUp)
        
        return sum1
    
    def calcPriceSum2(self, interestRate, up, down, maturity, startPrice, strike, barriere):
        """
        Für die Berechnung des Preises (im arbitragefreien CRR-Modell) müssen zwei Summanden berechnet
        werden. Präziser müssen zwei Erwartungswerte für bestimmte Szenarien berechnet werden (hier
        ist der Endwert des Assets kleiner als die Barriere).
        
        Args:
            interestRate (float größer -1): "Risikoloser" Zins (z.B. für ein Tagesgeldkonto)
            up (float mit interestRate < up): Die Rendite für das Szenario, dass der Preis eines Assets steigt.
            down (float mit down < interestRate): Die Rendite für das Szenario, dass der Preis eines Assets fällt.
            maturity (int größer 0): Laufzeit der Put-Option.
            startPrice (float größer 0): Startpreis des Assets.
            strike (float größer 0): Bestimmt die Schranke, ab welcher eine Auszahlung stattfindet (falls die
            Barriere erreicht wird).
            barriere (float größer strike): Die Barriere ist eine Schranke, die einmal (bevor die Laufzeit
            endet) erreicht werden muss, damit grundsätzlich die Möglichkeit einer Auszahlung besteht.
        
        Returns:
            Float (größer/gleich 0): Ein Summand für die Berechnung des (arbitragefreien) Preises für eine
            Up & In Call-Option zum gegenwärtigen Zeitpunkt.
        """
        
        upReturn = 1.0 + up
        sum2 = 0.0
        probUp = super().calcMartingalMeasure(interestRate, up, down)[0]
        limit = self.barrierLimits(up, maturity, startPrice, barriere)
        tempStrike = strike * (upReturn ** (- 2.0 * limit))
        tempBarriere = (startPrice**2) / barriere
        for numberUps in range(maturity):
            endPrice = startPrice * (upReturn ** (2.0 * numberUps - maturity))
            if endPrice < tempBarriere:
                sum2 = sum2 + max(endPrice - tempStrike, 0) * binom.pmf(numberUps, maturity, probUp)
        return ((probUp / (1.0 - probUp)) ** limit) * ((barriere / startPrice) ** 2.0) * sum2
    
    def calcPrice(self, interestRate, up, down, maturity, startPrice, strike, barriere):
        """
        Die Methode berechnet den arbitragefreien Preis für eine Up & In Call-Option im CRR-Modell.
        
        Args:
            interestRate (float größer -1): "Risikoloser" Zins (z.B. für ein Tagesgeldkonto)
            up (float mit interestRate < up): Die Rendite für das Szenario, dass der Preis eines Assets steigt.
            down (float mit down < interestRate): Die Rendite für das Szenario, dass der Preis eines Assets fällt.
            maturity (int größer 0): Laufzeit der Put-Option.
            startPrice (float größer 0): Startpreis des Assets.
            strike (float größer 0): Bestimmt die Schranke, ab welcher eine Auszahlung stattfindet (falls die
            Barriere erreicht wird).
            barriere (float größer strike): Die Barriere ist eine Schranke, die einmal (bevor die Laufzeit
            endet) erreicht werden muss, damit grundsätzlich die Möglichkeit einer Auszahlung besteht.
        
        Returns:
            Float (größer/gleich 0): Der (arbitragefreie) Preis für eine Up & In Call-Option zum gegenwärtigen Zeitpunkt
            im CRR-Modell.
        """
        
        sum1 = self.calcPriceSum1(interestRate, up, down, maturity, startPrice, strike, barriere)
        sum2 = self.calcPriceSum2(interestRate, up, down, maturity, startPrice, strike, barriere)
        diskont = (1.0 + interestRate) ** maturity
        
        return (sum1 + sum2) / diskont

if __name__ == "__main__":
    #Maturity-Preis
    option = UICallOption()
    maturities = []
    prices1 = []
    prices2 = []
    prices3 = []
    for i in range(4, 100):
        maturities.append(i)
        prices1.append(option.calcPrice(-0.25, 1.0, -0.5, i, 1, 1, 8))
        prices2.append(option.calcPrice(0.0, 1.0, -0.5, i, 1, 1, 8))
        prices3.append(option.calcPrice(0.25, 1.0, -0.5, i, 1, 1, 8))
    
    plt.plot(maturities, prices1, label="Zins=-0.25")
    plt.plot(maturities, prices2, label="Zins=0.0")
    plt.plot(maturities, prices3, label="Zins=0.25")
    plt.legend(loc='best')
    plt.xlabel("Maturity")
    plt.ylabel("Price")
    plt.title("Preis in Abhängigkeit von der Laufzeit (Strike=1;Barriere=8)")
    plt.grid()
    plt.show()
    
    #Barrier-Preis
    option = UICallOption()
    barrier = []
    prices1 = []
    prices2 = []
    prices3 = []
    for i in range(15):
        barrier.append(2.0**i)
        prices1.append(option.calcPrice(-0.25, 1.0, -0.5, 20, 1, 1, barrier[i]))
        prices2.append(option.calcPrice(0.0, 1.0, -0.5, 20, 1, 1, barrier[i]))
        prices3.append(option.calcPrice(0.25, 1.0, -0.5, 20, 1, 1, barrier[i]))
    
    plt.plot(barrier, prices1, label="Zins=-0.25")
    plt.plot(barrier, prices2, label="Zins=0.0")
    plt.plot(barrier, prices3, label="Zins=0.25")
    plt.legend(loc='best')
    plt.xlabel("Barriere")
    plt.ylabel("Price")
    plt.title("Preis in Abhängigkeit von der Barriere (Strike=1;Laufzeit=20)")
    plt.grid()
    plt.show()
    
    #Strike-Preis
    option = UICallOption()
    strike = []
    prices1 = []
    prices2 = []
    prices3 = []
    for i in range(120):
        strike.append(i)
        prices1.append(option.calcPrice(-0.25, 1.0, -0.5, 20, 1, i, 128))
        prices2.append(option.calcPrice(0.0, 1.0, -0.5, 20, 1, i, 128))
        prices3.append(option.calcPrice(0.25, 1.0, -0.5, 20, 1, i, 128))
    
    plt.plot(strike, prices1, label="Zins=-0.25")
    plt.plot(strike, prices2, label="Zins=0.0")
    plt.plot(strike, prices3, label="Zins=0.25")
    plt.legend(loc='best')
    plt.xlabel("Strike")
    plt.ylabel("Price")
    plt.title("Preis in Abhängigkeit vom Strike (Barriere=128;Laufzeit=20)")
    plt.grid()
    plt.show()
    #Zins-Preis
    option = UICallOption()
    interest = np.linspace(-0.49, 0.99, 100)
    prices1 = []
    prices2 = []
    prices3 = []
    for i in interest:
        prices1.append(option.calcPrice(i, 1.0, -0.5, 20, 1, 1, 2))
        prices2.append(option.calcPrice(i, 1.0, -0.5, 20, 1, 1, 16))
        prices3.append(option.calcPrice(i, 1.0, -0.5, 20, 1, 1,128))
    
    plt.plot(interest, prices1, label="Barriere=2")
    plt.plot(interest, prices2, label="Barriere=16")
    plt.plot(interest, prices3, label="Barriere=128")
    plt.legend(loc='best')
    plt.xlabel("Interest Rate")
    plt.ylabel("Price")
    plt.title("Preis in Abhängigkeit vom Zins (Strike=1;Laufzeit=20)")
    plt.grid()
    plt.show()