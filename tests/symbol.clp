(defrule mostra-goal "Mostra il goal"
	(declare (salience 1000))
	(su-riva agricoltore lontana)
	(su-riva pecora lontana)
	(su-riva lupo lontana)
	(su-riva cavolo lontana)
=>
)

(defrule aquisizione-elemento "Acquisisce l'elemento fino a quando il valore immesso non sara' corretto"
	(declare (salience 900))
	?serve <- (serve-acquisizione ?elemento)
	(not (su-riva ?elemento ?))
=>
)

(deffacts stato-iniziale "Stato iniziale"
	(serve-acquisizione agricoltore)
	(serve-acquisizione lupo)
	(serve-acquisizione cavolo)
	(serve-acquisizione pecora)
)

(defrule torna-agricoltore-solo "Sposta l'agricoltore dalla sponda lontana a quella vicina"
	?agricoltore <- (su-riva agricoltore lontana)
	(not
		(and
			(su-riva pecora lontana)
			(su-riva cavolo lontana)
			(su-riva lupo vicina)
		)
	)
	(not
		(and
			(su-riva lupo lontana)
			(su-riva pecora lontana)
			(su-riva cavolo vicina)
		)
	)
=>
)
