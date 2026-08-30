"""Adapters that connect the domain to external systems and infrastructure.

Adapters provide concrete implementations for interfaces required by the
application and domain layers. They isolate infrastructure concerns such as
database persistence, password hashing, and other external services from
the core application logic.

Examples:
    - UserRepository: Persists and retrieves User objects from the database.
    - PasswordHasher: Hashes passwords and verifies passwords against stored
      password hashes.
    - ORM models and mappers: Translate between domain objects and database
      records.
"""