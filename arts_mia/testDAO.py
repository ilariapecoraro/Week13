from arts_mia.database.DAO import DAO

results = DAO.readObjects()
print(len(results))
print(results[5])