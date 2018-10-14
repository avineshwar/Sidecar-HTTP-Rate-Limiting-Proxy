# Sidecar-HTTP-Rate-Limiting-Proxy

###### Sidecar: Any utility software that is complimentary i.e. it exist to facilitate any existing server or container. Also, it means that it makes little to no sense for its existence all by itself.


##### High-level goals:
- Implement a realistic rate limitation (route independent GET-only, _for the time being for simplicity_)
- Protection against contention/DDoS is also achievable via information sharing to some appropriate master (control plane) for achieving restrictions at L7
- Make the adoption of service mesh easier
- Ensure the application for which rate limitation is being implemented stays free from taking any extra burden
- Accelerate the possibilities of architecture maturity via compartmentalization and isolation


##### Implementation overview:
- The program contains a server (S) and a client (C)
- For any web client (WC), the S portion is listening and the C portion is used to request upstream for WC.
- Unless any failure condition is met (HTTP 429 is returned whenever more than allowed number of requests are made within a pre-set time window), the S portion will forward a request to the C portion and upon getting a response (**timeouts are not handled**), the C portion will make it available for the S portion which will then relay it back to WC. In a way, this is a minimalistic reverse proxy with specific end goals.


##### Language overview:
- As you might have noticed, it is a Python-based implementation. Specifically, it is Python 2.7.
- Best effort strategy is currently in effect i.e. wherever possible, appropriate and current libraries are used. These might factor into simplicity, reliability, and reusability over speed and potential needs of modification, if any.


##### Architecture overview:
- Primitive error handling is taken care off.
- The current design supports horizontal scalability. An extension towards multi-threaded will make vertical scalability attainable, if needed.
- Natively offered libraries are used. Also, socket creation is avoided as a best practice. This supports the goal of production readiness in an agile setting.


##### Running instructions:
- Ensure Python 2.7 is installed (and available at `/usr/bin/python`)
- Make the file executable (`chmod u+x HRLP.py`)
- Run the file (`./HRLP.py`)


##### Highlights, Gotchas & Considerations:
- Some reasons behind using native offerings: promotes code reusability, help avoiding anti-patterns, promotes production readiness, supports cross compatibility. This was a whole hearted thought and is fairly exercised.
- From a surface-level inspection, errors can seem non-trivial to understand. A common such scenario is when `HRLP.py` is attempted to run and tested (via browser, for example) locally, a mismatch in the initial **Host** header (sent from WC to the S portion) and the forwarded header (from the S portion to the C portion) could result in an unexpected (from WC's perspective; _but safe and by design_) response. **A proxy is not suppose handle it; WC, being a user-side component, is an untrusted entity.**
- There are 3 ways to reduce bugs (security issues included): **eliminate surface level bugs** (easily identifiable items: missing error handling, scan results, misconfigurations, known limitations and issues, et cetera), **reduce untrusted code** (i.e. the amount of code which could be juiced without any loss of functionality and experience from a client perspective), **reduce trusted code** (things in which we put our implicit trust i.e. a compromise in a trusted component would break some kind of user guarantee, albeit it is not supposed to be a security issue). _This is also attempted but remains an ideal place to be_.
- _Potentially security considerations:_ Any client-side data (headers (repeats possible), data, path) can be malicious which will then be forwarded upstream in its bare form. This holds a potential of triggering either a client side (XSS) or a server side (SSRF, HTTP Response Splitting) issue. Upstream application need to have a fair amount of resiliency in-place to avoid any triggers due to an untrusted input; this includes any logical fallacy being triggered due to an untrusted data (example: depending upon any accessor method in question, referring to a variable in which some value has been saved could be safer data access mechanism than referring to an incoming data multiple times as needed. A forwarded pointer offered in the accessor method could point to a duplicate entry, but, this time, it contains a malicious value and the code responsible for doing ends up being trusted and potentially disastrous).
- To ensure a no-to-minimum glitch service, resiliency is important. The proxy needs to support a heartbeat mechanism for an appropriate action by some coordinator process whenever it makes sense; this promotes the adoption of service mesh and promotes close-knit coordination with L5. _This is an implementable feature._
- To support distributed tracing and an easier relatable debbugging, log format needs to be standardized and support unique ids for each incoming request. _This is an implementable feature._
