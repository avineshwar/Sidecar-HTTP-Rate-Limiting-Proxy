# Sidecar-HTTP-Rate-Limiting-Proxy

###### Sidecar: Any utility software that is complimentary i.e. it exist to facilitate any existing server or container. Also, it means that it makes little to no sense for its existence all by itself.


##### High-level goals:
- Implement a realistic rate limitation (route and method independent, _for the time being for simplicity_)
-- As an added benefit, protection against contention/DDoS is also achievable
- Make the adoption of service mesh easier
- Ensure the application for which rate limitation is being implemented stays free from doing any extra burden
- Accelerate the possibilities of architecture maturity via compartmentalization and isolation
