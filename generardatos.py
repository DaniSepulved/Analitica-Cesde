import csv
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('es_ES')

# Cantidades
NUM_PROFESORES = 200
NUM_ESTUDIANTES = 1000
NUM_ASIGNATURAS = 500
NUM_CALIFICACIONES = 2000

# Almacenar IDs
profesores = []
estudiantes = []
asignaturas = []

# ========================
# Generar profesores.csv
with open("profesores.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "nombre", "email", "password", "rol"])
    for _ in range(NUM_PROFESORES):
        pid = str(uuid.uuid4())
        nombre = fake.name()
        email = fake.unique.email()
        password = "1234"
        rol = "PROFESOR"
        profesores.append(pid)
        writer.writerow([pid, nombre, email, password, rol])

# ========================
# Generar estudiantes.csv
with open("estudiantes.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "nombre", "email", "password", "rol"])
    for _ in range(NUM_ESTUDIANTES):
        eid = str(uuid.uuid4())
        nombre = fake.name()
        email = fake.unique.email()
        password = "1234"
        rol = "ESTUDIANTE"
        estudiantes.append(eid)
        writer.writerow([eid, nombre, email, password, rol])

# ========================
# Generar asignaturas.csv
asignatura_nombres = [
    "Matemáticas", "Física", "Química", "Biología", "Historia", "Geografía", "Lengua Castellana",
    "Inglés", "Educación Física", "Filosofía", "Arte", "Música", "Tecnología", "Informática", 
    "Ética", "Religión", "Economía", "Literatura", "Ciencias Sociales", "Emprendimiento"
]

with open("asignaturas.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "nombre", "profesor_id"])
    for _ in range(NUM_ASIGNATURAS):
        aid = str(uuid.uuid4())
        nombre = random.choice(asignatura_nombres) + f" {random.randint(1, 4)}"
        profesor_id = random.choice(profesores)
        asignaturas.append(aid)
        writer.writerow([aid, nombre, profesor_id])

# ========================
# Generar calificaciones.csv
with open("calificaciones.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["estudiante_id", "asignatura_id", "nota", "fecha"])
    for _ in range(NUM_CALIFICACIONES):
        estudiante_id = random.choice(estudiantes)
        asignatura_id = random.choice(asignaturas)
        nota = round(random.uniform(1.0, 5.0), 1)
        fecha = (datetime.today() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        writer.writerow([estudiante_id, asignatura_id, nota, fecha])
