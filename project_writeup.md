# Project writeup, also known as *task 1*

## Foreword
So, finally "done". I must say that it is extremely ftrustrating to work alone, on trying to servisize someeones piece of code that doesn't come with any explanation of what is it doing,
or even wroking example of how to use it (the one in repo requires a bit of manual adjustment in order to run it). But I guess I prevailed?

Initially I wanted to just knock the service task quickly with thrift + bottle, but as I started going at it this seemed more and more nonsensical (more on that later down the road)
so in the end I've decided to mash the both together, and implement a microservice + describe how it was designed, and why. And this is the result of it. This is quite
outisde of both tasks MO, i know that, so if that doesn't satisfy you - that is on me and I will convert this work into a form of couple blog entries. It's way overdue
for an update anyway!

Also given how much hassle the graph took me (and sadly I had to discover it as I go), I didn't have time to dokerize the stack. But I wouldn't call it as a loss, as
docker is not suitable for at-scale deployments, and dev environment can be easily shared with existing vagrant file, all you have to do is `up` it. And unlike docker
it will work on any operating system that supports hardware visualization. Also since we leverage the power of celery, this takes care of mundane task of logging for us.

Now, lets gets on with the writeup.

## Design choices and overall plan

### Givens

 - graph is considered a black box, encrypted DLL, which we can only access via it's own API. No messing around with member variables etc. Also no
 code fixing and tweaking, so all I've done to it is to port it up to python3 + fix couple pip violations that attacked me when I tried to read the code.
 - MVC is the way to go. Period.
 - this is intended to be easily scalable up and side ways and handle loads of up to 20k requests/second (given enough boxes)
 - while the primary language is Python and majority of the codebase will be in it, it should allow for straightforward integration with extrenal languages
 - architecture designed toward fixed physical boxes, sometimes supported by autoscaled cloud.
 
### Design choices

#### Global overview of architecture

Application consists of 3 main components:

 - view. This consists of all consumer-facing parts in various forms (REST api, web interface, socket server etc).
 Views in general must easily scale vertically, as scaling them side-ways brings an expense in form of a load-balancer which has to tie all the horizontal boxes
 together into a single entry point. Given that a choice will be with a technology that does well with high-concurrency, preferably leveraging the power of forking
 and non-blocking threads. Mix of both is preferred, but you can do fine with just forks. Just threading won't cut it as it is highly inefficient in utilizing moden CPUs.
 - model. Pieces of software that manipulate the data, whether it is coming from some data source or user inputs. This will typically consists of scrapers, processors, 
 aggregation etc. This is the heart of the application that does most of the heavy lifting, and it must scale evenly up and sideways. Which way more depends on type of processing
 it will do. If it relies primarily on blocking CPU then it's best spread horizontallly, and if it is much more relient on some IO blocking then it's much better to go with
 vertical scaling to better utilize CPUs with a lot of idle threads awaiting their turn.
 - controller. The heart of application, that collects the requestst from teh views, routes them to approperiate piece of software in the model, and then passes a response
 back to the view (or passes a way for model to return data directly to view, depends). This is a piece that is always best scaled vertically, as there is almost no idling
 and it is almost always entirely CPU-bound process, with very little IO taking place in general. Good example of this is all sorts of messaging systems like RabbitMQ, 
 Kafka and so on.
 
#### Implementation choices.
 
##### View
 
Given the above, the view will be best served with an extremely lightweight python webserver that relies on forking to handle high loads. That leaves us with either
twisted, which is quite complex to properly set up and maintain, but at the same time is a speed deamon. Or something based on cherrpyp - either Flask or Bottle. 
I certainly would not consider here one of the humongous frameworks like django with rest-django middleware, because while it does allow for rapid development, it certainly
does not hold a candle in terms of performance. It also works best when it fill entire MVC itself, which while good for small apps, is rather challenging to later on
parcel, distribute and scale.
Difference between flask and bottle is purely cosmetics, those two frameworks are almost identical performance and feature wise, so we will stick to a bottle here due to
my personal preference and larger amount of experience with it over flask.

