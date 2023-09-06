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

Dieser *Code* sollte in einer Datei abgelegt werden die dann beim Aufruf des *QSFW* übergeben wird, also so ähnlich wie
```bash
python3 qsfw.py /pfad/zur/programm/datei.qs
```

Alle Ausgaben und Ereignisse werden dann auf der Standardausgabe ausgegeben und können von der GUI verarbeitet oder direkt vom Anwender gesichtet werden.