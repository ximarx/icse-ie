;@include(moduli/halt-on-end.clp)
;@debug(watch_rule_fire=True)
;@debug(watch_fact_assert=True)
;@debug(watch_fact_retract=True)
;@debug(watch_rule_activation=True)
;@debug(watch_rule_deactivation=True)
;@debug(watch_strategy_change=True)


(set-strategy mea)

; Riempie il PRIMO(4L) secchio al massimo (se non lo e' gia')
(defrule riempi-uno "Riempie il primo secchio"
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
(defrule riempi-due "Riempie il secondo secchio"
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
	(retract ?massimo)
	(bind ?new-nextid (+ ?nextid 1))
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
(defrule svuota-uno "Svuota il primo secchio"
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
(defrule svuota-due "Svuota il secondo secchio"
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
(defrule versa-tutto-due-in-uno "Versa tutto il contenuto del primo secchio nel secondo"
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(test (> ?r-secondo 0))		
	?massimo <- (massimo-id ?nextid)
	(capienza uno ?capienza)
	(test (>= ?capienza (+ ?r-primo ?r-secondo)))
	(not (status ~?id ? ? =(+ ?r-primo ?r-secondo) 0 ?))
=>
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
(defrule versa-tutto-uno-in-due "Versa tutto il contenuto del secondo secchio nel primo"
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(test (> ?r-primo 0))
	?massimo <- (massimo-id ?nextid)
	(capienza due ?capienza)
	(test (>= ?capienza (+ ?r-primo ?r-secondo)))
	(not (status ~?id ? ? 0 =(+ ?r-primo ?r-secondo) ?))
=>
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
(defrule versa-due-in-uno-fino-a-pieno "Versa il contenuto del secondo secchio nel primo fino a riempirlo"
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(test (> ?r-secondo 0))
	?massimo <- (massimo-id ?nextid)
	(capienza uno ?capienza)
	(test (> ?capienza ?r-primo))
	(not (status ~?id ? ? ?capienza =(- ?r-secondo (- ?capienza ?r-primo) ) ?))
=>
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
(defrule versa-uno-in-due-fino-a-pieno "Versa il contenuto del primo secchio nel secondo fino a riempirlo"
	(status
			?id
			?depth 
			?parent 
			?r-primo 
			?r-secondo 
			?ultima-mossa
		)
	(test (> ?r-primo 0))
	?massimo <- (massimo-id ?nextid)
	(capienza due ?capienza)
	(test (> ?capienza ?r-secondo))
	(not (status ~?id ? ? =(- ?r-primo (- ?capienza ?r-secondo)) ?capienza ?))
=>
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


(defrule rimozione-stati-duplicati "Rimuove un eventuale stato duplicato"
	(declare (salience 100))
	(status ?id ?depth ? ?r-primo ?r-secondo ?)
	?duplicato <- (status ?id-duplicato ?depth-duplicato ? ?r-primo-duplicato ?r-secondo-duplicato ?)
	(test (< ?depth ?depth-duplicato))
	(test (= ?r-primo ?r-primo-duplicato))
	(test (= ?r-secondo ?r-secondo-duplicato))
=>
	(retract ?duplicato)
)

(defrule goal-trovato "Stampa il ritrovamento del goal e avvia la ricostruzione delle mosse"
	(declare (salience 200))
	?goal <- (status ?id ?depth ?id-prec ? 2 ?ultima-mossa )
	(status ?id-prec ? ?parent-id-prec ? ? ?)
	(massimo-id ?max)
=>
	(printout t "Goal raggiunto in " (- ?depth 1) " mosse, generando " (- ?max 1) " configurazioni" crlf)
	(assert (modalita ricostruzione ?id-prec))
	(assert (transizione ?id-prec ?ultima-mossa ?id))
)

(defrule ricostruzione-passo-non-primo "Ricostruisce la mossa da N-1 a N"
	(declare (salience 200))
	?modalita <- (modalita ricostruzione ?id)
	(status ?id ? ?id-prec ? ? ?ultima-mossa)
=>
	(assert (transizione ?id-prec ?ultima-mossa ?id))
	(retract ?modalita)
	(assert (modalita ricostruzione ?id-prec))
)

(defrule ricostruzione-primo "Ricostruisce il primo passo e passa alla modalita' di stampa"
	(declare (salience 201))
	?modalita <- (modalita ricostruzione 0)
	?primostato <- (status 0 1 none 0 0 none)
=>
	(retract ?modalita)
	(assert (modalita stampa 0))
)

(defrule stampa-transizione "Stampa la descrizione della mossa dallo stato N a N+1"
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
	 
(defrule fine-stampa "Termina la modalita' di stampa e avvia la modalita' di pulizia"
	(declare (salience 300))
	?modalita <- (modalita stampa ?id)
	(not (transizione ?id ? ?))
=>
	(printout t "Il secondo secchio contiene 2 litri" crlf)
	(retract ?modalita)
	(assert (modalita pulizia))
)

(defrule pulisci-stati-intermedi "Rimuove tutti gli stati inutili rimasti, evitando il proseguo del gioco"
	(declare (salience 400))
	(modalita pulizia)
	?status <- (status ? ? ? ? ? ?)
=>
	(retract ?status)
)

(defrule fine-gioco "Esce dalla modalita' di pulizia e mette fine al gioco"
	(declare (salience 400))
	?modalita <- (modalita pulizia)
	(not (status ? ? ? ? ? ?))
=>
	(retract ?modalita)
)

; ogni stato del problema verra' espresso come:
; (stato 
;		#id 
;		#profondita
;		#parent
;		#riempimento-primo 
;		#riempimento-secondo 
;		#ultima-mossa)

(deffacts stato-iniziale "Prepara lo stato iniziale del problema"
	(status 0 1 none 0 0 none)
	(massimo-id 1)
)

(deffacts capienze "Inserisce i valori di capienza massima dei secchi"
	(capienza uno 4)
	(capienza due 3)
)

(deffacts testi-mosse "Mappa regola -> testo azione"
	(mossa svuota-uno "Svuota il contenuto del primo secchio")
	(mossa svuota-due "Svuota il contenuto del secondo secchio")
	(mossa riempi-uno "Riempri completamente il primo secchio")
	(mossa riempi-due "Riempri completamente il secondo secchio")
	(mossa versa-tutto-due-in-uno "Versa tutto il contenuto del secondo secchio nel primo")
	(mossa versa-tutto-uno-in-due "Versa tutto il contenuto del primo secchio nel secondo")
	(mossa versa-uno-in-due-fino-a-pieno "Versa il contenuto del primo secchio nel secondo fino a riempirlo")
	(mossa versa-due-in-uno-fino-a-pieno "Versa il contenuto del secondo secchio nel primo fino a riempirlo")
)
