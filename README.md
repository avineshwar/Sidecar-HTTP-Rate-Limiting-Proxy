# Sidecar-HTTP-Rate-Limiting-Proxy

###### Sidecar: Any utility software that is complimentary i.e. it exist to facilitate any existing server or container. Also, it means that it makes little to no sense for its existence all by itself.


##### High-level goals:
- Implement a realistic rate limitation (route and method independent, _for the time being for simplicity_)
- Protection against contention/DDoS is also achievable via information sharing to some appropriate master for achieving restrictions at L7
- Make the adoption of service mesh easier
- Ensure the application for which rate limitation is being implemented stays free from taking any extra burden
- Accelerate the possibilities of architecture maturity via compartmentalization and isolation


##### Implementation overview:
- The program contains a server (S) and a client (C)
- For any web client (WC), the S portion is listening and the C portion is used to request upstream for WC.
- Unless any failure condition is met, the S portion will forward a request to the C portion and upon getting a response (**timeouts are not handled**), the C portion will make it available for the S portion which will then relay it back to WC. In a way, this is a minimalistic reverse proxy with specific end goals.


##### Language overview:
- As you might have noticed, it is a Python-based implementation. Specifically, it is Python 2.7.
- Best effort strategy is currently in effect i.e. wherever possible, appropriate and current libraries are used. These might factor into simplicity, reliability, and reusability over speed and potential needs of modification, if any.


##### Architecture overview:
- Primitive error handling is taken care off.
- The current design supports horizontal scalability. An extension towards multi-threaded will make vertical scalability attainable, if needed.
- Libraries are used over socket creation. This supports the goal of production readiness in an agile setting.


##### Running instructions:
- Ensure Python 2.7 is installed (at `/usr/bin/python`)
- Make the file executable (`chmod u+x HRLP.py`)
- Run the file (`./HRLP.py`)


##### Gotchas & Considerations:
- 1
- 2
- 3
