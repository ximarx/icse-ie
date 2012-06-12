;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)
;@debug(draw_graph=True)


(defrule attivata "regola attivata"
	(declare (salience 100))
	?f <- (A B C)
=>
	(printout t "Ho attivato la regola con " ?f crlf)
)

(defrule esegue-refresh "refresha la regola, una volta sola"
	(declare (salience -100))
	?f <- (fatto no)
=>
	(printout t "Eseguo il refresh" crlf)
	(retract ?f)
	(refresh attivata)
	(assert (fatto si))
)

(deffacts iniziale
	(A B C)
	(fatto no)
)