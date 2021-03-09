# ImportKonverter
Konverter-Skripte für verschiedene Datenquellen

## Wofür dies ist

Dieses Script ist dafür gedacht auf einem Arbeitsrechner aus Tabellen mit Schülerdaten (Schüler, Kurse, Lehrer, ...) eine Import-Datei für den PhilleConnect-Server zu machen.

## Benutzung

Die Daten müssen als .csv-Datei zur Verfügung stehen. Eine solche lässt sich mit jedem Tabellenkalkulationsprogramm erstellen.

Die Daten müssen dabei eine Titelzeile haben die den Schlüsselbegriff für die entsprechenden Daten enthalten. Diese sind in der `lusd.py` unter `# Configuration information` definiert, so muss z.B. die Spalte mit den Schüler-Vornamen die Titelzeile `Schueler_Vorname` enthalten.

Als Spaltentrenner ist `;` vorgesehen, die Standardeinstellungen beim Speichern aus LibreOffice-Calc funktionieren.

Es sind zwei csv-Dateien nötig: Die erste enthält die Lehrerdaten, die zweite die Kursdaten samt Schülern. Die zweite ist damit in der Regel mehrere tausend Zeilen groß, da sie jede Kurs-Schüler-Beziehung enthält. Sie kann so z.B. aus der hessischen Schülerdatenbank LUSD exportiert werden (daher der Name des scriptes).

Aufgerufen werden muss das Skript mit drei Argumenten, das erste ist der Pfad zur 

Beispiel:

`python3 lusd.py teachers.csv groups.csv ./`

Liegen die Daten nur anders vor muss das Script entsprechend an die eigenen Bedürfnisse oder Daten angepasst werden. Liegen z.B. keine Kurszuordnungen vor können auch nur die Schüler- und Lehrerdaten entsprechend verwendet werden.
