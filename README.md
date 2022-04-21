# Chat Application

This is the Chat Web application allowing you to register new WebSocket
servers that can be used to handle load (maintain WS connections).
Load is balanced based on number of connections.

### To start Chat App
* Do build on your first time running the application `docker-compose build` (in the root directory)
* Starting the application - `docker-compose up` or `docker-compose up -d` (in the root directory)
* Stopping the application - `docker-compose down` (in the root directory)
* When the app is run you can go to `http://localhost:8080/`
* Register new WebSocket server - `http://localhost:8080/register` (max 3)
