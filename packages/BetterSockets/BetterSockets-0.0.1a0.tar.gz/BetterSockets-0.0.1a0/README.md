## BetterSockets
#### The alternative for Python sockets and asyncio streams is here
##
### Usage:

To use this library just import BetterSockets, and you are good to go.
Start by choosing your class in form of a _client_ or a _server_, by writing
`client = BetterSockets.Client()` or `server = BetterSockets.HubServer() / ProcessorServer()`. You can customize the client in some ways, 
as well as the server. For that we make the use of keyword arguments. You can choose 
whether you want to utilise the normal python sockets or an asynchronous stream by 
putting in a `is_async=` - followed by a boolean inside the apprentices of the class. 
In the same way you can modify the port, ip and a debug - menu. For the ProcessorServer 
you can add a function to process incoming messages by placing a `func=function` inside 
the corresponding apprentices. Same goes for the client, but it is different for the HubServer, 
you can put a `identifier=Function` inside it. It is used to determine whether the client 
gains access to the server.
To start listening on a server-class, you need to call the `listen()` function of that class. 
For the client to send data, you need to call the `send()` function, just put the data you want
 to send inside the apprentices.

#
## Changelog
####
**0.0.1a (14.07.2021)**
- Release of this package
