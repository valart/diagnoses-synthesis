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

1. `python main.py -p 1000` genereerib 1000 isikut projekti sees olevasse ***output*** kausta faili *diagnoses.csv*. Iga diagnoosi on kujul ***(diagnoosi_kood, tekkimise_kuupäev)***, kuid leidub ka kujul ***(diagnoosi_kood, tekkimise_kuupäev, TRJ)***, mis näitab, et antud diagnoos oli lisatud trajektoori generaatori abil

2. `python main.py -plot chapter` genereerib graafiku, mille peal on näha kõikide daignooside peatükkide jaotust. `python main.py -plot A00-B99` genereerib teatavaid nakkus- ja parasiithaigusi![Figure_1](https://user-images.githubusercontent.com/22376543/117357207-513df900-aebd-11eb-88eb-7bb40a6d38bd.png)


3. `python main.py -model 5 F` genereerib *HTML* koodi, mille peal on näha kogu tõenäosusliku automaadi, mis vastab naissoole vanuses 5

### Andmebaas

Andmebaasi andmete lisamiseks peab käivitama *database/connection.py* faili. Selleks, et scirpt käivituks kaustas *data/ICD10* peavad olema failid *icd10_to_omop.tsv* ja *concept.tsv*. Nende saamiseks võtke ühendust autoriga.

### Trajektooride lisamine

1. Kaustas *trajectories* looge kaust RHK10 koodi nimega, millest algab trajektoor (näiteks *A00*)
2. Selles kaustas looge fail *.yml* nimega, millest trajektoor algab (näiteks *A00.yml*)
3. Esimese faili sisu näeb välja järgmiselt (näide)
```
code: A00
percent: 0.8
transaction:
  B00:
    probability: 1
    period: 12
```
kus *code* antud oleku RHK10 kood, *percent* kui suurel osal protsentuaalselt antud trajektoor hakkab esinema, *transaction* võimalikud üleminekud, mis omavad võimaliku oleku RHK10 koodi, tõenäosust (kõikide olekute summa peab olema 1) ning ajavahemikku, mille jooksul antud haigus saab tekkida

4. Selleks et luua olek, millese tahame edasi liikuda peab looma faili antud RHK10 koodiga (näiteks B00), mille sisu saab olla järgmine
```
code: B00
transaction:
  C00:
    probability: 0.7
    period: 12
  D00:
    probability: 0.2
    period: 12
  E00:
    probability: 0.1
    period: 12
```

## Autor
	Artjom Valdas, Tartu Ülikool
