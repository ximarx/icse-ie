

(defrule positiva "regola positiva"
	(C)
	(A ?a B ?b)
	(B ?b A ?a)
=>
)

(defrule negativa-non-attivata "regola negativa"
	(C)
	(not (and
		(A ?a B ?b)
		(B ?b A ?a)
	))
=>
)

(defrule negativa-attivata "regola negativa"
	(C)
	(not (and
		(A ?a B ?b)
		(B ?b A ?a)
		(C ?b ?a C)
	))
=>
)


(deffacts fatti-iniziali
	(C)
	(A A B B)
	(B B A A)
	(C C C C)
)
