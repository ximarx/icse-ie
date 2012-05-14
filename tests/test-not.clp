
(defrule not-eq-attiva "Deve essere attiva"
	(A ?b C)
	(~?b ~E ?e)
	(~?e ?e ~?b)
=>
)

(defrule not-eq-variabile-silente "Non deve essere attiva"
	(?a B ?c)
	(~?c D E)
	(D E ~?a)
=>
)

(defrule not-eq-costante-silente "Non deve essere attiva"
	(A ~B C)
=>
)

	
(deffacts initial-facts
	(A B C)
	(C D E)
	(D E A)
)
