## Programmas aktualitāte, uzdevums:

Jaunajiem auto vadītājiem tādiem kā mums ir aktuāla problēma - savas, lietotas automašīnas meklēšana. Tā kā jauni lietoti auto sludinājumi tiek ievietoti katru dienu un
iespēja, ka labākos auto nopērk relitīvi ātri ir liela, tad redzam automatizācijas iespēju. Lietota auto meklēšana var aizņemt lielu daudzumu laika, tādēļ mēs veidojam 
programmu, kura ar webscraping palīdzību, automatizē lietotu auto sludinājumu izskatīšanu. Tā kā auto var būt defekti, tad lietotājam tāpat vēlams apskatīt vēlamo sludinājumu
pašam ar konsolē atrodamo url. Programmas uzdevums ir lietotājam parādīt automašīnas, kuras sakrīt ar vēlamajiem markas, cenas, vecuma kritērijiem.

## Izmantotās bibliotēkas:

1) beautiful soup- HTML parsēšanai, web scraping pamats, ar kura palīdzību ērti piekļūt mājaslapas HTML specifiskiem datiem, tos izmantot programā vai modificēt.
2) requests- HTML caur post request atjauno filtrus un caur get request šos datus saņemam.
3) re – ļauj meklēt, pārbaudīt, modificēt un sadalīt teksta virknes pēc noteiktām pazīmēm. Tiek pielietota, lai HTML atrastu specifisku saturu.
4) os- ļauj programmai veidot saskarni ar failu sistēmu(strādāt ar tiem visdažādākajos veidos). Mums tiek pielietota jau apskatīto rakstu uzglabāšanai
5) datetime- visa veida darbības ar laiku. Mūsu gadījumā katram iegūtajam sludinājumam pievieno laiku, kurā tas iegūts.

## Programmas izmantošanas instrukcija:

1) Palaist programmu
2) Terminālī izvēlās mašīnas marku no dotā saraksta un filtrus.
3) Terminālī tiek izvadīti vēlamie, lietotāja filtram atbilstošie, automobīļi, kas skatīti pirmo reizi.
