
(defrule nnc-primo-attiva "Regola con NccPredicate come primo nodo"
	(not (and
		(A B Z)
		(2 ? ? ? E)
	))
	(A B C)
=>
)

(defrule nnc-primo-silente "Regola con NccPredicate come primo nodo"
	(not (and
		(A B C)
		(G ? ?c ? E)
	))
	(A B ?c)
=>
)

(defrule nnc-attiva "Regola con NccPredicate come primo nodo"
	(A B C)
	(not (and
		(A B Z)
		(2 ? ? ? E)
	))
=>
)

(defrule nnc-silente "Regola con NccPredicate come primo nodo"
	(?a B C)
	(not (and
		(A B C)
		(G ?a ? ? E)
	))
=>
)


(deffacts fatti-iniziali
	(G A C 2 E)
	(G A C Z E)
	(A B C)
)
