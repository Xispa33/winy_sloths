=====
CI/CD
=====

| Une approche CI/CD (Continuous Integration/Continuous Delivery) a été mise en place dans le cadre du développement de WS. Cette partie vise à présenter cette approche, expliciter son intérêt et présenter les jobs mis en place.

Qu'est-ce que l'approche CI/CD ?
--------------------------------

L’approche CI/CD (Continuous Integration/Continuous Delivery) est un processus permettant d’accélérer le déploiement et la mise en production des applications en automatisant le développement des applications. Ceci est rendu possible grâce à la mise en place d'outils/programmes permettant de tester l'application et de vérifier que le programme fonctionne correctement.

| L'intégration continue (CI) est une pratique de génie logiciel permettant d'intégrer le travail effectué continuellement.
| La livraison continue (CD) n'est dans notre cas pas exploitée pour le moment. Cette pratique permet néanmoins de gérer le déploiement des logiciels pour la mise en production.

Quels sont les avantages de cette approche ?
--------------------------------------------
Dans notre cas, le processus de CI/CD est entièrement géré par un ordinateur.
| Après chaque modification de code, l'ensemble de l'application peut être testée de manière automatique, tout comme la qualité du code qui peut être mesurée. La réduction drastique de la dette technique permet aux développeurs d'analyser plus rapidement l'impact de leur modifications et ainsi de focaliser davantage leurs efforts sur la conception et le développement des fonctionnalités de l’application. L'évolutivité du code est clairement facilitée et mise en avant grâce à cette approche.
| Outres ces avantages en temps, efficacité et productivité, WS est emmené quotidiennement à gérer des quantités importantes d'argent, l'intégration de cette approche dans notre processus de développement est donc apparue comme une nécessité afin de garantir le maintien de la fiabilité de notre système.

Workflow de la chaine CI/CD
---------------------------
Le code de Winy Sloth est hébergé sur la plateforme GitHub. GitHub Action est une fonctionnalité de GitHub permettant le développement de workflows d'une chaine CI/CD. L'ensemble du workflow s'exécute sur une VM distante, désignée runner. Notre workflow actuel se décompose en deux parties, chacune permettant de jouer des tests :

* des tests dynamiques, permettant de tester le bon fonctionnement de l'application
* des tests statiques, permettant d'analyser la qualité du code

| Les tests dynamiques intégrent deux types de tests fonctionnels : les tests unitaires et les tests de validation. Sur chacune des plateformes d'échanges de cryptomonnaies, une API permet de s'interfacer avec la plateforme. Pour chaque API, les services nécessaires à notre application ont été encapsulés. Les tests unitaires testent ces services encapsulés. 
| Le framework pytest a été utilisé pour implémenter les scripts de tests et sert également pour générer le fichier de résultat au format JUnit. Les scénarios des tests unitaires ainsi que les résultats de la dernière campagne de tests unitaires sont disponibles à la page suivante :ref:`Tests`
| 
| Les tests d'intégration testent eux l'application toute entière. De même que pour les tests unitaires, unittest a été utilisé pour implémenter les tests. Le framework Multiprocessing de Python a également été utilisé. Le Multiprocessing nous permet stimuler WS (passage d'un ordre d'achat/vente) en parallèle de son exécution.
| Les scénarios des tests d'intégration ainsi que les résultats de la dernière campagne de tests d'intégration sont disponibles à la page suivante :ref:`Tests`

.. contents::
   :local:
   :backlinks: top


