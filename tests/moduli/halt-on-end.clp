
(defrule halt-on-end "Blocca l'esecuzione prima di terminare l'esecuzione del sistema"
	(declare (salience -10000))
	(halt-on-end-assertion)
=>
	(printout t crlf "Premere invio per continuare..." crlf)
	(read)
)

(deffacts halt-on-end-deffacts
	(halt-on-end-assertion)
)
