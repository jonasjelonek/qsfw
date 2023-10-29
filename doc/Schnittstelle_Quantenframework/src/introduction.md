# Einleitung

Das `qsfw` (Quantensimulationsframework oder auch Quantensimulator-Framework) bietet zwei verschiedene Wege, damit zu arbeiten und seine Funktionalitäten zu nutzen:
1. Einbindung als Python-Modul in ein eigenes Python-Projekt
2. Scripting über eine Schnittstellendatei mithilfe der CLI-Schnittstelle

Dieses Dokument beschreibt die zweite Möglichkeit, wie das `qsfw` mit einer Schnittstellendatei - bzw. 
umgangssprachlicher ausgedrückt einem Script - verwendet wird und wie die Syntax des QuantumScripts definiert ist. 
Das `qsfw` bietet hier eine CLI-Schnittstelle, wie man sie bereits vom Umgang mit Python-Skripten oder im 
Allgemeinen mit jeglichen Befehlen auf der Kommandozeile kennt.   
   
Der Aufruf des `qsfw` erfolgt grundsätzlich aus dem root-Verzeichnis des Projekts heraus. Genauer bedeutet das, lädt man das `qsfw` aus dem Github-Repository herunter und entpackt es lokal, öffnet man die Kommandozeile (unter Linux/macOS `Terminal`; unter Windows `Kommandozeile` oder `PowerShell`) und wechselt in das Verzeichnis, in das das `qsfw` entpackt wurde.   
Anschließend erfolgt der grundsätzliche Aufruf mit, hier mit dem Argument -h zur Anzeige der Hilfe:
```bash
python3 -m qsfw -h
```

Die Hilfe-Anzeige gibt grundsätzliche Informationen über die CLI-Schnittstelle des `qsfw`, im Detail welche  Parameter unterstützt/erfordert sind und wie sie anzugeben sind.

>Ein Aufruf aus einem anderen Verzeichnis heraus ist grundsätzlich möglich, erfordert jedoch einen erhöhten Aufwand zur Einrichtung. Python sucht standardmäßig nur in bestimmten Pfaden nach Modulen, demnach müsste dann der Pfad erst zur Umgebungsvariablen, die Python nutzt, hinzugefügt werden.

Hat man bereits eine Schnittstellendatei/ein Skript vorliegen, das mit dem `qsfw` ausgeführt werden soll, nutzt man:
```bash
python3 -m qsfw <options> <pfad zum skript>
```
Der Pfad zum Skript kann dabei absolut oder relativ angegeben werden. Bei einer relativen Angabe muss darauf 
geachtet werden, dass die Angabe relativ zum Arbeitsverzeichnis(Working Directory) erfolgen muss, also dem bereits
angesprochenen root-Verzeichnis des `qsfw` (sofern der Aufruf von dort aus erfolgt).   
   
Im Ordner `examples` des `qsfw` sind mehrere Beispiele zu finden, die zuerst getestet werden können. Die 
Beispiele, die als Python-Skript vorliegen, werden wie folgt aufgerufen:
```bash
python3 examples/<beispiel>
```

Die `.qs`-Dateien, die beispielhaften Skript-Code für der `qsfw` enthalten, können auch wie bereits 
beschrieben dem `qsfw` direkt übergeben werden:
```bash
python3 -m qsfw examples/code.qs
```