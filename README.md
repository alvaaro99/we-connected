# We-connected

This project is a proof of concept of the theory of the 6 degrees of separation between people. This backend returns the information necessary to be able to paint.
a graph and represent it visually.

Este proyecto es una prueba de concepto de la teoría de los 6 grados de separación entre personas. Este backend devuelve la información necesaria para poder pintar
un grafo y representarlo visualmente.

## Tabla de Contenidos

-   [Descripción](#descripción)
-   [Instalación](#instalación)

## Descripción

Esta pensado para que un usuario se registre con una información mínima y se cree un nodo con la información necesaria para quedar registrado en el grafo.
Recomendablemente a la hora del registro se debe indicar una conexión con una persona en el grafo para que no se queden nodos sueltos.

It is designed so that a user registers with minimal information and a node is created with the necessary information to be registered in the graph.
It is recommended that at the time of registration a connection with a person in the graph should be indicated so that no nodes are left loose.

## Instalación

Ejecutar el archivo de docker-compose para que se instale y se cree el contenedor en docker de neo4j. Luego iniciar como una aplicación de flask.

Run the docker-compose file to install and create the neo4j docker container. Then start as a flask application.

### Prerrequisitos

Lista de prerrequisitos necesarios para ejecutar el proyecto, por ejemplo:

-   Docker
-   Docker-compose
-   Python
