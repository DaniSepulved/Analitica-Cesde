import pandas as pd
from pymongo import MongoClient
from bson import DBRef

uri = "mongodb+srv://Daniel:4334@cluster0.7qgozao.mongodb.net/notas?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["notas"]

profesores_df = pd.read_csv("profesores.csv", dtype={"id": str})
profesores = profesores_df.rename(columns={"id": "_id"})
db.profesores.insert_many(profesores.to_dict(orient="records"))

estudiantes_df = pd.read_csv("estudiantes.csv", dtype={"id": str})
estudiantes = estudiantes_df.rename(columns={"id": "_id"})
db.estudiantes.insert_many(estudiantes.to_dict(orient="records"))

asignaturas_df = pd.read_csv("asignaturas.csv", dtype={"id": str})
asignaturas = asignaturas_df.rename(columns={"id": "_id"})
db.asignaturas.insert_many(asignaturas.to_dict(orient="records"))

calificaciones_df = pd.read_csv("calificaciones.csv", dtype={"estudiante_id": str, "asignatura_id": str})
calificaciones = []
from bson import DBRef
for _, row in calificaciones_df.iterrows():
    calificaciones.append({
        "estudiante": DBRef("estudiantes", row["estudiante_id"]),
        "asignatura": DBRef("asignaturas", row["asignatura_id"]),
        "nota": float(row["nota"]),
        "fecha": row["fecha"]
    })
db.calificaciones.insert_many(calificaciones)

print("✅ Datos insertados correctamente.")


# from pymongo import MongoClient

# uri = "mongodb+srv://Daniel:4334@cluster0.7qgozao.mongodb.net/notas?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(uri)

# db = client["notas"]
# print(db.list_collection_names())

