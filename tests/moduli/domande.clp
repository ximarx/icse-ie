
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
	?f-spiegazione-domanda <- (testo-spiegazione ?id-domanda ?)
	(not (domanda ?id-domanda))	
=>
	(retract ?f-spiegazione-domanda)
)
