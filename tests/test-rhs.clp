
(defrule azione-printout "Stampa qualcosa"
	(A B C)
=>
	(bind ?variabile-temp (1 2 3))
	(printout t "Questa stringa e' cosi fica che quasi no la riconoscevo" crlf)
	(printout t "Proviamo" crlf "la" crlf "sostituzione" crlf "del" crlf "crlf" crlf)
	(printout t "Ultima riga" crlf)
	(printout t ?variabile-temp "una scritta dopo la variabile")
)

(deffacts iniziali
	(A B C)
)