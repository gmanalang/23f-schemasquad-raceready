# MySQL + Flask CS3200 Semester Project - RaceReady

RaceReady is an event organization application specifically tailored toward longer-distance running races (such as 5Ks, half-marathons, and full marathons). Compared to something like your typical high school track and field meet, these events require much more coordination and organization, as there are many more different parties involved – runners, volunteers, sponsors, and the event organizer (host) themselves, just to name a few – as well as more protocols that need to be put in place (formal registration, road closures, spectating, etc.). Overall, the stakes are much higher, and the smallest mistake (e.g., not having easy access to a phone number and consequently forgetting to make a call) can quickly derail these events. So, this app will ensure that all parties know and fulfill their responsibilities, and it will provide the necessary resources to proactively and reactively tackle issues that may arise. Thus, our users will always be RaceReady for each event.

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

## Link to our video presentation
https://www.youtube.com/watch?v=PeFxgHv6ldw




