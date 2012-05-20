;@include(moduli/domande.clp)
;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)

(deffacts inizio
	(stato inizio)
	(spiegazione " ")
)


(defrule Presentazione
	(declare (salience 1000))
	(stato inizio)
=>
	(printout t "Sistema per la diagnosi di malattie del fegato" crlf)
)

(defrule Visualizza_Diagnosi
	(diagnosi ?malattia)
=>
	(printout t crlf "        Diagnosi: " ?malattia crlf)
)

(defrule Visualizza_Spiegazioni-si
	?visualizza <- (visualizza-spiegazione-diagnosi si)
	(spiegazione ?testo-spiegazione)
=>
	(printout t ?testo-spiegazione crlf)
	(retract ?visualizza)
)

(defrule Visualizza_Spiegazioni-no
	?visualizza <- (visualizza-spiegazione-diagnosi no)
=>
	(retract ?visualizza)
)

(defrule Chiedi_Per_Spiegazioni
	(declare (salience -2000))
	(diagnosi ?)
=>
	(assert
		(domanda richiesta-spiegazioni)
		(testo-domanda richiesta-spiegazioni "Vuoi sapere come sono arrivato alla diagnosi? (si/no)")
		(risposta-valore-ammesso richiesta-spiegazioni si)
		(risposta-valore-ammesso richiesta-spiegazioni no)
		(risposta-in richiesta-spiegazioni visualizza-spiegazione-diagnosi)
	)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; REGOLE
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule Sindrome_di_Gilbert-stress
	(SINTOMO_ittero-sclerale si)
	(SINTOMO_febbre no)
	(SINTOMO_stress si)
	(not (diagnosi Sindrome_di_Gilbert))
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi Sindrome_di_Gilbert))
	(bind ?n-spiegazione "\tL'ittero sclerale e l'assenza di febbre fanno pensare che si tratti di Sindrome di Gilbert\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)

(defrule Sindrome_di_Gilbert-digiuno
	(SINTOMO_ittero-sclerale si)
	(SINTOMO_febbre no)
	(SINTOMO_digiuno si)
	(not (diagnosi Sindrome_di_Gilbert))
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi "Sindrome di Gilbert"))
	(bind ?n-spiegazione "\tL'ittero sclerale e l'assenza di febbre fanno pensare che si tratti di Sindrome di Gilbert\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)



(defrule Domanda_Febbre
	(declare (salience -100))
	(not (SINTOMO_febbre ?))
=>
	(assert
		(domanda ha-febbre)
		(testo-domanda ha-febbre "Il paziente ha febbre? (si/no)")
		(risposta-valore-ammesso ha-febbre si)
		(risposta-valore-ammesso ha-febbre no)
		(risposta-in ha-febbre SINTOMO_febbre)
	)
)


(defrule Epatite_Acuta_Virale
	(SINTOMO_ittero-franco si)
	(SINTOMO_febbre si)
	(paziente-giovane si)
	(SINTOMO_stanchezza si)
	(SINTOMO_dispepsia si)
	(SINTOMO_aumento-fegato si)
	(not (diagnosi Epatite_Acuta_Virale))
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi Epatite_Acuta_Virale))
	(bind ?n-spiegazione "\tL'ittero franco, la febbre, la stanchezza, la dispepsia, l'aumento delle dimensioni fegato e la giovane eta' del paziente fanno pensare che si tratti di Epatite acuta virale\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)


(defrule Colecistite
	(not (diagnosi Colecistite))
	(SINTOMO_ittero-franco si)
	(SINTOMO_febbre si)
	(paziente-giovane no)
	(SINTOMO_dolori-ricorrenti si)
	(SINTOMO_dolore-coleciste si)
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi Colecistite))
	(bind ?n-spiegazione "\tL'ittero franco, la febbre, i dolori ricorrenti e quelli della coleciste, insieme alla eta' media-avanzata del paziente fanno pensare che si tratti di Sindrome di Colecistite\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)


(defrule Cirrosi_Alcolica
	(not (diagnosi Cirrosi_Alcolica))
	(SINTOMO_ittero-franco si)
	(SINTOMO_febbre no)
	(paziente-giovane no)
	(uso-alcool si)
	(SINTOMO_aumento-fegato si)
	(SINTOMO_aumento-milza si)
	?spiegazione <- (spiegazione ?testo-spiegazione)
	=>
	(assert (diagnosi Cirrosi_Alcolica))
	(bind ?n-spiegazione "\tL'ittero franco, l'assenza di febbre, l'uso di alcool, l'eta' giovane del paziente, l'aumento di dimensioni del fegato e della milza fanno pensare che si tratti di Cirrosi Alcolica\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)


(defrule Ignota
	(declare (salience -1000))
	(not (diagnosi ?))
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi Malattia_ignota))
	(bind ?n-spiegazione "\tNon ci sono abbastanza elementi per effetuare una diagnosi\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)


(defrule Sintomo_Ittero_Franco
	(SINTOMO_occhi-gialli si)
	(SINTOMO_colorito-giallo si)
	(not (SINTOMO_ittero-franco ?)) ; la presenza di "spiegazioni" mi porta a loop, uso questo per evitare
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (SINTOMO_ittero-franco si))
	(bind ?n-spiegazione "\tGli occhi gialli ed il colorito giallo indicano ittero franco\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)

(defrule Sintomo_Ittero_Sclerale
	(SINTOMO_occhi-gialli si)
	(SINTOMO_colorito-giallo no)
	(not (SINTOMO_ittero-sclerale ?)) 
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (SINTOMO_ittero-sclerale si))
	(bind ?n-spiegazione "\tGli occhi gialli ed il colorito normale indicano ittero franco\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)

(defrule Domanda_Occhi_Gialli
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_occhi-gialli ?))
=>
	(assert
		(domanda ha-occhi-gialli)
		(testo-domanda ha-occhi-gialli "Il paziente ha gli occhi gialli? (si/no)")
		(testo-spiegazione ha-occhi-gialli "Serve per verificare la presenza di ittero")
		(risposta-valore-ammesso ha-occhi-gialli si)
		(risposta-valore-ammesso ha-occhi-gialli no)
		(risposta-in ha-occhi-gialli SINTOMO_occhi-gialli)
	)
)

(defrule Domanda_Colorito_Giallo
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_colorito-giallo ?))
=>
	(assert
		(domanda ha-colorito-giallo)
		(testo-domanda ha-colorito-giallo "Il paziente ha il colorito giallo? (si/no)")
		(testo-spiegazione ha-colorito-giallo "Serve per distinguere l'ittero sclerale da quello franco")
		(risposta-valore-ammesso ha-colorito-giallo si)
		(risposta-valore-ammesso ha-colorito-giallo no)
		(risposta-in ha-colorito-giallo SINTOMO_colorito-giallo)
	)
)

(defrule Domanda_Sintomo_Stress
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_stress ?))
=>
	(assert
		(domanda ha-stress)
		(testo-domanda ha-stress "Il paziente e' stressato? (si/no)")
		(testo-spiegazione ha-stress "La presenza di stress o digiuno fa propendere per la Sindrome di Gilbert")
		(risposta-valore-ammesso ha-stress si)
		(risposta-valore-ammesso ha-stress no)
		(risposta-in ha-stress SINTOMO_stress)
	)
)
	
