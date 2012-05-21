;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)
;@debug(draw_graph=True)

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