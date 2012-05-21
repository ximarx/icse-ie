;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)
;@debug(draw_graph=True)

(defrule negative-primo-attivato "Questa regola deve avere riscontro per passare il test"
	(not (C Z))
	(not (K V))
	(A ?b)
	(not (Y Y))
	(A ?b ?c)
=>
)

(deffacts fatti-iniziali "Attivano negative-attivano, ma non negative-silente"
	(A B)
	(A B C)
)
	

