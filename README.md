Resty Codes
===========

A Python implementation of the HTTP response codes.

This API implements version 1.0 of my diagram, but which is based on version 3
of Alen Dean's work. Alen Dean's diagram can be downloaded from:

http://code.google.com/p/http-headers-status/


Deviations In My Diagram
------------------------

There are two basic area in Alen Dean's diagram which I believe there are
errors.

1) After reading everything I could get my hands on I have never found an
   reference to why a 202 Accepted could not be in a response to a GET, HEAD,
   POST, or PUT though Alen seems to only allow this in the case of a DELETE.
   In the RFC-2616 10.2.2 (201 Created) it says that "the server SHOULD respond
   with 202 (Accepted) response". There is no mention in the RFC about a GET or
   HEAD method with regards to a 202, but I see no reason why a 202 should
   also not be possible.

2) Another possible issue with Alen Dean's diagram is that updates are routed
   through the "New resource" condition. An update by definition would never
   create a new resource, so why does it go through this condition? My diagram
   does not take this route at all. The create and update conditions are
   completely separate and, I feel, making the diagram simpler.

3) The decision "New resource" was renamed to "New resource created". Though
   not an error I believe this name change makes the purpose of the decision
   clearer.

Diagram Notes
-------------

1) The major decision point in the diagram is at G7 (Resource exists?). Here
   is where an updated or a created resource is determined.
2) A point of confusion is what does B32 actually do? This is a decision
   that would be made by the origin server as to weather or not a resource
   existed on a URI at a time in the past or not. The response may be a 301,
   307, 410, or a new resource created on a missing resource by the POST
   method.

Comments and discussion on this topic are welcome. Please contact me at:

carl dot nobile at gmail.com