(defrule Domanda_Sintomo_Digiuno
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_digiuno ?))
=>
	(assert
		(domanda ha-digiuno)
		(testo-domanda ha-digiuno "Il paziente digiuna? (si/no)")
		(testo-spiegazione ha-digiuno "La presenza di stress o digiuno fa propendere per la Sindrome di Gilbert")
		(risposta-valore-ammesso ha-digiuno si)
		(risposta-valore-ammesso ha-digiuno no)
		(risposta-in ha-digiuno SINTOMO_digiuno)
	)
)


(defrule Domanda_Paziente_Giovane
	(declare (salience -100))
	(not (diagnosi ?))
	(not (paziente-giovane ?))
	=>
	(assert
		(domanda paziente-giovane)
		(testo-domanda paziente-giovane "Il paziente e' giovane? (si/no)")
		(risposta-valore-ammesso paziente-giovane si)
		(risposta-valore-ammesso paziente-giovane no)
		(risposta-in paziente-giovane paziente-giovane)
	)
)	
	
(defrule Domanda_Sintomo_Stanchezza
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_stanchezza ?))
=>
	(assert
		(domanda ha-stanchezza)
		(testo-domanda ha-stanchezza "Il paziente e' stanco? (si/no)")
		(testo-spiegazione ha-stanchezza "E' indice di epatite acuta virale")
		(risposta-valore-ammesso ha-stanchezza si)
		(risposta-valore-ammesso ha-stanchezza no)
		(risposta-in ha-stanchezza SINTOMO_stanchezza)
	)	
)


