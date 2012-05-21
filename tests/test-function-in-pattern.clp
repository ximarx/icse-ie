;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)
;@debug(draw_graph=True)


(defrule function-attiva "Deve essere attiva per superare il test"
	(A ?var)
	(A =(+ 1 ?var) B)
=>
)

(defrule function-silente "Non deve essere attiva per superare il test"
	(A =(+ 1 1.1) B)
=>
)


(deffacts iniziali
	(A 1)
	(A 2 B)
)
