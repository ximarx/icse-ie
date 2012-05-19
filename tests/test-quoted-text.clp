
(defrule testo-quotato-CORRETTO "Il commento dovrebbe essere letto"
	(data ?testo-quotato)
=>
	(printout t "Hai trovato il testo quotato: " crlf "   ->   " ?testo-quotato crlf)
)

(defrule trova-testo-quotato-SBAGLIATO "Il commento dovrebbe essere letto"
	(data ? ?testo-quotato ?)
=>
	(printout t "Hai trovato il testo quotato: " crlf "   ->   " ?testo-quotato crlf)
)


(deffacts iniziale
	(data "il mio favoloso testo quotato")
)