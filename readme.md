# Sünteetiliste diagnooside genreerimine

Antud programm on loodud Tartu Ülikooli lõputöö raames teemal **Sünteetiliste diagnooside genereerimine**.
Eesmärgiks on luua võimalikult lähedased reaalsusele andmed. Progamm on realiseeritud tõenäosusliku
automaadi abil ning kõik sündmused ja üleminekud omavad tõenäosust, mida kasutaja saab iseseisvalt muuta.

### Projekti kirjeldus

Projektis *data/input* kausta sees on olemas neli põhikausta: *chapter, subchapter, section, subsection*, mis
vastavad [RHK-10][1] kategooriatele. Iga kood on eraldiseisev objekt, millel on järgmised väljad:

***code*** - diagnoosile vastav kood

***age*** - igale vanusele (0 kuni 95) ja soole vastav diagnoosi tekkimistõenäosus

***once*** -  kas esineb üks või mitu korda elu jooksul

***chronic*** - kas haigus on krooniline

***next*** - võimalikud üleminekud antud olekust (lõppolekust) koos tõenäosusega

näiteks 
```
next: 
  A00: 0.5
  INITIAL: 0.5
```

<br/>
Samuti on olemas kaust *data/trajectories*, mis vastab trajektooride lisamise eest. Igale trajektoorile vastab kindel diagnoosi kood, millest ta algab. Trajektoori lisamiseks antud kausta sees peab looma kausta algdiagnoosi nimelise koodiga ning lisama sinna eraldiseisvaid objekte, millel on järgmised väljad:

***code*** - diagnoosile vastav kood. Juhul kui trajektooris esinevad samasugused olekud, kuid nad viidavad erinevatele diagnoosidele, siis koodi ja selle faili (laiendiga .yml) peaks nimetama code_X, kus X vastab numbrile. Iga järgnev number peab olema suurem eelmisest (näiteks I10_1, I10_2 jne).

***percent*** - protsent vahemikus 0-1, mis näitb, kui suur osa inimestest saab antud signaali (antud väli on ainult algolekul)

***transaction*** - massiiv objektidest millel on

  * probability - tulevase diagnoosi tekkimis tõenäosus
  * period - kuuline ajavahemik, mille jooksul andtud diagnoos saab tekkida

[1]: https://rhk.sm.ee/

### Kasutusjuhend

Kõikide käskude käivitamiseks peate olema ***diagnoses*** kaustas

Põhikäsud on `python main.py [-p populatsiooni arv] [-plot RHK-10 peatükki kood või sõna chapter] [-model vanus sugu(M,F)]`. Kõik käsud jooksutatakse eraldi

1. `python main.py -p 1000` genereerib 1000 isikut projekti sees olevasse ***output*** kausta

2. `python main.py -plot chapter` genereerib graafiku, mille peal on näha kõikide daignooside peatükkide jaotust. `python main.py -plot A00-B99` genereerib teatavaid nakkus- ja parasiithaigusi![Figure_1](https://user-images.githubusercontent.com/22376543/117357207-513df900-aebd-11eb-88eb-7bb40a6d38bd.png)


3. `python main.py -model 5 F` genereerib *HTML* koodi, mille peal on näha kogu tõenäosusliku automaadi, mis vastab naissoole vanuses 5

Andmebaasi andmete lisamiseks peab käivitama *database/connection.py* faili.

## Autor
	Artjom Valdas, Tartu Ülikool
