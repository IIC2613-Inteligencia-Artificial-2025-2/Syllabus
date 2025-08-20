
% i1 es un interruptor
% i1 representa a un objeto
% sintacticamente i1 es una "constante"
% sintácticamente interruptor es un "predicado"
interruptor(i1).
interruptor(i2).
encendido(i2).
% alumbra es una relación entre i1 y z2
% sintácticamente alumbra es un "predicado"
alumbra(i1, z4).
alumbra(i2, z2).

iluminado(Z) :- interruptor(I), encendido(I),
    alumbra(I,Z).

