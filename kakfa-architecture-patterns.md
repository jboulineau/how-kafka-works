# Kafka Architecture Patterns

## Important Architecture Questions

1. Synchronous or Asynchronous?
2. Events or Messages?
3. How can you implement idempotence?
4. Is horizontal scaling a requirement?
5. Do you have to maintain transactional awareness across multiple processes?
6. How do you manage message ordering?
7. How should events be distributed across partitions or topics?
8. Are these meaningful business events?

## File Extracts

```text
+------------------------+           +---------------------+         +-----------------------+     +-----------------------+
| Service                |           |Topic                |         | Service               |     | Service               |
|                        |           |                     |         |                       |     |                       |
| Extract Scheduler      +---------->+ Extract_Scheduled   +----+--->+ Extract Processor     |---->+ Extract Delivery      |
|                        |           |                     |    |    |                       |     |                       |
+------------------------+           +---------------------+    |    +-----------------------+     +-----------------------+
                                                                |
                                                                |    +-----------------------+     +-----------------------+
                                                                |    | Service               |     | Service               |
                                                                |    |                       |     |                       |
                                                                +--->+ Extract Processor     |---->+ Extract Delivery      |
                                                                     |                       |     |                       |
                                                                     +-----------------------+     +-----------------------+
```

1. Synchronous or Asynchronous?
2. Events or Messages?
3. How can you implement idempotence?
4. Is horizontal scaling a requirement?
5. Do you have to maintain transactional awareness across multiple processes?
6. How do you manage message ordering?
7. How should events be distributed across partitions?
8. Are these meaningful business events?

## IOT

``` text
+-------------------+              +---------------------+            +----------------------+
|                   |              |                     |            |                      |
| Service           |              |  Topic              |            |  Service             |
|                   +-------+-----<+                     +------+----<+                      |
| IOT device        |       |      |  Telemetry Event    |      |     |  Telemetry processor |
|                   |       |      |                     |      |     |                      |
+-------------------+       |      +---------------------+      |     +----------------------+
                            |                                   |
+-------------------+       |                                   |
|                   |       |                                   |     +----------------------+
| Service           |       |                                   |     |                      |
|                   +-------+                                   +---->+ Service              |
| IOT device        |                                                 |                      |
|                   |                                                 | Anomaly Detection    |
+-------------------+                                                 |                      |
                                                                      +----------------------+
```

1. Synchronous or Asynchronous?
2. Events or Messages?
3. How can you implement idempotence?
4. Is horizontal scaling a requirement?
5. Do you have to maintain transactional awareness across multiple processes?
6. How do you manage message ordering?
7. How should events be distributed across partitions?
8. Are these meaningful business events?

## New Employee Onboarding

``` text
+----------------------+            +-----------------+           +-------------------------+
| Service              |            | Topic           |           | Service                 |
|                      +----------->+                 +-----+---->+                         |
| HR Onboarding        |            | Employee Hired  |     |     | Network User Creation   |
|                      |            |                 |     |     |                         |
+----------------------+            +-----------------+     |     +-------------------------+
                                                            |
                                                            |     +-------------------------+
                                                            |     | Service                 |
                                                            +---->+                         |
                                                            |     | Benefits Enrollment      |
                                                            |     |                         |
                                                            |     +-------------------------+
                                                            |
                                                            |     +-------------------------+
                                                            |     | Service                 |
                                                            +---->+                         |
                                                                  | Background Check        |
                                                                  |                         |
                                                                  +-------------------------+
```

1. Synchronous or Asynchronous?
2. Events or Messages?
3. How can you implement idempotence?
4. Is horizontal scaling a requirement?
5. Do you have to maintain transactional awareness across multiple processes?
6. How do you manage message ordering?
7. How should events be distributed across partitions?
8. Are these meaningful business events?

## Account Transactions

``` text
+-------------------+    +----------------------+       +--------------------------+
| Service           |    | Topic                |       | Service                  |
|                   |    |                      |       |                          |
| ATM               +--->+ Account Transaction  +---+-->+ Transaction Processor    |
|                   |    |                      |   |   |                          |
+-------------------+    +----------------------+   |   +--------------------------+
                                                    |
                                                    |   +--------------------------+
                                                    |   | Service                  |
                                                    |   |                          |
                                                    +-->+ Limit governor           |
                                                    |   |                          |
                                                    |   +--------------------------+
                                                    |
                                                    |   +--------------------------+
                                                    |   | Service                  |
                                                    |   |                          |
                                                    +-->+ Customer Communications  |
                                                        |                          |
                                                        +--------------------------+
```

1. Synchronous or Asynchronous?
2. Events or Messages?
3. How can you implement idempotence?
4. Is horizontal scaling a requirement?
5. Do you have to maintain transactional awareness across multiple processes?
6. How do you manage message ordering?
7. How should events be distributed across partitions?
8. Are these meaningful business events?

## Caching

``` text
+--------------------+     +---------------------+     +-------------------------+
|                    |     |                     |     |                         |
| Service            |     |  Topic              |     |  Service                |
|                    |     |                     |     |                         |
| CRM                +--+--+  Customer Created   +--^->+  Operational Data Cache |
|                    |  |  |                     |  |  |                         |
+---------------------  |  +---------------------+  |  +-------------------------+
                        |                           |
                        |                           |
                        |  +---------------------+  |
                        |  |                     |  |
                        |  |  Topic              |  |
                        |  |                     |  |
                        +--+  Customer Updated   +--+
                           |                     |
                           +---------------------+
```

1. Synchronous or Asynchronous?
2. Events or Messages?
3. How can you implement idempotence?
4. Is horizontal scaling a requirement?
5. Do you have to maintain transactional awareness across multiple processes?
6. How do you manage message ordering?
7. How should events be distributed across partitions?
8. Are these meaningful business events?

## Final Thoughts

1. Event Driven Architecture can be a very complicated way of solving application architecture problems. It's best to avoid it if you can. (But, remember analytics and future use cases.)
2. Architect the system, not the components. Idempotence is a SYSTEM property, for instance.
3. Kafka is not a pattern; there are many patterns that Kafka can be used to enable.
4. The devil is in the details.