(defrule Domanda_Sintomo_Dispepsia
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_dispepsia ?))
=>
	(assert
		(domanda ha-dispepsia)
		(testo-domanda ha-dispepsia "Il paziente ha dispepsia? (si/no)")
		(testo-spiegazione ha-dispepsia "Potrebbe essere indice di epatite acuta virale")
		(risposta-valore-ammesso ha-dispepsia si)
		(risposta-valore-ammesso ha-dispepsia no)
		(risposta-in ha-dispepsia SINTOMO_dispepsia)
	)	
)


(defrule Domanda_Sintomo_Aumento_Fegato
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_aumento-fegato ?))
=>
	(assert
		(domanda ha-aumento-fegato)
		(testo-domanda ha-aumento-fegato "Il paziente ha aumento del fegato? (si/no)")
		(testo-spiegazione ha-aumento-fegato "Aiuta a distinguere epatite e cirrosi da altre malattie")
		(risposta-valore-ammesso ha-aumento-fegato si)
		(risposta-valore-ammesso ha-aumento-fegato no)
		(risposta-in ha-aumento-fegato SINTOMO_aumento-fegato)
	)	
)


(defrule Domanda_Sintomo_Dolori_Ricorrenti
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_dolori-ricorrenti ?))
=>
	(assert
		(domanda ha-dolori-ricorrenti)
		(testo-domanda ha-dolori-ricorrenti "Il paziente ha dolori ricorrenti? (si/no)")
		(testo-spiegazione ha-dolori-ricorrenti "Potrebbe servire per confermare la colecistite")
		(risposta-valore-ammesso ha-dolori-ricorrenti si)
		(risposta-valore-ammesso ha-dolori-ricorrenti no)
		(risposta-in ha-dolori-ricorrenti SINTOMO_dolori-ricorrenti)
	)	
)


(defrule Domanda_Sintomo_Dolore_Coleciste
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_dolore-coleciste ?))
=>
	(assert
		(domanda ha-dolore-coleciste)
		(testo-domanda ha-dolore-coleciste "Il paziente ha dolore coleciste? (si/no)")
		(testo-spiegazione ha-dolore-coleciste "Conforme la colecistite")
		(risposta-valore-ammesso ha-dolore-coleciste si)
		(risposta-valore-ammesso ha-dolore-coleciste no)
		(risposta-in ha-dolore-coleciste SINTOMO_dolore-coleciste)
	)	
)


(defrule Domanda_Uso_Alcool
	(declare (salience -100))
	(not (diagnosi ?))
	(not (uso-alcool ?))
	=>
	(assert
		(domanda ha-uso-alcool)
		(testo-domanda ha-uso-alcool "Il paziente fa uso di alcool? (si/no)")
		(testo-spiegazione ha-uso-alcool "Farebbe pensare alla cirrosi")
		(risposta-valore-ammesso ha-uso-alcool si)
		(risposta-valore-ammesso ha-uso-alcool no)
		(risposta-in ha-uso-alcool uso-alcool)
	)	
)


(defrule Domanda_Aumento_Milza
	(declare (salience -100))
	(not (diagnosi ?))
	(not (SINTOMO_aumento-milza ?))
=>
	(assert
		(domanda ha-aumento-milza)
		(testo-domanda ha-aumento-milza "Il paziente ha aumento milza? (si/no)")
		(testo-spiegazione ha-aumento-milza "E' un sintomo tipico di cirrosi")
		(risposta-valore-ammesso ha-aumento-milza si)
		(risposta-valore-ammesso ha-aumento-milza no)
		(risposta-in ha-aumento-milza SINTOMO_aumento-milza)
	)	
)

