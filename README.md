# graph_microservice
Budyfying the md graph

## Installation
1. Get vagrant
2. `vagrant up`
3. `vagrant ssh -c 'behave /opt/graph_microservice/features'
4. If any of the tests failed or take longer than 1 minute to complete then most likely celery refused to boot up (god knows why)
In that case just drop down to SSH and launch `screen -d -m celery -A service worker --loglevel=info --concurrency=10`
5. Enjoy, if your network is configured correctly you will be able to access the webservice at 127.0.0.1:9090
or VM_IP:9191


#### The task content
Description
Write an operational microservice in Python that converts a Your.MD Graph 1 into a service.
We need:
1A
Docker2 container running the s erver service which has the same class variables and the
following methods available:
. update create
a node
. connect connect
2 nodes
. get_nodes prints
all the nodes in the Graph
. connected_nodes print
the nodes and the connection between them
2A
Docker container running the client service (basic API + web server) that can interact
with the server service . This service should provide the following APIs to the external world
through http calls :
get_nodes GET
/nodes
update POST
/nodes d
‘{“uid”:1, “kind”:”hypothesis”, “name”: ”foo”}’
connect POST
/nodes/uid1 d
‘{“id”: “uid2”, “kind”: “kind2”, “relationship”: {“date”: “2015”}}’
connected_nodes GET
/nodes/uid1 (optional ?relationship=date:2015)
The above are only examples, you can do it in whichever way you feel best.
Requirements
1. Python is the preferred language for this
2. Service definition and implementation can be either Thrift, Protocol Buffers, Avro, etc.
Explain your choice.
3. Tests, basic documentation and coding guidelines according to Your.MD Coding
Standards3
4. Logging and proper exception handling
1
