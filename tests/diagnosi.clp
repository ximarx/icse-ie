
(deffacts inizio
	(stato inizio)
	(spiegazione "\t")
)


(defrule Presentazione
	(declare (salience 1000))
	(stato inizio)
=>
	(printout t "Sistema per la diagnosi di malattie" crlf)
)

(defrule Visualizza_Diagnosi
	(declare (salience 10))
	(diagnosi ?malattia)
=>
	(printout t crlf "        Diagnosi: " ?malattia crlf)
)

(defrule Visualizza_Spiegazioni-si
	?visualizza <- (visualizza-spiegazioni-diagnosi si)
	(spiegazione ?testo-spiegazione)
=>
	(printout t ?testo-spiegazione crlf)
)

(defrule Visualizza_Spiegazioni-no
	?visualizza <- (visualizza-spiegazioni-diagnosi no)
=>
)

(defrule Chiedi_Per_Spiegazioni
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
	(declare (salience 10)) 
	(SINTOMO_ittero-sclerale si)
	(SINTOMO_febbre no)
	(SINTOMO_digiuno si)
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi "Sindrome di Gilbert"))
	(bind ?n-spiegazione "\tL'ittero sclerale e l'assenza di febbre fanno pensare che si tratti di Sindrome di Gilbert\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)

(defrule Sindrome_di_Gilbert-digiuno
	(declare (salience 10)) 
	(SINTOMO_ittero-sclerale si)
	(SINTOMO_febbre no)
	(SINTOMO_digiuno si)
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi "Sindrome di Gilbert"))
	(bind ?n-spiegazione "\tL'ittero sclerale e l'assenza di febbre fanno pensare che si tratti di Sindrome di Gilbert\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)



(defrule Domanda_Febbre
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
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi "Epatite_Acuta_Virale"))
	(bind ?n-spiegazione "\tL'ittero franco, la febbre, la stanchezza, la dispepsia, l'aumento delle dimensioni fegato e la giovane eta' del paziente fanno pensare che si tratti di Epatite acuta virale\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)


(defrule Colecistite
	(SINTOMO_ittero-franco si)
	(SINTOMO_febbre si)
	(paziente-giovane no)
	(SINTOMO_dolori-ricorrenti si)
	(SINTOMO_dolore-coleciste si)
	?spiegazione <- (spiegazione ?testo-spiegazione)
=>
	(assert (diagnosi "Colecistite"))
	(bind ?n-spiegazione "\tL'ittero franco, la febbre, i dolori ricorrenti e quelli della coleciste, insieme alla eta' media-avanzata del paziente fanno pensare che si tratti di Sindrome di Colecistite\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)


(defrule Cirrosi_Alcolica
	(SINTOMO_ittero-franco si)
	(SINTOMO_febbre no)
	(paziente-giovane no)
	(uso-alcool si)
	(SINTOMO_aumento-fegato si)
	(SINTOMO_aumento-milza si)
	?spiegazione <- (spiegazione ?testo-spiegazione)
	=>
	(assert (diagnosi "Cirrosi Alcolica"))
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
	(assert (diagnosi "Malattia ignota"))
	(bind ?n-spiegazione "\tNon ci sono abbastanza elementi per effetuare una diagnosi\n")
	(bind ?testo-spiegazione (str-cat ?testo-spiegazione ?n-spiegazione))
	(retract ?spiegazione)
	(assert (spiegazione ?testo-spiegazione)) 
)



;@INCLUDE(modulo-domande.clp)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; MODULO DI DOMANDA:
;;	permette di porre una domanda all'utente
;;	come se fosse una funzione
;;
;;	Per attivarlo e' necessario impostare:
;;
;;		(domanda ID_DOMANDA) ** RICHIESTO **
;;			ID_DOMANDA dovra' essere condiviso con tutti
;;				gli elementi della stessa domanda
;;
;;		(testo-domanda ID_DOMANDA TESTO_DOMANDA) ** RICHIESTO **
;;			TESTO_DOMANDA testo che verra' posto
;;				all'utente
;;
;;		(testo-spiegazione ID_DOMANDA TESTO_SPIEGAZIONE) ** OPZIONALE **
;;			TESTO_SPIEGAZIONE il testo che verra'
;;				visualizzato come spiegazione della domanda
;;
;;		(risposta-valore-ammesso ID_DOMANDA VALORE) ** RICHIESTO: almeno 1 **
;;			VALORE un valore di risposta ammesso
;;				
;;		(risposta-in ID_DOMANDA POSIZIONE_RISPOSTA) ** RICHIESTO **
;;			POSIZIONE_RISPOSTA rappresenta la prima componente
;;				del nuovo fatto che verra' asserito
;;				in seguito ad una risposta convalidata
;;				fra i valori ammessi. Il nuovo fatto
;;				asserito sara' in forma:
;;				(POSIZIONE_RISPOSTA RISPOSTA_DELL_UTENTE)
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;		

(defrule Domanda_poni-senza-spiegazione
	(declare (salience 996))
	(domanda ?id-domanda)
	(testo-domanda ?id-domanda ?testo-domanda)
=>
	(printout t ?testo-domanda " ")
	(bind ?risposta (read))
	(printout t crlf) ; vado a capo dopo la risposta
	(assert (risposta-domanda ?id-domanda ?risposta))
)

(defrule Domanda_poni-con-spiegazione
	(declare (salience 997))
	(domanda ?id-domanda)
	(testo-domanda ?id-domanda ?testo-domanda)
	(testo-spiegazione ?id-domanda ?testo-spiegazione)
=>
	(printout t ?testo-domanda crlf "       " ?testo-spiegazione crlf)
	(bind ?risposta (read))
	(printout t crlf) ; vado a capo dopo la risposta
	(assert (risposta-domanda ?id-domanda ?risposta))
)


(defrule Domanda_controllo-risposta-valida
	(declare (salience 998))
	?f-domanda <- (domanda ?id-domanda)
	?f-risposta <- (risposta-domanda ?id-domanda ?risposta)
	?f-valore <- (risposta-valore-ammesso ?id-domanda ?risposta)
	?f-posizione <- (risposta-in ?id-domanda ?posizione)
=>
	(assert (?posizione ?risposta))
	(retract ?f-risposta ?f-valore ?f-posizione ?f-domanda)
)

(defrule Domanda_controllo-risposta-non-valida
	(declare (salience 998))
	?f-domanda <- (domanda ?id-domanda)
	?f-risposta <- (risposta-domanda ?id-domanda ?risposta)
	(not (risposta-valore-ammesso ?id-domanda ?risposta))
=>
	(printout t "La risposta non e' valida" crlf)
	(retract ?f-risposta ?f-domanda)
	(assert (domanda ?id-domanda)) ; ritratto e ri-asserisco lo stesso id per attivare di nuovo la regola
)

(defrule Domanda_rimozione-valori-inutili
	(declare (salience 1200))
	?f-valore <- (risposta-valore-ammesso ?id-domanda ?)
	(not (domanda ?id-domanda))
=>
	(retract ?f-valore)
)

(defrule Domanda_rimozione-risposta-in-inutili
	(declare (salience 1200))
	?f-risposta-in <- (risposta-in ?id-domanda ?)
	(not (domanda ?id-domanda))
=>
	(retract ?f-risposta-in)
)

(defrule Domanda_rimozione-testo-inutili
	(declare (salience 1200))
	?f-testo-domanda <- (testo-domanda ?id-domanda ?)
	(not (domanda ?id-domanda))	
=>
	(retract ?f-testo-domanda)
)

(defrule Domanda_rimozione-spiegazione-inutili
	(declare (salience 1200))
	?f-spiegazione-domanda <- (spiegazione-domanda ?id-domanda ?)
	(not (domanda ?id-domanda))	
=>
	(retract ?f-spiegazione-domanda)
)


