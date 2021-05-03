# Sünteetiliste diagnooside genreerimine

Antud programm on loodud Tartu Ülikooli lõputöö raames teemal **Sünteetiliste diagnooside genereerimine**.
Eesmärgiks on luua võimalikult lähedased reaalsusele andmed. Progamm on realiseeritud tõenäosusliku
automaadi abil ning kõik sündmused ja üleminekud omavad tõenäosust, mida kasutaja saab iseseisvalt muuta.

Projektis *data/input* kausta sees on olemas neli põhikausta: *chapter, subchapter, section, subsection*, mis
vastavad [RHK-10][1] kategooriatele. Iga kood on eraldiseisev objekt, millel on järgmised väljad:

*code* - diagnoosile vastav kood

*age* - igale vanusele (0 kuni 95) ja soole vastav diagnoosi tekkimistõenäosus

*once* -  kas esineb üks või mitu korda elu jooksul

*chronic* - kas haigus on krooniline

*next* - võimalikud üleminekud antud olekust (lõppolekust) koos tõenäosusega

Samuti on olemas kaust *data/trajectories*, mis vastab trajektooride lisamise eest. Igale trajektoorile vastab kindel diagnoosi kood, millest ta algab. Trajektoori lisamiseks antud kausta sees peab looma kausta algdiaagnoosi nimelise koodiga ning lisama sinna eraldiseisvaid objekte, millel on järgmised väljad:

*code* - diagnoosile vastav kood

*transaction* - massiiv objektidest millel on
    
    *probability* - tulevase diagnoosi tekkimis tõenäosus
    
    *period* - kuuline ajavahemik, mille jooksul andtud diagnoos saab tekkida

[1]: https://rhk.sm.ee/

### Kasutusjuhend

Kõikide käskude käivitamiseks peate olema ***diagnoses*** kaustas

Põhikäsud on `python main.py [-p populatsiooni arv] [-plot RHK-10 peatükki kood või sõna chapter] [-model vanus sugu(M,F)]`. Kõik käsud jooksutatakse eraldi

1. `python main.py -p 1000` genereerib 1000 isikut projekti sees olevasse ***output*** kausta

2. `python main.py -plot chapter` genereerib graafiku, mille peal on näha kõikide daignooside peatükkide jaotust

3. `python main.py -model 5 F` genereerib *HTML* koodi, mille peal on näha kogu tõenäosusliku automaadi, mis vastab naissoole vanuses 5

## Autor
	Artjom Valdas, Tartu Ülikool
