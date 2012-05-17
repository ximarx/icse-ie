
(defrule azione-printout "Stampa qualcosa"
	?match <- (A B C)
=>
	(bind ?variabile-temp (1 2 3))
	(printout t "Questa stringa e' cosi fica che quasi no la riconoscevo" crlf)
	(printout t "Proviamo" crlf "la" crlf "sostituzione" crlf "del" crlf "crlf" crlf)
	(printout t "Ultima riga" crlf)
	(printout t ?variabile-temp "una scritta dopo la variabile")
	(assert (D E F) ?variabile-temp)
	(retract ?match (D E F) ?variabile-temp)
)

(defrule azione-secondaria
	(D E F)
=>
	(printout t "Ho trovato l'azione secondaria")
)

(deffacts iniziali
	(A B C)
)