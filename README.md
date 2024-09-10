<h1 align="center">
    Micro Servicio Autorización
</h1>

<center>
    Jose Daniel Sarmiento , Manuel Ayala  | { jose2192232, jose2195529 } @correo.uis.edu.co
</center>



## Resumen

The follow repository aims to management the user client and operation user to manage, and distribute the each 


## Tabla de Contenido

- [Instalación](#instalación)


## Instalación


- Configurar ar archivo `.env` con endpoint localhost y no de contenedores


1. Crear base de datos

```
    docker network create realidad_aumentada
    docker volume create db_data_user
    docker run -d --name db_user --network realidad_aumentada -p 57017:27017 --mount src=db_data_user,dst=/data/db mongo
```

2. Crear volumen estático  para la base de datos

```
    docker build -t ms_user_management:2 .
```

3. Correr el contenedor

```
    docker run --name ms_user_management -8081:81  --network realidad_aumentada  ms_user_management:2
```

## Referencias

[1] Michael Davis (2015) JSON web signature, python. Available at: https://python-jose.readthedocs.io/en/latest/jws/index.html (Accessed: 05 December 2023). 

[2] Sourabh, F. (2023) Password hashing with Bcrypt, Company. Available at: https://www.fastapitutorial.com/blog/password-hashing-fastapi/ (Accessed: 05 December 2023). 