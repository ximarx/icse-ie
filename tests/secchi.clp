
; Riempie il PRIMO(4L) secchio al massimo (se non lo e' gia')
(defrule riempi-uno
	(capienza uno ?capienza)
	(status
			?id 
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(not (status ~?id ? ? ?capienza ?r-secondo ?))
	?massimo <- (massimo-id ?nextid)
	(test (< ?r-primo ?capienza))  ; questo assicura che non sia gia' al massimo
=>
	(printout t "                                 [provo riempi-uno: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
	(assert (status
				?nextid 
				?new-depth
				?id
				?capienza
				?r-secondo
				riempi-uno
			)
		)
)



; Riempie il SECONDO(3L) secchio al massimo (se non lo e' gia')
(defrule riempi-due
	(capienza due ?capienza)
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(not (status ~?id ? ? ?r-primo ?capienza ?))
	?massimo <- (massimo-id ?nextid)
	(test (< ?r-secondo ?capienza))  ; questo assicura che non sia gia' al massimo
=>
	(printout t "                                 [provo riempi-due: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid =(+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
	(assert (status
				?nextid 
				?new-depth
				?id
				?r-primo
				?capienza
				riempi-due
			)
		)
)

; Svuota il PRIMO(4L) secchio, (se non lo e' gia)
(defrule svuota-uno
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(not (status ~?id ? ? 0 ?r-secondo ?))
	?massimo <- (massimo-id ?nextid)
	(test (> ?r-primo 0))  ; questo assicura che non sia gia' vuoto
=>
	(printout t "                                 [provo svuota-uno: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
	(assert (status
				?nextid 
				?new-depth
				?id
				0
				?r-secondo
				svuota-uno
			)
		)
)

; Svuota il SECONDO(3L) secchio, (se non lo e' gia)
(defrule svuota-due
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(not (status ~?id ? ? ?r-primo 0 ?))
	?massimo <- (massimo-id ?nextid)
	(test (> ?r-secondo 0))  ; questo assicura che non sia gia' vuoto
=>
	(printout t "                                 [provo svuota-due: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
	(assert (status
				?nextid 
				?new-depth
				?id
				?r-primo
				0
				svuota-due
			)
		)
)


; Versa il SECONDO(3L) secchio nel PRIMO(4L) (assicurandosi che il primo possa contenere tutto)
(defrule versa-tutto-due-in-uno
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	?massimo <- (massimo-id ?nextid)
	(capienza uno ?capienza)
	(test (>= ?capienza (+ ?r-primo ?r-secondo)))
	(not (status ~?id ? ? =(+ ?r-primo ?r-secondo) 0 ?))
=>
	(printout t "                                 [provo versa-tutto-due-in-uno: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
	(bind ?new-r-primo (+ ?r-primo ?r-secondo))
	(assert (status
				?nextid 
				?new-depth
				?id
				?new-r-primo
				0
				versa-tutto-due-in-uno
			)
		)
)	
	
; Versa il PRIMO(4L) secchio nel SECONDO(3L) (assicurandosi che il secondo possa contenere tutto)
(defrule versa-tutto-uno-in-due
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	?massimo <- (massimo-id ?nextid)
	(capienza due ?capienza)
	(test (>= ?capienza (+ ?r-primo ?r-secondo)))
	(not (status ~?id ? ? 0 =(+ ?r-primo ?r-secondo) ?))
=>
	(printout t "                                 [provo versa-tutto-uno-in-due: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
	(bind ?new-r-secondo (+ ?r-primo ?r-secondo))
	(assert (status
				?nextid 
				?new-depth
				?id
				0
				?new-r-secondo
				versa-tutto-uno-in-due
			)
		)
)


; Versa il SECONDO(3L) secchio nel PRIMO(4L) fino a riempirlo (conservando il resto)
(defrule versa-due-in-uno-fino-a-pieno
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	?massimo <- (massimo-id ?nextid)
	(capienza uno ?capienza)
	(test (< ?capienza (+ ?r-primo ?r-secondo)))
	(not (status ~?id ? ? ?capienza =(- ?r-secondo (- ?capienza ?r-primo) ) ?))
=>
	(printout t "                                 [provo versa-due-in-uno-fino-a-pieno: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
    (bind ?versato (- ?capienza ?r-primo))
    (bind ?new-r-secondo (- ?r-secondo ?versato))
	(assert (status
				?nextid 
				?new-depth
				?id
				?capienza
				?new-r-secondo
				versa-due-in-uno-fino-a-pieno
			)
		)
)	

; Versa il PRIMO(4L) secchio nel SECONDO(3L) fino a riempirlo (conservando il resto)
(defrule versa-uno-in-due-fino-a-pieno
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	?massimo <- (massimo-id ?nextid)
	(capienza due ?capienza)
	(test (< ?capienza (+ ?r-primo ?r-secondo)))
	(not (status ~?id ? ? =(- ?r-primo (- ?capienza ?r-secondo)) ?capienza ?))
=>
	(printout t "                                 [provo versa-uno-in-due-fino-a-pieno: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		depth: " ?depth crlf)
	(printout t "                                 		parent: " ?parent crlf)
	(printout t "                                 		1: " ?r-primo crlf)
	(printout t "                                 		2: " ?r-secondo crlf)
	(printout t "                                 		ultima: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
	(assert (massimo-id ?new-nextid ))
	(bind ?new-depth (+ ?depth 1))
    (bind ?versato (- ?capienza ?r-secondo))
    (bind ?new-r-primo (- ?r-primo ?versato))
	(assert (status
				?nextid 
				?new-depth
				?id
				?new-r-primo
				?capienza
				versa-uno-in-due-fino-a-pieno
			)
		)
)	


(defrule rimozione-stati-duplicati
	(declare (salience 100))
	(status ?id ?depth ? ?r-primo ?r-secondo ?)
	?duplicato <- (status ?id-duplicato ?depth-duplicato ? ?r-primo-duplicato ?r-secondo-duplicato ?)
	(test (< ?depth ?depth-duplicato))
	(test (= ?r-primo ?r-primo-duplicato))
	(test (= ?r-secondo ?r-secondo-duplicato))
=>
	(printout t "                                 [provo rimozione-stati-duplicati: {" crlf)
	(printout t "                                 		id: " ?id crlf)
	(printout t "                                 		id-duplicato: " ?id-duplicato crlf)
	(printout t "                                 }]" crlf)
	(retract ?duplicato)
)

(defrule goal-trovato
	(declare (salience 200))
	?goal <- (status ?id ?depth ?id-prec ? 2 ?ultima-mossa )
	(status ?id-prec ? ?parent-id-prec ? ? ?)
=>
	(printout t "Goal raggiunto in " ?depth " mosse" crlf)
	(assert (modalita ricostruzione ?id-prec))
	(assert (transizione ?id-prec ?ultima-mossa ?id))
)

(defrule ricostruzione-passo-non-primo
	(declare (salience 200))
	?modalita <- (modalita ricostruzione ?id)
	(status ?id ? ?id-prec ? ? ?ultima-mossa)
=>
	(printout t "                                 [ricostruzione-pass-non-primo: {" crlf)
	(printout t "                                 		id-prec: " ?id-prec crlf)
	(printout t "                                 		id-succ: " ?id crlf)
	(printout t "                                 		mossa: " ?ultima-mossa crlf)
	(printout t "                                 }]" crlf)
	(assert (transizione ?id-prec ?ultima-mossa ?id))
	(retract ?modalita)
	(assert (modalita ricostruzione ?id-prec))
)

(defrule ricostruzione-primo
	(declare (salience 201))
	?modalita <- (modalita ricostruzione 0)
	?primostato <- (status 0 1 none 0 0 none)
=>
	(printout t "                                 [ricostruzione-primo: {" crlf)
	(printout t "                                 }]" crlf)
	(retract ?modalita)
	(assert (modalita stampa 0))
)

(defrule stampa-transizione
	(declare (salience 300))
	?modalita <- (modalita stampa ?id-prec)
	?transizione <- (transizione ?id-prec ?mossa ?id-succ)
	(mossa ?mossa ?testo-mossa)
=>
	(printout t ?testo-mossa crlf)
	(retract 
			?modalita
			?transizione
		)
	(assert (modalita stampa ?id-succ))
)
	 
(defrule fine-stampa
	(declare (salience 300))
	?modalita <- (modalita stampa ?id)
	(not (transizione ?id ? ?))
=>
	(printout t "Il secondo secchio contiene 2 litri" crlf)
	(retract ?modalita)
	(assert (modalita pulizia))
)

(defrule pulisci-stati-intermedi
	(declare (salience 400))
	(modalita pulizia)
	?status <- (status ? ? ? ? ? ?)
=>
	(retract ?status)
)

(defrule fine-gioco
	(declare (salience 400))
	?modalita <- (modalita pulizia)
	(not (status ? ? ? ? ? ?))
=>
	(retract ?modalita)
)

; ogni stato del problema verra espresso come:
; (stato #id #profondita #parent #riempimento-primo #riempimento-secondo #ultima-mossa)

(deffacts stato-iniziale
	(status 0 1 none 0 0 none)
	(capienza uno 4)
	(capienza due 3)
	(massimo-id 1)
	(mossa svuota-uno "Svuota il contenuto del primo secchio")
	(mossa svuota-due "Svuota il contenuto del secondo secchio")
	(mossa riempi-uno "Riempri completamente il primo secchio")
	(mossa riempi-due "Riempri completamente il secondo secchio")
	(mossa versa-tutto-due-in-uno "Versa tutto il contenuto del secondo secchio nel primo")
	(mossa versa-tutto-uno-in-due "Versa tutto il contenuto del primo secchio nel secondo")
	(mossa versa-uno-in-due-fino-a-pieno "Versa il contenuto del primo secchio nel secondo fino a riempirlo")
	(mossa versa-due-in-uno-fino-a-pieno "Versa il contenuto del secondo secchio nel primo fino a riempirlo")
)
	