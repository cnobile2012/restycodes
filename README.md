Resty Codes
===========

A Python implementation of the HTTP response codes.

This API implements version 1.0 of my diagram, but which is based on version 3
of Alen Dean's work. Alen Dean's diagram can be downloaded from:

http://code.google.com/p/http-headers-status/


Deviations In My Diagram
------------------------

There are two basic areas in Alen Dean's diagram in which I believe there are
errors.

1. After reading everything I could get my hands on I have never found a
   reference to why a 202 Accepted could not be in a response of a GET, HEAD,
   POST, or PUT although Alen seems to only allow this in the case of a
   DELETE. In the RFC-2616 10.2.2 (201 Created) it says "If the action cannot 
   be carried out immediately, the server SHOULD respond with 202 (Accepted) 
   response instead". It does not indicate that the action should only be a 
   DELETE, so I have included all actions (methods). Both a PUT and POST can 
   cause a 202 in the response though there is no mention in the RFC about 
   a GET or HEAD method with regards to a 202, but I see no reason why a 202 
   should not be possible. Consider a situation where the origin server is not 
   able to fulfill a GET or HEAD request immediately, but needs to delay it 
   for some future time.

2. Another possible issue with Alen Dean's diagram is that updates are routed
   through P11 (New resource) condition. An update by definition would never
   create a new resource, so why does it go through this condition? My diagram
   does not take this route at all. The create and update conditions are
   completely separate and, I feel, making my diagram simpler.

3. The decision "New resource" was renamed to "New resource created". Though
   not an error I believe this name change makes the purpose of the decision
   clearer.

New Diagram Notes
-----------------

1. The major decision point in the diagram is at G7 (Resource exists?). Here
   is where an updated or a created resource is determined.

2. A point of confusion is what does B32 actually do? This is a decision
   that would be made by the origin server as to weather or not a resource
   existed on a URI at a time in the past or not. The response may be a 301,
   307, 410, or a new resource created on a missing resource by the POST
   method.

The Python Code
---------------

There are actually two apps in one in Resty Codes. The Rules Engine and Resty
Codes itself.

### Rules Engine

> The decision making process is the Rules Engine which is written around a 
> binary tree. It can be used completely independently of Resty Codes. The 
> RulesEngine class can either be inherited or a composite in your class. See
> the unittests for an example of usage.

> RulesEngine class has four exposed methods:

> > RulesEngine.load(seq) -- Loads the sequence (seq) into Node objects, later 
> > used when dump is called. The root Node of the binary tree is returned.

> > RulesEngine.dump(**kwargs) -- Executes the binary tree applying the keyword 
> > arguments to the methods in the Nodes. The return value is the Boolean of 
> > the first object executed. Having a return value here is somewhat useless,
> > but could come in handy.

> > RulesEngine.getIterationCount() -- Returns the actual decision tree count 
> > for the kwargs passed to the dump methods. Used mostly for debugging.

> > RulesEngine.getCallSequence() -- Returns a list of the methods that were 
> > executes in the order of execution. Used mostly for debugging.

### Resty Codes

> There are at this time 49 conditions in version 1.0 of my diagram. This
> translates to 49 keyword arguments that can be set to True or False. See
> the unittests for an example of usage.

> The module has two exposed dictionaries and one function:

> > STATUS_CODE_MAP -- A module dictionary object that holds all the response 
> > codes.

> > RESTYARGS -- A module dictionary object that defines the 49 keyword objects 
> > and their default Boolean value.

> > getCodeStatus(code) -- A module function that creates a tuple of the code 
> > and status text.

> RestyCodes class has two exposed methods:

> > RestyCodes.getStatus(**kwargs) -- Returns a tuple containing the status code
> > and the status description. eg. (200, "OK")

> > RestyCodes.setConditions(**kwargs) -- A convenience method that sets the 
> > argument kwargs in a copy of RESTYARGS. The returned kwargs are suitable 
> > for passing into RestyCodes.getStatus(**kwargs).

--------------------------------------------------------------------------------

Comments and discussion on this topic are welcome. Please contact me at:

carl dot nobile at gmail.com
