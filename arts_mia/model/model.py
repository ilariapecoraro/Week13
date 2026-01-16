import copy

from arts_mia.database.DAO import DAO
import networkx as nx
from arts_mia.model.connessione import Connessione

class Model:
    def __init__(self):
        self._objects_list = []
        self._getObjects()
        # mi posso creare anche un dizionario di Object
        self._objects_dict = {} # è la idMap di Object
        for o in self._objects_list:
            self._objects_dict[o.object_id] = o
        # grafo semplice, non diretto ma pesato
        self._grafo = nx.Graph()
        self._soluzioneMigliore = []
        self._pesoMigliore = 0

    def _getObjects(self):
        self._objects_list = DAO.readObjects()

    def buildGrafo(self):
        # nodi
        self._grafo.add_nodes_from(self._objects_list)

        # archi

        # MODO 1 (80k x 80k  query SQL, dove 80k sono i nodi)
        """
        for u in self._objects_list:
            for v in self._objects_list:
                DAO.readEdges(u, v) # da scrivere
        """

        # MODO 2 (usare una query sola per estrarre le connessioni)

        connessioni = DAO.readConnessioni(self._objects_dict)
        # leggo tutte le connessioni dal DAO
        # mi porto dietro un dizionario degli oggetti
        # perchè nel database tiro fuori gli id degli oggetti, ma nella classe
        # memorizzo gli oggetti
        for c in connessioni:
            # per ogni connessione
            # creo un arco: non ho duplicati perchè check gia nella query
            # se non l'avessimo fatto avremmo dovuto controllare se la coppia ci fosse già
            # e nel caso non aggiungerla
            self._grafo.add_edge(c.o1, c.o2, peso = c.peso) # peso?


    # abbiamo fatto tre versioni
    def calcolaConnessa(self, id_nodo):
        nodo_sorgente = self._objects_dict[id_nodo]

        # Usando i successori
        successori = nx.dfs_successors(self._grafo, nodo_sorgente)
        # visita in profondità, ci restituisce l'albero orientato
        # non abbiamo quindi un elenco di nodi, ma proprio un grafo
        print(f"Successori: {len(successori)}")
        #for nodo in successori:
        #    print(nodoo)
        
        # Usando i predecessori (ma devo poi increm. di 1)
        prededessori = nx.dfs_predecessors(self._grafo, nodo_sorgente)
        print(f"Prededessori: {len(prededessori)}")

        # Ottenendo l'albero di visita
        # include anche i nodi che non sono connessi direttamente al nodo sorgente
        albero = nx.dfs_tree(self._grafo, nodo_sorgente)
        print(f"Albero: {albero}")
        return len(albero.nodes)

        # se volessi solo quelli vicini:

        # vicini = list(G.neighbors("Obj1"))
        # print(vicini)

    def getPercorsoMassimo(self, id_oggetto, lunghezza):

        v_iniziale = self._objects_dict[id_oggetto]
        self._soluzioneMigliore = []
        self._pesoMigliore = 0

        parziale = [v_iniziale]
        self.ricorsione(parziale, lunghezza)

    def ricorsione(self, parziale, lunghezza):
        if len(parziale) == lunghezza:
            # Qui ho una possibile soluzione
            # Verifico se sia "migliore" dell'attuale migliore
            # ovvero seil suo peso sia maggiore del peso
            # massimo finora trovato per le soluzioni precedenti
            if self.calcolaPeso(parziale) > self._pesoMigliore:
                self._pesoMigliore = self.calcolaPeso(parziale)
                self._soluzioneMigliore = copy.deepcopy(parziale)
            return

        # Altrimenti faccio la ricorsione
        for v in self._grafo.neighbors(parziale[-1]): # vicini dell'ultimo nodo aggiunto
            if v not in parziale and v.classification == parziale[0].classification:
                parziale.append(v)
                self.ricorsione(parziale, lunghezza)
                parziale.pop()

    def calcolaPeso(self, listaNodi):
        pesoTotale = 0
        for i in range(0,len(listaNodi)+1):
            u = listaNodi[i]
            v = listaNodi[i+1]
            pesoTotale = pesoTotale + self._grafo[u][v]["peso"]
        return pesoTotale