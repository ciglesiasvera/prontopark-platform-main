
# Pronto Park platform

## Descripción

Repositorio de desarrollo para una plataforma web que permite a residentes de un condominio el poder reservar estacionamientos.

## Repo del proyecto

[Link del proyecto en GitHub](https://github.com/armincano/prontopark-platform.git)

## 🖼️ Tech Stacks

- Django framework.
- psycopg2 library. Para usar PostgreSQL RDBMS.
- python-dotenv. Para usar variables de entorno.
- djLint library. Para obtener información de errores de sintaxis y formatear Django templates.

> [!IMPORTANT]  
> Instala la extensión `djLint` por monosans desde el marketplace de vscode. Debería aparecer como extensión recomendada.

## Flujo de GIT

Utilizamos GitHub flow. Más información en [GitHub docs](https://docs.github.com/es/get-started/using-github/github-flow).

### 1. Cambios locales

1. Localmente, ubicado en rama `main`, ejecuta `git pull` para traer los últimos commits desde remoto.
2. Crear rama `x` desde `main` ejecutando `git checkout -b feature`
3. Ubicado en rama `x`, realiza los cambios y commits necesarios para desarrollar la funcionalidad.

### 2. Preparando mi rama para remoto

Cuando se quiera hacer merge de una rama `x` desarrollada localmente hacia la rama `main` remota del proyecto en GitHub:

1. Localmente, ubicado en la rama `x`, ejecuta `git pull origin main` para traer los últimos cambios a `main`
2. Localmente hacer merge de rama `main` en rama `x` ejecutando `git merge main`. Esto para resolver conflictos localmente.
3. Resolver localmente posibles conflictos (pedir ayuda al equipo si es necesario).
4. Hacer las pruebas que corresponda para validar que nuestros cambios no generaron bugs en rama `main`.
5. Ejecuta `git push` de la rama `x`.

### 3. Crear el pull request

1. Desde tu explorador abre el repo en GitHub -> selecciona la pestaña **Pull requests** -> presiona el botón **New pull request** -> en la página **Compare changes** selecciona como **base ref** a `main` y selecciona como **head ref** a tu rama `x`
2. Presiona **Create pull request**.

> [!TIP]
> Al crear el pull request se puede escribir un comentario, hacerlo si el contexto lo amerita.
> Si se estima conveniente, antes de hacer el merge del siguiente paso, puede solicitar a otros miembros del equipo que lo revisen (ver Reviewers, arriba, a la derecha, en la página del pull request creado).

3. Realizar el merge del pull request en GitHub. Como no deberían haber conflictos, uno mismo puede realizar inmediatamente el merge del pull request presionando `Merge pull request`. Está al final de la página del pull request creado.
4. Borrar la rama `x` en Github.

## Convención de nombres para ramas

Al crear una rama, debes añadir un prefijo dependiendo del tipo del tipo de desarrollo que efectúes.

- Nueva característica: `feature/`
  - `feature/short-description`
  - `feature/login-page`

- Bugfix: `bugfix/`
  - `bugfix/issue-123`
  - `bugfix/null-pointer-exception`

- Hotfix (fix urgente en producción): `hotfix/`
  - hotfix/critical-bug-455

- Mejoramiento: `improvement/`
  - `improvement/refactor-auth`
  - `improvement/update-dependencies`

- Release (preparar nuevo reléase): `release/`
  - `release/v1.2.0`
  - `release/2.0.0`

- Experimentos:  `experiment/`
  - `experiment/new-layout`
  - `experiment/feature-toggle`

## Instalación

> [!NOTE]  
> Comandos funcionales para sistema MacOS

1. Clona el repo del proyecto.
2. Desde tu CLI, navega al directorio raíz del proyecto clonado.
3. Crea un ambiente virtual con el nombre `venv`
4. Activa tu ambiente virtual `source venv/bin/activate`
5. Instala los requerimientos con `pip3 install -r requirements.txt`
6. Crea una DB (Data Base) local. Te recomendamos el nombre `ppark_platform`

> [!IMPORTANT]  
> Para crear una DB local, debes tener instalado en tu equipo PostgreSQL RDBMS. Ya instalada, puedes instalar el software pgAdmin como cliente para crear tu DB; o usa tu CLI ejecutando el comando `psql`, y finalmente `CREATE DATABASE ppark_platform;`.

7. Crea un archivo `.env` en la carpeta raíz del proyecto con las siguientes variables (los valores para las primeras 6 variables dependen de la creación de la DB del paso anterior, excepto para `DJANGO_SECRET_KEY` la cual es requerida para trabajar con datos ficticios que contienen contraseñas hasheadas con el valor de esta variable):

```env
DB_NAME=ppark_platform
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
DJANGO_ALLOWED_HOSTS=*
DJANGO_SECRET_KEY="django-insecure-c8#47!ht*il3&^@ql)$9j642c8&tcty#h71yu0_zr^ddz4g_y)"
```

> [!WARNING]  
> Recuerda crear una nueva `SECRET_KEY` para producción.

> [!IMPORTANT]  
> En producción, `DJANGO_ALLOWED_HOSTS` solamente debe contener la dirección desde donde será accesible el sitio, por ej.: wwww.prontopark.cl.

8. Ejecuta `python3 manage.py migrate` para que tu DB local cree las tablas correspondientes al proyecto.
9. Llena tu DB local con datos ficticios, ejecutando `python3 manage.py loaddata fixtures/fixtures.json`

> [!IMPORTANT]  
> Cada usuario creado con el archivo `fixture` utiliza la misma contraseña que es `contra123`

10. Crea tu superusuario con `python3 manage.py createsuperuser`
11. Inicia el servidor de desarrollo con `python3 manage.py runserver`
12. Ingresa al Django Admin Site `http://localhost:8000/admin`. Luego ingresa al dashboard de la app `USERS`, selecciona el correo del super usuario que creaste y cambia su `Role` a `Supervisor` con la lista desplegable.

> [!TIP]
> Si tienes errores en la DB local, posiblemente debas eliminarla, crear una nueva DB y luego ejecutar `python3 manage.py migrate`

## Conectarse a servidor local Django desde dispositivos móviles

1. Obtener la ip local de su máquina, en donde corre el servidor.
2. En el archivo `.env` que creaste previamente, la variable `DJANGO_ALLOWED_HOSTS` contiene la lista de nombres de dominio que Django puede servir. Por defecto, utilizamos el comodín `*` que permite a Django aceptar solicitudes de cualquier host.

> [!WARNING]  
> El comodín `*` es una brecha de seguridad. En producción, en `ALLOWED_HOSTS` solo debe ir la dirección pública final.

3. El servidor se inicia con: `python3 manage.py runserver 0.0.0.0:8000` Ahora cualquier dispositivo conectado a la red local se puede conectar a la ip sirviendo la aplicación.

> [!IMPORTANT]  
> Si usan firewall, crear una regla en el firewall para abrir el puerto TCP 8000 en conexiones privadas.