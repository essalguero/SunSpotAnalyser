# SunSpotAnalyser
Analyse areas of the Sun for thermal activity


## Development
The whole development of the app has been carried out using PyCharm in an Ubuntu Linux 20.4.1.
It has been design to be run inside 2 different Docker Containers. One to execute the database and the other one to 
execute the REST API


## Unit Testing
Unit tests have been created for each of the classes included in the project. Unfortunately, I only have been able to 
run the unit test from inside PyCharm. When trying to execute them from outside the IDE, an exception is always raised, 
but I did not have enough time to investigate the issue


## Execution
Two different bash files are provided in the project containing the needed commands to create the Docker containers 
needed for the project. One of the files is meant to execute the application itself (docker_build.sh), while the other 
one (docker_build_tests.sh) is meant to be used for executing the unit tests


## GitHub Repository
The project is stored in the following public GitHub url:

https://github.com/essalguero/SunSpotAnalyser

for executing the project, the following steps should be followed

1.- Clone the project

git clone https://github.com/essalguero/SunSpotAnalyser ./SunSpotAnalyser

2.- Go to the directory of the project

cd SunSpotAnalyser

3.- Create the Docker containers
(It is needed that Docker is installed in the machine where the project is going to be executed)
./docker_build.sh

In this point the REST API should be available at http://localhost:5000


## Available Operations

"/sun-spot-analyser-api/delete", methods=['DELETE']

"/sun-spot-analyser-api/scores_sorted", methods=['GET']

"/sun-spot-analyser-api/scores", methods=['GET']

"/sun-spot-analyser-api/grid", methods=['POST']
