;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)
;@debug(draw_graph=True)

(defrule azione-printout "Stampa qualcosa"
	?match <- (A B C)
=>
	(bind ?variabile-temp 2)
	(printout t "Questa stringa e' cosi fica che quasi no la riconoscevo" crlf)
	(printout t "Proviamo" crlf "la" crlf "sostituzione" crlf "del" crlf "crlf" crlf)
	(printout t "Ultima riga" crlf)
	(printout t ?variabile-temp "una scritta dopo la variabile")
	(assert (D E F) (1 ?variabile-temp L))
	(retract ?match)
)

(defrule azione-secondaria
	(D E F)
=>
	(printout t "Ho trovato l'azione secondaria")
)

(deffacts iniziali
	(A B C)
)