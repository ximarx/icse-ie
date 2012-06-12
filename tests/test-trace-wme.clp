;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)
;@debug(draw_graph=True)

(defrule test-trigger-event
	?f <- (A B ?)
=>
	(trace-wme ?f)
)

(deffacts statoIniziale "Stato iniziale"
	(A B C)
)
