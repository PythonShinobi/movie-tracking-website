"""Application services for coordinating application use cases.

Application services orchestrate application workflows by coordinating
domain objects, repositories, and other application components. They
contain use-case logic without handling HTTP requests or direct database
operations.

Examples:
    - AuthenticationService.register(): Registers a new user.
    - AuthenticationService.login(): Authenticates a user using their
      email and password.
    - Future services may coordinate workflows such as updating a user
      profile or managing a user's movie collection.
"""