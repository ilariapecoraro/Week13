from dataclasses import dataclass
from arts_mia.model.object import Object

@dataclass
class Connessione:
    o1 : Object # Approccio ORM
    o2 : Object
    peso : int

# approccio ORM: non abbiamo messo egli id, ma direttamente degli oggetti