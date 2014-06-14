# mutated-mongo

### What is it?

Mutated mongo listens to the MongoDB oplog for changes that occur within the database. It also manages lists of clients that want to subscribe to these updates.

Clients can subsribe to

* Any change that occurs within a collection
* Changes that occur on a record (identified by an `_id`)
* Changes that occur on records that fall in scope of a query

### How do I use it?

Firstly, you'll need MongoDB running in a state where it offers an oplog. Once you've got that, all you should need to do is the following:

   $ pip install -r requirements.txt
   $ python mutated.py

The mutated server will now be running. You can test that it's all up ok by running the client like so:

   $ python test_client.py

The client library (in `client.py`) will allow you to integrate this server into any of your python projects.

### Still under development

I've still got considerable to work to do on this. The client socket handling from the server is a bit buggy. There's some awkwardness when performing object queries on the oplog records as to which field ("o" or "o2") that I still need to work out . . .


