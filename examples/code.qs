/* Erstmal einen Schaltkreis definieren! */
circuit(
    ('a', 0), 
    ('b', 1), 
    ('c', 1)
);
ident('a');
pauliX('a');
pauliY('b');
pauliZ('c');
tphase('b');
phase(
    'a', 
    2 * pi
);
measure('a');

cnot('a', 'b');
swap('b', 'c');
toffoli(
    'a', 
    'b', 
    'c'
); hadamard('b');
cnot('b', 'a');

// Nach dem hier müssten a und b verschränkt sein 
measure('a');