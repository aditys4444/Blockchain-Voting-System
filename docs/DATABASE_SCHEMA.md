# Database Schema & Entity Relationships

```text
+-------------------+       +--------------------+       +-------------------+
|      users        |       |     elections      |       |    candidates     |
+-------------------+       +--------------------+       +-------------------+
| id (PK)           |<----->| id (PK)            |<----->| id (PK)           |
| email (Unique)    |       | title              |       | election_id (FK)  |
| username (Unique) |       | description        |       | name              |
| hashed_password   |       | status             |       | party             |
| role              |       | start_time         |       | manifesto         |
| created_at        |       | end_time           |       | vote_count        |
+-------------------+       +--------------------+       +-------------------+
          |                           |
          v                           v
+------------------------------------------------+
|                     votes                      |
+------------------------------------------------+
| id (PK)                                        |
| user_id (FK)                                   |
| election_id (FK)                               |
| candidate_id (FK)                              |
| voter_hash (Indexed)                           |
| encrypted_vote                                 |
| tx_hash (Unique)                               |
| block_index                                    |
| receipt_hash (Unique)                          |
+------------------------------------------------+
```

```text
+-------------------+       +--------------------+       +-------------------+
|      blocks       |       |    transactions    |       |    audit_logs     |
+-------------------+       +--------------------+       +-------------------+
| id (PK)           |       | id (PK)            |       | id (PK)           |
| index (Unique)    |<----->| tx_hash (Unique)   |       | user_id           |
| timestamp         |       | block_index        |       | action            |
| previous_hash     |       | election_id        |       | details           |
| hash (Unique)     |       | voter_hash         |       | ip_address        |
| nonce             |       | encrypted_vote     |       | timestamp         |
| merkle_root       |       | signature          |       +-------------------+
| signature         |       +--------------------+
+-------------------+
```
