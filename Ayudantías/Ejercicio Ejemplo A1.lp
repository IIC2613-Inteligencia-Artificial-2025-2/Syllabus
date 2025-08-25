planta(tomate).
planta(durazno).
planta(uva).
planta(oregano).

regador(r1).
regador(r2).
regador(r3).

% riega(R,P) el regador R riega a la planta P
riega(r1, durazno).
riega(r1, uva).
riega(r2, tomate).
riega(r3, oregano).
riega(r2, oregano).

#show regada/1.
#show encendido/1.
% #show defectuoso/1.
#show seca/1.

% encendido(R) expresa el regador R está encendido

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PRIMER EJERCICIO: Armar predicados y restricciones para expresar que
% i.   Sólo puede haber 1 regador encendido
% 1 {encendido(r1) ; encendido(r2) ; encendido(r3)} 1.

% OTRA SOLUCIÓN (MEJOR)
% 1 {encendido(R) : regador(R) } 1.

% ii.  Una planta está regada cuando un regador que la riega está encendido.
% regada(P) :- riega(R, P), planta(P), encendido(R).

% iii.  Una planta está seca cuando no está siendo regada.
% seca(P) :- not regada(P), planta(P).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SEGUNDO EJERCICIO: Armar predicados para expresar que
% i.   La planta de orégano y tomate no pueden estar secas.

% :- seca(oregano), seca(tomate).

% SOLUCIÓN ALTERNATIVA
% objetivo :- not seca(oregano).
% objetivo :- not seca(tomate).
% :- not objetivo.

% ii.  El tomate ni el oregano pueden estar secos.
% :- seca(oregano).
% :- seca(tomate).

% SOLUCIÓN ALTERNATIVA
% objetivo :- not seca(oregano), not seca(tomate).
% :- not objetivo.

% iii. El regador 2 está defectuoso
% defectuoso(r2).

% iv.  [Modiifca el ítem i. del PRIMER EJERCICIO] Si un regador está 
%      defectuoso, no puede estar encendido. Máximo hay 1 encendido.
% 1 { encendido(R) : not defectuoso(R), regador(R) } 1.
