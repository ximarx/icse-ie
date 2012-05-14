

(defrule sposta "sposta un blocco libero su un altro blocco libero"
	?obiettivo <- (obiettivo sopra-a ?blocco1 ?blocco2)
	(blocco ?blocco1)
	(blocco ?blocco2)
	(sopra-a niente ?blocco1)
	?pila1 <- (sopra-a ?blocco1 ?blocco3)
	?pila2 <- (sopra-a niente ?blocco2)
=>
)

(defrule sposta-sul-piano "sposta un blocco libero (sopra un altro blocco) sul piano"
	?obiettivo <- (obiettivo sopra-a ?blocco1 piano)
	(blocco ?blocco1)
	(blocco ?blocco2)
	(sopra-a niente ?blocco1)
	?pila <- (sopra-a ?blocco1 ?blocco2)
=>
)

(defrule libera-blocco-partenza "comunica l'intenzione di liberare il blocco di partenza"
	?obiettivo <- (obiettivo sopra-a ?blocco1 ?)
	(blocco ?blocco1)
	(blocco ?blocco2)
	(sopra-a ?blocco2 ?blocco1)
=>
)


(defrule libera-blocco-arrivo "comunica l'intenzione di liberare il blocco di arrivo"
	?obiettivo <- (obiettivo sopra-a ? ?blocco2)
	(blocco ?blocco2)
	(blocco ?blocco3)
	(sopra-a ?blocco3 ?blocco2)
=>
)


(deffacts stato-iniziale "A/B/C D/E/F, voglia mettere C su F"
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





