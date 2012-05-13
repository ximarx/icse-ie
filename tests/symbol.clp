(defrule mostra-goal "Mostra il goal"
	(declare (salience 1000))
	(suriva agricoltore lontana)
	(suriva pecora lontana)
	(suriva lupo lontana)
	(suriva cavolo lontana)
=>
)

(defrule aquisizione-elemento "Acquisisce l'elemento fino a quando il valore immesso non sara' corretto"
	(declare (salience 900))
	?serve <- (serve-acquisizione ?elemento)
	(not (suriva ?elemento ?))
=>
)

(deffacts stato-iniziale "Stato iniziale"
	(serve-acquisizione agricoltore)
	(serve-acquisizione lupo)
	(serve-acquisizione cavolo)
	(serve-acquisizione pecora)
)

