# Lion Handler - Loghandler application - Client

## Team
Authored by: [Saulo Leão - @sleao](https://github.com/sleao)

Coauthored by: [Thiago Pinho - @thiagolrpinho](https://github.com/thiagolrpinho)

# Lion Handler
Over engineering things is my passion and I will do it forever. That being said, this repo includes both a server for receiving and managing logs via websockets/API and a client that you can attach to your code that will send the logs over.

## Setting up goals

To better track this project, I'll write a bunch of things I think it should have in order to achieve my goals for this tool.

My basic idea for this is to be able to send/receive logs and the server should store it in MongoDB, but also to have some sort of control panel, to explore the logs with analytics, maybe or something like that.

The server itself should have a frontend (the control panel), with access control (a.k.a. login/logout), and the hability to create **application tokens**.

**Application tokens** will be used as a sort of access control to the log server and to minimize the amount of data in each message. An application token should be a HS256 encrypted [JWT](https://jwt.io/), with info about the app on its payload.

I'm building this to work in a container based enviroment, that hosts many applications with one or more instances of each application, so there should be a way to differentiate the instances (maybe use hostnames, since each are unique to the application pod?)

On receiving a connection, the server should validate the token (or deny the connection) and assign the application instance to its application **bucket**

A **bucket** should be a collection of logs related to an application, each log with its instance tag.

- **Client**

  - [x] Can send INFO, WARNING, ERROR, CRITICAL and DEBUG
  - [x] Can handle both String and JSON messages
  - [x] Has a fallback in case the server is unreachable

## Connection Manager

In order to better manage all the socket connections from all different applications, a Connection Manager class is defined. Besides handling both instance connection and disconnection, it should be able to return a list of active Apps/Instances, following the JSON specification below

```json
{
    "cerco": {
        "running_instances": 3,
        "instances": {
            "a2b5": {
                "socket": "hash",
                "connected_at": "6/11/2021"
            },
            "a2b6": {
                "socket": "WebSocket",
                "connected_at": "6/11/2021"
            },
            "a2b7": {
                "socket": "WebSocket",
                "connected_at": "6/11/2021"
            }
        }
    },
    "midas": {
        ...
    }
}

```
