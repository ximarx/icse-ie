;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)
;@debug(draw_graph=True)


(defrule negative-attivato "Questa regola deve avere riscontro per passare il test"
	(A ?b)
	(not (Z ?b A))
=>
)

(defrule negative-silente "Questa regola non deve avere riscontro per passare il test"
	(A ?b)
	(not (A ?b C))
=>
)

(defrule negative-primo-attivato "Questa regola deve avere riscontro per passare il test"
	(not (C Z))
	(A ?b)
=>
)

(defrule negative-primo-silente "Questa regola non deve avere riscontro per passare il test"
	(not (A B C))
	(A ?b)
=>
)

(deffacts fatti-iniziali "Attivano negative-attivano, ma non negative-silente"
	(A B)
	(A B C)
)
	

