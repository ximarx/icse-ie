
(defrule assigned-pattern-CE-attivato "Questa regola deve avere riscontro per passare il test"
	?a <- (A B)
	?b <- (A B C)
=>
)

(deffacts fatti-iniziali "Attivano negative-attivano, ma non negative-silente"
	(A B)
	(A B C)
)
	

