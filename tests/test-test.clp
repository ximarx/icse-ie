
(defrule test-eq-attivo "Esegue test su uguaglianza"
	(A B ?primo)
	(A B ?secondo)
	(test (= ?primo ?secondo))
=>
)

(defrule test-eq-silente "Esegue test su uguaglianza"
	(A B ?primo)
	(A ?secondo C)
	(test (= ?primo ?secondo))
=>
)

(defrule test-not-eq-attivo "Esegue test su diseguaglianza"
	(A B ?primop)
	(A B ?secondop)
	(test (<> ?primop ?secondop))
=>
)


(defrule test-not-eq-silente "Esegue test su diseguaglianza"
	(A ?primo ?)
	(A ?secondo ?)
	(test (<> ?primo ?secondo))
=>
)


(deffacts statoIniziale "Stato iniziale"
	(A B C)
	(A B Z)
)
