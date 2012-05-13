(defrule mostraGoal "Mostra il goal"
	(declare (salience 1000))
	(suriva agricoltore lontana)
	(suriva pecora lontana)
	(suriva lupo lontana)
	(suriva cavolo lontana)
=>
)

(defrule tornaAgricoltoreSolo "Sposta l'agricoltore dalla sponda lontana a quella vicina"
	?agricoltore <- (suriva agricoltore lontana)
	(not
		(and
			(suriva pecora lontana)
			(suriva cavolo lontana)
			(suriva lupo vicina)
		)
	)
	(not
		(and
			(suriva lupo lontana)
			(suriva pecora lontana)
			(suriva cavolo vicina)
		)
	)
=>
)

(defrule tornaAgricoltoreConPecoraA "Sposta l'agricoltore e la pecora dalla sponda lontana a quella vicina"
	?agricoltore <- (suriva agricoltore lontana)
	?pecora <- (suriva pecora lontana)
	(suriva cavolo lontana)
	(suriva ? vicina)
=>
)

(defrule tornaAgricoltoreConPecoraB "Sposta l'agricoltore e la pecora dalla sponda lontana a quella vicina"
	?agricoltore <- (suriva agricoltore lontana)
	?pecora <- (suriva pecora lontana)
	(suriva lupo lontana)
	(suriva ? vicina)
=>
)

		 
(defrule mandaPecoraIniziale "Sposta la pecora e l'agricoltore dalla sponda vicina a quella lontana (lasciando lupo e cavolo sulla sponda vicina)"
	?agricoltore <- (suriva agricoltore vicina)
	?pecora <- (suriva pecora vicina)
	(suriva lupo vicina)
	(suriva cavolo vicina)
=>
)


(defrule mandaLupo "Sposta l'agricoltore ed il lupo dalla sponda vicina a quella lontana" 
	?agricoltore <- (suriva agricoltore vicina)
	?lupo <- (suriva lupo vicina)
	(suriva pecora lontana)
	(suriva cavolo vicina)
=>
)

(defrule mandaCavolo "Sposta l'agricoltore ed il cavolo dalla sponda vicina a quella lontana"
	?agricoltore <- (suriva agricoltore vicina)
	?cavolo <- (suriva cavolo vicina)
	(suriva lupo lontana)
=>
)	


(defrule mandaPecoraFinale "Sposta l'agricoltore e la pecora sulla sponda lontana (se lupo e cavolo sono sull'altra sponda)"
	?agricoltore <- (suriva agricoltore vicina)
	?pecora <- (suriva pecora vicina)
	(suriva ?op1 lontana)
	(suriva ~?op1 lontana)
=>
)

(defrule mandaAgricoltoreSolo "Sposta SOLO l'agricoltore dalla sponda distante a quella vicina"
	?agricoltore <- (suriva agricoltore vicina)
	(not (suriva ~agricoltore vicina))
=>
)

(defrule acquisizione "Acquisisce lo stato da tastiera"
	(declare (salience 1000))
	(not (suriva ? ?))
=>
)

(defrule aquisizioneElemento "Acquisisce l'elemento fino a quando il valore immesso non sara' corretto"
	(declare (salience 900))
	?serve <- (serveAcquisizione ?elemento)
	(not (suriva ?elemento ?))
=>
)


(defrule controlloCondizioneErrataPecoraCavolo "Controlla se una condizione e' errata e la corregge"
	(declare (salience 1100))
	(suriva pecora ?riva)
	(suriva cavolo ?riva)
	(suriva agricoltore ~?riva)
	(suriva lupo ~?riva)
=>
)

(defrule controlloCondizioneErrataPecoraLupo "Controlla se una condizione e' errata e la corregge"
	(declare (salience 1100))
	(suriva pecora ?riva)
	(suriva lupo ?riva)
	(suriva agricoltore ~?riva)
	(suriva cavolo ~?riva)
=>
)
