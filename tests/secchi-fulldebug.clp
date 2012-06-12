;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)

;@include(secchi.clp)


(defrule trace-regola-uno-e-due "mostra il grafico delle regole riempi-uno e riempi-due"
	(declare (salience -9999))
	(not (rule-traced si))
=>
	(assert (rule-traced si))
	(trace-rule riempi-uno riempi-due)
)


(defrule trace-wme "refresha la regola, una volta sola"
	(declare (salience -9999))
	?f <- (rule-traced si)
=>
	(trace-wme ?f)
)

