# BackendPokegrunn
Backend for pokegrunn

to build:
- Download and install Docker
- Inside root directory execute `docker-compose up --build`

to run:
- do `docker-compose up`

Om de admin te kunnen gebruiken en achievements to te voegen moet je eerst een superuser aanmaken. Dit doe je door de terminal van de docker container te openen en het volgende commando in te typen: `python manage.py createsuperuser`

Volg de stappen en daarna kun je met die credentials inloggen op `https://localhost:8000/admin`

-----

## Api documentation

### Endpoints:

- `/api/register-achievement` koppelt een user aan een achievement.
- `/api/user-achievements` Laat alle achievements zien van een user.
- `/api/achievements` Laat alle achievements zien.
- `/api/achievement/[ID]` Laat achievement zien op basis van id.
- `/api/achievement-code/[CODE]` laat achievement zien op basis van code.
- `/api/user/[USERNAME]` laat user zien op basis van username
- `/api/users/` laat alle users zien

-----

### Voorbeelden
`/api/register-achievement`
Zorg ervoor dat je een body meegeeft met deze format. Koppeld een user "ditiseenusername" aan de achievement met de code "xxxx":
```json
{
    "username": "ditiseenusername",
    "achievement_code": "xxxx"
}
```

-----

`/api/user-achievements`

Zorg ervoor dat je deze format gebruikt:
`/api/user-achievements?username=ditiseenusername`

-----

`/api/achievements`

Om alle achievements te laten zien die een bepaalde user niet heeft:
`/api/achievements?username=ditiseenusername`

Om alle achievents te laten zien gerankschikt op basis van afstand van de user's apparaat:
`/api/achievements?longitude=34.23131&latitude=52.23123`

Om alle achievents te laten zien met een maximum aantal records:
`/api/achievements?max=5`

Note: Alle query parameters kunnen gecombineerd worden. Bijvoorbeeld username met een max aantal record of username en longitude+latitude.

-----

De twee andere endpoints zijn vanzelf sprekend.