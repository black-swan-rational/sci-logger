sci-logger
==========

####Overview
Táto utilitka slúži na archyvovanie experimetnálnych parametrov pomocou gitu. Zatiaľ je nutné, aby priečinok v ktorom ju spúšťame bol zároveň aj git repozitárom (násilná výroba repozitára pribudne časom)

Vieme ňou spustiť skript a povedať jej, aké parametre daný skript dostal, ona všeteky súbory ktoré chceme commitne do gitu (uloží) a uloží si v priešinku .snaps/ ktorý je tam, kde aj .git/, dané parametre a outcome programu. Na daných outcomoch potom vieme pomocou -e púšťať rôzne vyzualizačné skripty (tie si ale musí napísať každý sám, ale aj to čaosm bude). Vsetko co si uklada je dane id-ckom komitu a casom vykonoania akcie. 

####MAN PAGE
* -h help
* -a [file]: adne file ktory potom aduje do gitu
* -r [file]: removne file ktory potom aduje do gitu
* -p [file] [code]: zoberie code a spusti pricom ulozi jeho vystup a ulozi file ako parametre. potom zobere zoznam naadovanych suborov a commitne to.
* -s : ukaze zoznam runov
* -d : difne dva commity
* -l : list trackovanych suborov
* -e [code] [zoznam]: pusti kod (meno daneho bash scriptu) na vysledkoch zo zoznamu (cisla,mozno casom dake mena, alebo tagy)
* -E [code]: pusti [code] (meno daneho bash scriptu) na vsetkych vystupoch a prntne vysledok


####Co pribudne casom

automaticka vyzualizacia, rozumnejsie vstupne parametre, man, viac user friendly, menej vystupov, daka analytika, filtrovanie a clastrovanie vysledkov po nejakych zmenach, tagovanie, pozeranie si difov commitov
