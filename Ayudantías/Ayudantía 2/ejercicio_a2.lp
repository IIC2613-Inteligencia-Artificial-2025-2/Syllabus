%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    DEFINICIÓN DEL GRAFO    %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
nodo(1..4).
arista(1, 2).
arista(1, 3).
arista(2, 4). % Comentar esto hace al grafo no conexo
arista(X, Y) :- arista(Y, X). % Grafo no dirigido

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%          PROBLEMA          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1. Dado un grafo, genere predicados para determinar si dos nodos X e Y 
%    están `conectados` por algún camino o no. Observe que pasa cuando 
%    X = Y. Evite que un nodo esté conectado con sí mismo.
%
%    BONUS: Genere un predicado para obtener los nodos aislados. Puede
%    investigar sobre la directiva `count` (no es necesario usarla)
%
% 2. Ahora, genere un predicado para determinar si un nodo X es `no 
%    superalcanzable`. Es decir, este predicado debe indicar si existe o
%    no algún nodo Y tal que X e Y no posean ningún camino que los 
%    conecte.
%
% 3. Finalmente, genere un predicado para determinar si un nodo X es
%    `superalcanzable`. Es decir, que indique si todo nodo posee un
%    camino hacia él. Formalmente cuando esto ocurre en un grafo, lo 
%    llamamos grafo conexo.

% Primer problema
conectados(X, Y) :- arista(X, Y).
conectados(X, Y) :- conectados(X, Z), arista(Z, Y), X != Y, X != Z, Y != Z.

% Bonus
% aislado(X) :- #count{Y : nodo(Y), conectados(X, Y)} < 1, nodo(X).
aislado(X) :- nodo(X), not conectados(X, _).

% Segundo problema
no_superalcanzable(X) :- not conectados(X, Y), nodo (Y), nodo(X), X != Y.

% Tercer problema
superalcanzable(X) :- not no_superalcanzable(X), nodo(X).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Descomenta esta línea para que el modelo sea satisfacible si y solo si
% el grafo es conexo.
% Comenta la línea para que el visualizador funcione
% :- not superalcanzable(X), nodo(X).