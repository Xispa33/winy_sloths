=======
General
=======

.. contents::
   :local:
   :backlinks: top
   

Cette partie présente de manière générale le projet Winy Sloths.

Qu'est-ce que Winy Sloths ?
===========================
Winy Sloths (WS) est un algorithme de copy-trading de cryptomonnaies. Il permet de passer des ordres d'achat de Bitcoin, Ethereum et BNB sur des plateformes d'échange de cryptomonnaies. A ce jour, des ordres peuvent être passés sur Binance et Bybit, deux plateformes d'échanges parmi les 5 plus importantes. L'algorithme a été rendu générique afin que d'autres plateformes d'échanges puissent être ajoutées. Mexc et Kucoin sont notamment en cours d'ajout.

A quel besoin repond-il ?
===========================

Le copy-trading est une branche du trading social, où les positions d'une personne sont copiées sur les comptes d'autres personnes. L'ouverture ou la fermeture d'une position peuvent aussi bien être déclenchée par un trade, que par une alerte. Le copy-trading est une pratique très répandue et conseillé aux personnes débutantes en trading.

| WS répond ainsi à un besoin pour un particulier de copier les trades d'une personne de confiance et pour un trader un besoin de monétiser ses ordres d'achats ou de vente passés. Tous deux ont un intérêt lucratif dans l'utilisation de ce programme.

| Contrairement à d'autres systèmes de gestion d'actifs, à tout moment, le particulier est en pleine possession de son capital et peut le retirer s'il le souhaite.

Comment fonctionne WS ?
================================
WS s'execute en parallele d'une intelligence (trader, intelligence artificielle ou autre) qui détermine les trades à effectuer. WS et cette intelligence forment le système global.

| Le système global se compose également de plusieurs comptes associés à une plateforme d'échange. Un compte appelé "maître", géré par l'intelligence et plusieurs comptes "esclaves" contrôlés par WS. En parallèle de l'execution de l'intelligence, WS se charge lui, en continue, d'observer l'historique du compte maître. 

| Lorsque l'historique du compte maitre évolue (émission d'un ordre d'achat ou de vente), tous les comptes esclaves sont mis à jour par WS de la même manière que le compte maître.

.. figure:: ws_diagram.png
   :scale: 30 %
   :alt: ws diagram

   Figure : Schéma fonctionnement WS

Aspects techniques
------------------
L'algorithme Python est implémenté en Python, v3.7. Pour chacune des plateformes d'échanges supportées, des APIs permettent de contrôler le compte et la copie de l'ordre passé se fait grâce à une paire de clés API.

| Un logiciel de copy-trading est emmené à gérer des sommes d'argents conséquentes, de différentes personnes. La qualité du code ainsi que sa fiabilité doivent ainsi être étudié de près. Pour cette raison, un environnement DevOps a été mis au point sur GitHub grâce à GitHub Actions.

| Des tests unitaires unitaires et de validations sont présents et sont rejoués à chaque modification de code dans un environnement Dockerisé. Le framework unittest est utilisé pour les tests unitaires et pytest pour les tests de validation. Les scénarios ainsi que les derniers résultats de ces tests sont présents dans l'onglet Tests. Une mesure de couverture est également calculée à la fin de ces tests grâce au module coverage. La qualité du code est suivie de près grâce à SonarCloud.

.. figure:: classes_UML.png
   :scale: 30 %
   :alt: Diagramme UML WS

   Figure : Diagramme UML


Ajout d'une plateforme d'échange dans Winy Sloths
-------------------------------------------------
Pour ajouter une plateforme d'échange :

1. Créer un dossier du nom de la plateforme d'échange en minuscule

2. Dans ce dossier, ajouter deux fichiers:
    * un fichier contenant les constantes
    * un fichier contenant qui implémente l'interface entre WS et la plateforme d'échange

3. Dans tests/tu, ajouter un fichier de tests de toutes les fonctions de l'interface

4. Dans run_test.bash: 
    * ajouter une paire de clé associée au testnet de la nouvelle plateforme d'échange.
    * ajouter cette plateforme d'échange en tant que slave des TV spot et futures 


Améliorations
------------------
| Un module de gestion des bénéfices/pertes est également envisagé en complément de WS afin que les traders puissent s'assurer du versement de leurs bénéfices. L'approvisionnement en cas de pertes permettrait également d'être effectué grâce à l'ajout d'un tel module.

| L'implémentation d'un dashboard permettant de suivre l'évolution des résultats de chacunes des stratégies et pour chaque utilisateur est envisagée. Ce dashboard serait implémenté en javascript à l'aide des Framework React, Node Js et Bootstrap. A ce jour, l'historique des trades est écrit dans un fichier au format CSV. Le dashboard permettrait d'avoir un affichage graphique des résultats.
