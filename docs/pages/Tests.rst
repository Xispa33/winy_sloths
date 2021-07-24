.. _Tests:

=====
Tests
=====


Tests unitaires
===============

Scénarios de test
-----------------
Les comptes de type SPOT et FUTURES sont testés.

* SPOT 

    * Test 1 et 2:

    Les tests 1 et 2 visent à vérifier que le compte n'est pas en position d'achat en BTC ni en ETH.
    
    Le test 1 le vérifie sur le BTC et le test 2 sur l'ETH.
    
    .. table:: Scénarios tests 1 et 2
        :widths: auto

        ==================================== =======
        Commande effectuée                   Attendu
        ==================================== =======
        1 - Requête position du compte          OUT
        ==================================== =======

    * Test 3 et 4:
    Le test 3 passe un ordre d'achat en LONG, puis le ferme quelques secondes plus tard.
    Ce test permet donc de tester la fonction permettant de passer en LONG et celle permettant de fermer la position pour un compte de type SPOT.
    
    Le BTC est testé au test 3 et l'ETH au test 4.

    .. table:: Scénarios tests 3 et 4
        :widths: auto

        ==================================== ==========
        Commande effectuée                   Attendu
        ==================================== ==========
        1 - Requête ouverture LONG              SUCCESS
        2 - Requête position du compte             LONG
        3 - Requête fermeture LONG              SUCCESS
        4 - Requête position du compte              OUT
        ==================================== ==========

Résultats de test
-----------------

.. test-results:: pages/tu_spot.xml

* FUTURES

 Test 1 et 2:

    Les tests 1 et 2 visent à vérifier que le compte n'est pas en position d'achat en BTC ni en ETH.
    Le test 1 le vérifie sur le BTC et le test 2 sur l'ETH.
    
    .. table:: Scénarios tests 1 et 2
        :widths: auto

        ==================================== =======
        Commande effectuée                   Attendu
        ==================================== =======
        1 - Requête position du compte          OUT
        ==================================== =======

    * Test 3 et 4:
    Le test 3 passe un ordre d'achat en LONG, puis le ferme quelques secondes plus tard.
    Ce test permet donc de tester la fonction permettant de passer en LONG et celle permettant de fermer la position pour un compte de type FUTURES.
    
    Le BTC est testé au test 3 et l'ETH au test 4.
    
    AJOUTER LEVIER + TEST SL

    .. table:: Scénarios tests 3 et 4
        :widths: auto

        ==================================== ==========
        Commande effectuée                   Attendu
        ==================================== ==========
        1 - Requête ouverture LONG              SUCCESS
        2 - Requête position du compte             LONG
        3 - Requête fermeture LONG              SUCCESS
        4 - Requête position du compte              OUT
        ==================================== ==========

    * Test 5 et 6:
    Le test 5 passe un ordre de vente en SHORT, puis le ferme quelques secondes plus tard.
    Ce test permet donc de tester la fonction permettant de passer en SHORT et celle permettant de fermer la position pour un compte de type FUTURES.
    
    Le BTC est testé au test 5 et l'ETH au test 6.
    
    AJOUTER LEVIER + TEST SL

    .. table:: Scénarios tests 3 et 4
        :widths: auto

        ==================================== ===========
        Commande effectuée                   Attendu
        ==================================== ===========
        1 - Requête ouverture SHORT              SUCCESS
        2 - Requête position du compte             SHORT
        3 - Requête fermeture SHORT              SUCCESS
        4 - Requête position du compte               OUT
        ==================================== ===========

Résultats de test
-----------------

.. test-results:: pages/tu_futures.xml


Tests de validation
===================

Scénarios de test
-----------------

Les comptes de type SPOT et FUTURES sont testés.
Pour ces tests, le multiprocessing Python est utilisé. WS est lancé dans un
subprocess et un autre process en parallèle stimule le master. La réaction 
de WS a cette stimulation est ensuite étudiée.

* SPOT 
    * Test 1 et 2:

    Les tests 1 et 2 visent à vérifier que lorsque le compte SPOT master n'est pas excité, les comptes slaves ne changent pas de positions.
    
    Le test 1 le vérifie sur le BTC et le test 2 sur l'ETH.
    
    .. table:: Scénarios tests 1 et 2
        :widths: auto

        ======================================= =======
        Commande effectuée                      Attendu
        ======================================= =======
        1 - Requête position du compte master       OUT
        2 - Requête position des comptes slaves     OUT
        ======================================= =======

Résultats de test
-----------------

.. test-results:: pages/tu_results.xml

* FUTURES
    * Test 1 et 2:

    Les tests 1 et 2 visent à vérifier que lorsque le compte FUTURES master n'est pas excité, les comptes slaves ne changent pas de positions.
    
    Le test 1 le vérifie sur le BTC et le test 2 sur l'ETH.
    
    .. table:: Scénarios tests 1 et 2
        :widths: auto

        ======================================= =======
        Commande effectuée                      Attendu
        ======================================= =======
        1 - Requête position du compte master       OUT
        2 - Requête position des comptes slaves     OUT
        ======================================= =======

Résultats de test
-----------------

.. test-results:: pages/tu_results.xml

.. contents::
   :local:
   :backlinks: top


Pour plus d'info pour remplir ce document : 
https://readthedocs.org/projects/sphinx-test-reports/downloads/pdf/latest/
