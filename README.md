# MySQL + Flask CS3200 Semester Project - RaceReady

This repo contains a setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`.

## Project Overview
RaceReady is an event organization application designed for longer-distance running races like 5Ks, half-marathons, and full marathons. These events require much more coordination and organization than your average track meet, as there are many more different parties involved – runners, volunteers, sponsors, and the event organizer (host) themselves, just to name a few – as well as more formal processes that occur (registration, volunteer station sign-ups, police road closures, etc.). Overall, the stakes are much higher, and the smallest mistake can quickly derail these events. So, this app is meant to help all those involved always be RaceReady for each event.

## UI Implementation
RaceReady was created using AppSmith, and its current implementation includes pages for event organizers (to create races, post race results, and communicate with volunteers and police), runners (to view races, register for races, view race results, and edit their profile), and volunteers (to register for races and sign up for specific volunteer stations at particular races). The repository for this AppSmith implementation could be found [here](https://github.com/gmanalang/raceready-ui)!

## Link to our video presentation
https://www.youtube.com/watch?v=PeFxgHv6ldw




