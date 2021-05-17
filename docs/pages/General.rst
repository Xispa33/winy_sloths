=======
General
=======

L'objectif de cette partie consiste à présenter de manière générale 
le projet winy_sloths.


.. contents::
   :local:
   :backlinks: top

Qu'est-ce que winy_sloths ?
===========================
Winy Sloths est un algorithme de copy-trading de cryptomonnaies. 
Il permet de passer des ordres d'achat sur n'importe qu'elle cryptomonnaie 
et sur diverses plateformes connue (Binance, Kraken, Gemini, etc) en copiant
un trade passé. 

| Ce programme s'adresse autant aux traders souhaitant générer 
des profits en vendant leurs trades passés, qu'aux débutants en trading.
Le copy-trading est une branche du trading social, où les positions d'une 
personne sont copiées sur les comptes d'autres personnes. L'ouverture ou la 
fermeture d'une position peuvent aussi bien être déclenché par un trade,
que par une alerte*. Le copy-trading est une pratique très répandue et 
conseillé aux personnes débutants en trading.

Un module de gestion des bénéfices est également intégré 
à winy_sloths afin que les traders puissent s'assurer du versement de
leurs bénéfices.


A quel besoin repond-il ?
===========================
Mettre schéma

La figure 1 schématise un système ...

Une intelligence (trader, intelligence artificielle ou autre) émet un 
signal et Winy Sloths correspond à la partie permettant de suivre le signal.

Le signal est soit un ordre d'achat qu'il faudra copier, soit une alerte.
sur des comptes tiers de manière optimisée et sans échec.
Winy Sloths répond ainsi à un besoin pour un particulier de copier les trades
d'une personne de confiance et pour un trader un besoin de monétiser ses ordres
d'achats ou de vente passés.

Ainsi, un particulier a à tout moment son capital et peut le retirer s'il le 
souhaite contrairement à des fonds d'investissements ou certains livrets 
d'épargne proposés par les banques.

Comment fonctionne winy_sloths ?
================================

Fonctionnement général
----------------------
Master / Slave

Aspects techniques
------------------
L'algorithme Python est implémenté en Python, v3.7. Pour chacune des plateformes
d'échanges supportées, des APIs permettent de contrôler le compte et la copie 
de l'ordre passé se fait grâce à une paire de clés API.
Le développement de Winy Sloths se grâce à des technologies de pointe permettant
de garantir une certain niveau de qualité. 
Winy Sloth est un logiciel critique au regard des fonds gérés pouvant être
gérés. A cet effet, un environnement DevOps a été mis au point sur GitHub grâce
à GitHub Actions.
Des tests unitaires unitaires et de validations sont présents et sont rejoués à
chaque modification de code dans un environnement Dockerisé. Le module unittest a permis de rédiger les tests
unitaires et pytest permet de les jouer. Les scénarios ainsi que les derniers 
résultats de ces tests sont présents dans la partie Tests. 
Une mesure de couverture est également
calculée à la fin de ces tests grâce au module coverage. 
La qualité du code est assurée par SonarCloud.