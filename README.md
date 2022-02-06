# Bussiness rules

1. As a user I want to create my campaigns with: name, subject, body and sender
2. As a user I want to schedule my campaigns to be sent out at a specified date
3. As a user I want to know the status of my campaign
    * Our product owner says that the status should be the following ones
        * draft: When the user creates his campaign and do some updates
        * draft -> scheduled: When the user specifiy a date to be sent
        * draft -> sending: When the user tries to send immediately the campaign
        * scheduled -> sending: When it is time to send the campaign
        * sending -> sent: When the campaign is completely sent to all of its recipients
4. As a user I want to create contact lists
5. As a user I want to specify contact lists for a campaign
6. As a user I want to know the delivery status of my recipients
7. Users will have a daily send limit

# DDD
## Domain modeling
### Entity and Value objects
Entities are objects that needs to be uniquely recognizable among the application by its identification. 
While value objects are objects that we don't care about
their identity instead we care about their properties.
### Aggregate
It is a consistency boundary where 1 or more objects (entities and value objects) collaborate to resolve some business rules. Aggregates should be built thinking in:
1. Transactions: An aggregate should be saved always as a unit
2. Invariants: Aggregates enforce business rules so the application always end in a consistent state after some operation. i.e "A scheduled campaign should have a time to send"
### Aggregate root
The aggregate root is the "gateway" of a specific aggregate, this object is the entrypoint for clients to perform business rules. Some rules that an aggregate root should follow:
1. The communication between aggregates should be between aggregate roots
2. There should be one repository per aggregate
3. When a change to any object within the AGGREGATE boundary is committed, all invariants of the whole AGGREGATE must be satisfied.
