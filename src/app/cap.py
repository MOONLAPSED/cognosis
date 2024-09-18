# /src/app/cap.py - CAP Theorem
"""
SmallTalk's true OOP and CAP Theorem

In SmallTalk, everything is an object, and objects have their own state. This state is stored in a single, centralized image, which is the source of truth for the entire system. When an object receives a message, it can modify its state, and the updated state is stored in the image.

Now, let's analyze how this architecture affects the CAP Theorem:

    Consistency: SmallTalk's image-based persistence ensures that the system state is consistent, as all objects' states are stored in a single, centralized image. This means that every read operation will see the most recent write or an error. Score: 1/3 (Consistency: Strong)
    Availability: Since the entire system state is stored in a single image, if the image is unavailable, the system is unavailable. This means that SmallTalk's architecture is not designed for high availability. Score: 0/3 (Availability: Low)
    Partition tolerance: SmallTalk's architecture is not partition-tolerant, as the system relies on a single, centralized image. If the image is split or becomes unavailable due to a network partition, the system will not be able to operate. Score: 0/3 (Partition Tolerance: Low)

The losses in availability and partition tolerance are due to the following:

    Single point of failure: The centralized image is a single point of failure. If it becomes unavailable, the entire system is unavailable.
    No redundancy: There is no redundancy in the system, so if the image is lost or corrupted, the system cannot recover.
    No decentralized data storage: The system relies on a single, centralized image, which makes it difficult to scale and distribute the data.

CAP heuristics:
    CA (Consistency + Availability): A system that prioritizes consistency and availability may use a centralized architecture, where all nodes communicate with a single master node. This ensures that all nodes have the same view of the data (consistency), and the system is always available (availability). However, if the master node fails or becomes partitioned, the system may become unavailable (no partition tolerance).
    CP (Consistency + Partition Tolerance): A system that prioritizes consistency and partition tolerance may use a distributed architecture with a consensus protocol (e.g., Paxos or Raft). This ensures that all nodes agree on the state of the data (consistency), even in the presence of network partitions (partition tolerance). However, the system may become unavailable if a partition occurs, as the nodes may not be able to communicate with each other (no availability).
    AP (Availability + Partition Tolerance): A system that prioritizes availability and partition tolerance may use a distributed architecture with eventual consistency (e.g., Cassandra or Riak). This ensures that the system is always available (availability), even in the presence of network partitions (partition tolerance). However, the system may sacrifice consistency, as nodes may have different views of the data (no consistency).

"""
