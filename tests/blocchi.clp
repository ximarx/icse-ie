

(defrule sposta "sposta un blocco libero su un altro blocco libero"
	?obiettivo <- (obiettivo sopra-a ?blocco1 ?blocco2)
	(blocco ?blocco1)
	(blocco ?blocco2)
	(sopra-a niente ?blocco1)
	?pila1 <- (sopra-a ?blocco1 ?blocco3)
	?pila2 <- (sopra-a niente ?blocco2)
=>
	(printout t "Sposto " ?blocco1 " sopra a " ?blocco2 crlf)
	(retract ?obiettivo)
	(retract ?pila1 ?pila2)
	(assert (sopra-a ?blocco1 ?blocco2))
)

(defrule sposta-sul-piano "sposta un blocco libero (sopra un altro blocco) sul piano"
	?obiettivo <- (obiettivo sopra-a ?blocco1 piano)
	(blocco ?blocco1)
	(blocco ?blocco2)
	(sopra-a niente ?blocco1)
	?pila <- (sopra-a ?blocco1 ?blocco2)
=>
	(printout t "Sposto " ?blocco1 " sul piano" crlf)
	(retract ?obiettivo)
	(retract ?pila)
	(assert 
		(sopra-a ?blocco1 piano)
		(sopra-a niente ?blocco2)
	)
)

(defrule libera-blocco-partenza "comunica l'intenzione di liberare il blocco di partenza"
	?obiettivo <- (obiettivo sopra-a ?blocco1 ?bloccosotto)
	(blocco ?blocco1)
	(blocco ?blocco2)
	(sopra-a ?blocco2 ?blocco1)
=>
	(printout t "Per poter mettere " ?blocco1 " sopra a " ?bloccosotto ", devo spostare " ?blocco2 " da sopra " ?blocco1 " sul piano" crlf)
	(assert (obiettivo sopra-a ?blocco2 piano))
)


(defrule libera-blocco-arrivo "comunica l'intenzione di liberare il blocco di arrivo"
	?obiettivo <- (obiettivo sopra-a ?bloccosopra ?blocco2)
	(blocco ?blocco2)
	(blocco ?blocco3)
	(sopra-a ?blocco3 ?blocco2)
=>
	(printout t "Per poter mettere " ?bloccosopra " sopra a " ?blocco2 ", devo spostare " ?blocco3 " da sopra " ?blocco2 " sul piano" crlf)
	(assert (obiettivo sopra-a ?blocco3 piano))
)


(deffacts stato-iniziale "A/B/C D/E/F, voglio mettere C su F"
	(blocco A)
	(blocco B)
	(blocco C)
	(blocco D)
	(blocco E)
	(blocco F)
	(sopra-a niente A)
	(sopra-a A B)
	(sopra-a B C)
	(sopra-a C piano)
	(sopra-a niente D)
	(sopra-a D E)
	(sopra-a E F)
	(sopra-a F piano)
	(obiettivo sopra-a C F)
)





