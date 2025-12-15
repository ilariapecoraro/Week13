from dataclasses import dataclass

@dataclass
class Object:
    object_id : int
    classification : str
    continent : str
    country : str
    curator_approved : int
    dated : str
    department : str
    medium : str
    nationality : str
    object_name : str
    restricted : int
    rights_type : str
    role : str
    room : str
    style : str
    title : str

    def __str__(self):
        return f"{self.object_id} {self.title}"

    # Serve per poter usare l'oggetto come nodo del grafo
    def __hash__(self):
        return hash(self.object_id)