
(defrule test-eq-attivo "Esegue test su uguaglianza"
	(A B ?primo)
	(A B ?secondo)
	(test (eq ?primo ?secondo))
=>
)

(defrule test-eq-silente "Esegue test su uguaglianza"
	(A B ?primo)
	(A ?secondo C)
	(test (eq ?primo ?secondo))
=>
)

(defrule test-not-eq-attivo "Esegue test su diseguaglianza"
	(A B ?primop)
	(A B ?secondop)
	(test (neq ?primop ?secondop))
=>
)


(defrule test-not-eq-silente "Esegue test su diseguaglianza"
	(A ?primo ?terzo)
	(A ?secondo ?)
	(test (neq ?primo ?secondo))
=>
)

(defrule test-con-funzione-attiva "Attiva"
	(N ?num1)
	(N ?num2)
	(test (= ?num2 (+ 4 ?num1)))
=>
)

(defrule test-con-funzione-silente "Silente"
	(N ?num1)
	(N ?num2)
	(test (= ?num2 (+ 8 ?num1)))
=>
)


(deffacts statoIniziale "Stato iniziale"
	(A B C)
	(A B Z)
	(N 1)
	(N 5)
)
