.. _Tests:

=====
Tests
=====

Tests unitaires
===============

Les comptes de type SPOT et FUTURES sont testés. Ces tests visent à tester unitairement l'ensemble des fonctions permettant de communiquer avec les plateformes d'échanges. Plus précisement, Binance et Bybit sont testés.

| Chacune de ces deux plateformes disposent d'un testnet, permettant ainsi de simuler des échanges avec des actifs virtuels. Tous les tests sont effectués en échangeant du bitcoin (BTC).

Tests de validation
===================

Les comptes de type SPOT et FUTURES sont également testés ici. WS est lancé dans un subprocess, le master est stimulé avant le démarrage du subprocess le master. La réaction de WS a cette stimulation est ensuite étudiée.

| Pour ces tests, le master est toujours répertorié sur Binance et gère 2 slaves : 1 sur Binance, l'autre sur Bybit.

| De même que pour les TU, les tests sont effectués sur le testnet avec du bitcoin.

Scénarios de test
===================

.. tabs::
    
    .. tab:: Tests unitaires

        .. tabs::

            .. tab:: BINANCE

                .. tabs::

                    .. tab:: SPOT

                    .. tab:: FUTURES
        
            .. tab:: BYBIT
                
                .. tabs::

                    .. tab:: SPOT

                    .. tab:: FUTURES

    .. tab:: Tests de validation

        .. tabs::

            .. tab:: SPOT

            .. tab:: FUTURES


* TESTS SPOT 
    
    * Informations sur les tests

    .. table:: Informations tests des plateformes d'échanges SPOT
        :widths: auto

        ==================================== ================
        Plateforme d'échange                 Nb tests attendus
        ==================================== ================
        1 - Binance                          9
        2 - Bybit                            8
        ==================================== ================

* TESTS FUTURES
    
    * Informations sur les tests

    .. table:: Informations tests des plateformes d'échanges FUTURES
        :widths: auto

        ==================================== ================
        Plateforme d'échange                 Nb tests attendus
        ==================================== ================
        1 - Binance                          11
        2 - Bybit                            8
        ==================================== ================

Résultats de test unitaires
===========================

BINANCE
-------

* Spot

.. test-results:: pages/tu_spot_binance_BTCUSDT.xml

* Futures

.. test-results:: pages/tu_futures_binance_BTCUSDT.xml

BYBIT
-----

* Spot

.. test-results:: pages/tu_spot_bybit_BTCUSDT.xml

* Futures

.. test-results:: pages/tu_futures_bybit_BTCUSDT.xml


* Résultats de test de validation
---------------------------------

* SPOT

.. test-results:: pages/tv_spot_binance_BTCUSDT.xml

* FUTURES

.. test-results:: pages/tv_futures_binance_BTCUSDT.xml 


Qualité de code et couverture
=============================

Les résultats de tests sont également disponibles dans SonarQube. Une analyse complète de la couverture de code ainsi que de la qualité de code y figurent également. 

| Le logiciel est contenu dans un Docker, son utilisation permet de profiter pleinement de SonarQube gratuitement. L'intégration du Docker SonarQube dans le pipeline Github Action n'a pas été effectué, il faut donc lancer SonarQube manuellement.

Pour plus d'info pour remplir ce document : 
https://readthedocs.org/projects/sphinx-test-reports/downloads/pdf/latest/
