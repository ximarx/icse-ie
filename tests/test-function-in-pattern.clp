

(defrule function-attiva "Deve essere attiva per superare il test"
	(A ?var)
	(A =(+ 1 ?var) B)
=>
)

(defrule function-silente "Non deve essere attiva per superare il test"
	(A =(+ 1 1.1) B)
=>
)


(deffacts iniziali
	(A 1)
	(A 2 B)
)
