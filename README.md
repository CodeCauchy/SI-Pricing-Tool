# SI-Pricing-Tool
Das Programm EuropeanClaimCRR.py habe ich für einige Artikel auf
meiner Website (liberalfinance.de) verwendet und möchte dieses kleine
Skript hier gerne zur Verfügung stellen. Es handelt sich hier um ein
privates Hobby-Projekt. Für Fehlermeldungen und weitere Anmerkungen
bin ich sehr dankbar.

In der hier vorliegenden Version sind einige Klassen für das Pricing
von europäischen Claims vorhanden (im CRR-Modell). Mehr Details kann
man im Code nachlesen.

Das Programm wurde in Python 3.10.11 geschrieben.Weiterhin wurden die
folgenden Bibliotheken verwendet:
-numpy
-scipy
-matplotlib
Hat der User die oben beschriebenen Programme installiert, sollte er
das Programm ausführen können.

Ich möchte anmerken, dass keine Fehler abgefangen werden. Der User
sollte also auch auf eine sinnvolle Wahl der Parameter achten. Z.B.
wird nicht geprüft, ob down < interestRate gilt, etc.

Wird das Programm ausgeführt, erscheinen einige Plots zu den Preis
einer U&I Call-Option.

Ich wünsche viel Spaß beim spielen.
