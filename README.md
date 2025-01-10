# IoT-Microservices-Data-Platform

Nume: Petrea Andrei \
Grupa: 342C1

## Rulare
Tema se ruleaza folsosind scriptul *run.sh* care se afla in radacina proiectului. \
Pentru ca *docker swarm* necesita imagini predefinite, am folosit *docker compose* pentru a build-ui
mai intai imaginea adaptorului si dupa rulez serviciile in swarm.

## Descriere
Proiectul contine cele 4 componente cerute in cadrul temei:
- Broker MQTT
    - Foloseste aceeasi imagine ca si in laborator, *eclipse-mosquitto*
    - Expune portul 1883

- Adapter
    - Scris in Python, folosind *paho-mqtt*
    - Primeste date de la senzori si le introduce in baza de date
    - Foloseste modulul *logging* pentru a afisa log-urile si un filtru ce verifica
    existenta variabilei de mediu *DEBUG_DATA_FLOW*

- InfluxDB
    - Datele sunt etichetate cu *location*, *station* si *key*, ultima reprezentand cheie din json-ul primit
    pentru a se putea filtra in flux dupa ele
    - Identificatorul de serie de timp este *station.key*

- Grafana
    - Expune portul 80
    - Am creat 2 dashboards:
        - *UPB IoT Data* - cu cele 2 panel-uri cerute in enunt
        - *Battery Dashborad* - cu cele 2 panel-uri cerute in enunt