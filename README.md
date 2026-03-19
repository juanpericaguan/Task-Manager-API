🧠 Task Manager API — FastAPI

API RESTful para gestión de tareas con autenticación JWT, construida con FastAPI siguiendo una arquitectura en capas profesional.



🚀 Descripción

Este proyecto implementa un sistema de gestión de tareas donde los usuarios pueden:

Registrarse y autenticarse

Crear, leer, actualizar y eliminar tareas

Filtrar tareas por estado y prioridad

Gestionar sus propias tareas (control de ownership)

Administrar usuarios (rol admin)

Incluye autenticación segura con JWT y control de acceso basado en roles.



🛠️ Tecnologías utilizadas

FastAPI — Framework web moderno y rápido

SQLite — Base de datos ligera

Pydantic — Validación de datos

JWT (python-jose) — Autenticación basada en tokens

bcrypt — Hash seguro de contraseñas

dotenv — Manejo de variables de entorno




🧱 Arquitectura del proyecto

El proyecto sigue una arquitectura en capas:

app/
│
├── core/           # Configuración y seguridad (JWT, hashing)
├── db/             # Acceso a base de datos (queries SQL)
├── dependencies/   # Inyección de dependencias (auth, db, validaciones)
├── task/           # Lógica de tareas (router, schemas, services)
├── users/          # Lógica de usuarios (router, schemas)
└── main.py         # Punto de entrada
Separación de responsabilidades:

Routers → Endpoints (HTTP)

Services → Lógica de negocio

DB → Acceso a datos

Dependencies → Autenticación y validaciones



🔐 Autenticación

El sistema utiliza JWT (JSON Web Tokens):

Login con /users/login

Retorna access_token

Se debe enviar en headers:

Authorization: Bearer <token>




⚙️ Instalación y ejecución
1. Clonar el repositorio
git clone <https://github.com/juanpericaguan/Task-Manager-API>
cd Task-Manager

2. Crear entorno virtual
python -m venv venv

3. Activar entorno

Windows:

venv\\Scripts\\activate

Linux / Mac:

source venv/bin/activate

4. Instalar dependencias
pip install -r requirements.txt

5. Configurar variables de entorno
Crear archivo .env basado en .env.example

6. Crear base de datos
python app/db/create_db.py

7. Ejecutar servidor
uvicorn app.main:app --reload





📌 Endpoints principales

👤 Usuarios
Método	Endpoint	Descripción
POST	/users/	Crear usuario
GET	/users/	Listar usuarios (admin)
PUT	/users/{id}	Actualizar usuario
PATCH	/users/{id}	Actualización parcial
DELETE	/users/{id}	Eliminar usuario
POST	/users/login	Login

📋 Tareas
Método	Endpoint	Descripción
POST	/tasks/	Crear tarea
GET	/tasks/	Listar tareas
PUT	/tasks/{id}	Reemplazar tarea
PATCH	/tasks/{id}	Actualizar parcialmente
DELETE	/tasks/{id}	Eliminar tarea


🔎 Filtros disponibles

En /tasks/:

status: pending | in_progress | completed

priority: low | standard | high

limit: cantidad de resultados

offset: paginación




🛡️ Seguridad

Contraseñas hasheadas con bcrypt

Tokens JWT con expiración

Migración automática de SHA256 → bcrypt

Control de acceso:

Usuario solo accede a sus tareas

Admin puede ver todos los usuarios



🧪 Testing interactivo

FastAPI incluye documentación automática:

👉 Swagger UI:

http://localhost:8000/docs

👉 Redoc:

http://localhost:8000/redoc



📈 Posibles mejoras futuras

🔧 Sistema de migraciones (Alembic)

🧠 Capa de mapeo (DTOs / mappers)

🛡️ Manejo global de errores

🧪 Tests automatizados (pytest)

🐳 Dockerización

☁️ Deploy (Render / Railway)



👨‍💻 Autor Juan Pericaguan Correo: juanmiguel018@gmail.com

Proyecto desarrollado como práctica avanzada de backend con enfoque profesional en arquitectura, seguridad y buenas prácticas.

⭐ Nota final

Este proyecto está diseñado para simular un entorno real de desarrollo backend, aplicando conceptos utilizados en empresas como:

Arquitectura en capas

Autenticación segura

Buenas prácticas con FastAPI