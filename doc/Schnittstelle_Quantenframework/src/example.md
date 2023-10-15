# Beispiel

Im Folgenden ein Beispiel für eine Anweisungsabfolge für das *QSFW*. **Das Beispiel dient nur dazu zu zeigen,
wie ein passender Code für das *QSFW* geschrieben wird. Die Sinnhaftigkeit/Machbarkeit der Anweisungen und deren Abfolge sei
erstmal dahingestellt.**

```
circuit(('a', 0), ('b', 1), ('c', 1));
ident('a');
pauliX('a');
pauliY('b');
pauliZ('c');
tphase('b');
phase('a', 2 * π);
measure('a');

cnot('a', 'b');
swap('b', 'c');
toffoli('a', 'b', 'c');
hadamard('b');
cnot('b', 'a');
measure('a');
```

Dieser *Code* sollte in einer Datei abgelegt werden die dann beim Aufruf des *QSFW* übergeben wird. Um das *QSFW*
von der Kommandozeile aufzurufen, muss in den Hauptordner gewechselt werden, in dem sich auch die Ordner `doc` und
`examples` befinden.
Mit der genannten Datei kann das *QSFW* dann zur Verarbeitung wie folgt aufgerufen werden:
```bash
python3 -m qsfw /pfad/zur/programm/datei.qs
```

Alle Ausgaben und Ereignisse werden dann auf der Standardausgabe ausgegeben und können von der GUI verarbeitet oder direkt vom Anwender gesichtet werden.

Das *QSFW* bietet auch noch verschiedene Kommandozeilen-Parameter. Um alle möglichen Parameter mit einer Erklärung einzusehen, kann das *QSFW* wie folgt aufgerufen werden:
```bash
python3 -m qsfw -h
```

Um eins der vorhandenen Beispiele unter `examples` auszuführen, muss ebenfalls in der Kommandozeile in den Hauptordner
gewechselt werden und dann das Beispiel wie folgt aufgerufen werden:
```bash
python3 examples/<beispiel>
```