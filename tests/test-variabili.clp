
(defrule variabili-interne-attiva "Deve essere attiva per passare il test"
	(A B ?c D ?c)
=>
)

(defrule variabili-esterne-attiva "Deve essere attiva per passare il test"
	(?a ?b ?c ?d ?c)
	(?c ?b ?d ?a)
=>
)

(defrule variabili-interne-silente "Non deve essere attiva per passare il test"
	(A ?b ?c ?c C)
=>
)

(defrule variabili-esterne-silente "Non deve essere attiva per passare il test"
	(A ?b C D ?c)
	(?c B ?b A)
=>
)

(defrule not-variabile-interna-attiva "Deve essere attiva per passare il test"
	(A B ?c ~?c C)
=>
)

(defrule not-variabile-interna-silente "Non deve essere attiva per passare il test"
	(A B ?c D ~?c)
=>
)

(defrule not-variabile-esterna-attiva "Deve essere attiva per passare il test"
	(A B ?c D C)
	(C ~?c D A)
=>
)

(defrule not-variabile-esterna-silente "Non deve essere attiva per passare il test"
	(A ?b C D C)
	(A ~?b D A)
=>
)

(deffacts iniziali
	(A B C D C)
	(C B D A)
)
	
	