##### Model

Not much to describe here, we've settled on python for this project so that will be core of our processor. We have a problem that graph does not allow for any sort of
persistant data as it is now, so we have to wrap it around in order to mainain the data between user calls and application resets. Given that we only have access to results of
data, not to components itself, it's best to just settle with a generic container that allows to, rather easily, store whole python object and later fetch it as needed.
When it comes to as simple usage as that, there is no better choice than redis and we will go with it. If we wanted to do partial updates on the graph, not just fetch and
store whole object (which is what is going on now and is, well, bad design as it generates a lot of race conditions and work will overwrite one another) then the best course
of action would be to store partials of inside of the graph itself, and write those changes on each update ran. Doing that from outside is rather hard, especially if we are
concerned about race conditions, but proper setup would be to have the application write to a form of audit log, which would then be periodically processed and results stored.

##### Controller

There are many ways of tying the model and view together. You could go with sophisticated tools that require a lot of manual labor just to get up and running. Like thrift,
or similar, whicih would require writing and maintaining C definition files, for all the exposed API (including defining custom structs and objects as transports). It's 
a problematic approach, especially when we are working with a black box library, which return type varies not only from function to function but also on some internal
switches (for example hypothesis, ideally, should return a different structure than observation, and even observations can be way different from one another). It presents
very similar problem on the entry point, which makes this problem even worse. While there is the added benefit of then easily joining it up with any language, the high
maintenance costs and even higher entry costs made me run away from this idea rather quickly.
Instead I've embraced a higher-level idea of not only a messaging system, but also messaging broker known as celery. Primarily because it allows for extremely rapid 
deployment, brings very little overhead and doesn't in any way, shape, or form limit the futures of underlying system in any way. Which means that you benefit from teh
ease of development on python, you still can integrate other languages in similar way as you would with the vanilla messaging system. And celery allows us to work with
almost anything (pending a write-up of simple driver, which already exist for most popular choices, including RabbitMQ, kafka, zero, redis and popular databases) as the 
broker and backend, which makes the integration with extrenal languages and systems even easier as you can just wrap what already exists.

Given that nothing exists here yet, I've opted for rabbitMQ for few very strong and simple reasons:

 - Maturity. RabbitMQ is battle tested and has proven to not crumble even in edge cases.
 - Amount of features. Advanced routing, statistics, administrative tools, it's all there and ready out of the box.
 - Rather good performance. Singel rabbitMQ instance on a small box can handle about 20k inserts per second. It is low compared to kafka (100k) but can easily be ammended
 in the future by turning rabbitmq into a cluster, or even, as project grows, seamlessly replacing rabbitmq with kafka as needed.
 - Wide adaptation. Almost all modern languages support it, people know how to use it so it's rather easy to get new people aboard.
 
## Issues - code

Some of the issues/areas of improvement I can see right now (word test repeats in most fo them, they are that important!).

 - Implement a translation functions that takes the currently returned data about nodes and translates into something that can be translated into JSON. Currently the data
 structure returned does not allow that and thus we have to first pickle it, then encode it with base 64, encode to string and finally return to a client.
 - Implement authentication inside of request handlers in bottle. Authentication must be blazing fast, and most likely should call local redis as database, which is refreshed
 periodically from primary database. Eventually a ready solution like cassandra could be rolled out which can do exactly that and more (but is a bit problematic to set up)
 - Expand the tests with proper end-to-end caes for rest service. Right now we just test for malfunctions.
 - Removal of controlling
 - To create instance of graph you have to make api call as follows: `my_graph = graph.graph.Graph()`. This lack of API design would be caugh during either peer review or
 writing tests (if done ahead of time), because when writing tests you have to already think of how you will call and use your application. Even though it doesn't exist yet.
 - Lack of tests means that code is either just assumed to be working, or there is a manual process performed after each changes (lengthy and highly inaccurate). Having BDD
 testing in place not only allows for quick integration and regression testing, but also makes it very easy to get accustomed to what the application does, and how it does it.
 