# Week 1 — App Containerization

## Containerize the front-end and backend application

<!-- trunk-ignore(git-diff-check/error) -->
I have created a dockerfile for the front-end react code and dockerfile for the backend database. 

Have a look at the dockerfile for front-end application:
Have a look at the dockerfile for back-end application:


## Setting up docker-compose file

<!-- trunk-ignore(git-diff-check/error) -->
After creating the individual docker files. I have created a docker compose file for launching the front-end and back-end application simultaneously. The docker-compose file is used for connecting the front-end and backend docker containers and also providing the links for accessing the applications seperately. 

You can find the code for docker-compose file:
> version: "3.8"
    services:
      backend-flask:
        environment:
          FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
          BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
        build: ./backend-flask
        ports:
          - "4567:4567"
        volumes:
          - ./backend-flask:/backend-flask
      frontend-react-js:
        environment:
          REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
        build: ./frontend-react-js
        ports:
          - "3000:3000"
        volumes:
          - ./frontend-react-js:/frontend-react-js
      dynamodb-local:
        # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
        # We needed to add user:root to get this working.
        user: root
        command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
        image: "amazon/dynamodb-local:latest"
        container_name: dynamodb-local
        ports:
          - "8000:8000"
        volumes:
          - "./docker/dynamodb:/home/dynamodblocal/data"
        working_dir: /home/dynamodblocal
      db:
        image: postgres:13-alpine
        restart: always
        environment:
          - POSTGRES_USER=postgres
          - POSTGRES_PASSWORD=password
        ports:
          - '5432:5432'
        volumes: 
          - db:/var/lib/postgresql/data
    # the name flag is a hack to change the default prepend folder
    # name when outputting the image names
    networks: 
      internal-network:
        driver: bridge
        name: cruddur

    volumes:
      db:
        driver: local
