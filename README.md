# python-ehealth-connector
Python bridge to the Belgian eHealth Connector

# Intro

As described [here](https://www.ehealth.fgov.be/ehealthplatform/nl/service-ehealth-platform-services-connectors), Belgian eHealth (and associated organisations like MyCareNet) have created connector packages in Java and .NET for the eHealth services.  
The goal of this project is to provide a Python bridge (using py4j) to these connectors:
- The package will run a py4j JavaGateway in the background
- Through py4J we can then bridge with the Java objects in the JVM

This should make it relatively easy to request SAMLTokens or interface with the eHealth services via Python.  I aim to write as little Java code as possible.  As a result, the package will likely not be as performant as it could be, but it should provide much needed flexibility to Python developers.  
I'm hoping to also construct the attribute queries in Python using eg. pydantic-xml or Jinja2 templating, as I find it super cumbersome to work with the Java XML interfaces.

Note: I'm primarily developing for physiotherapists.  So the focus is currently on the MemberData, EAgreement, EFakt and EAttest services.  If other service implementations are needed, feel free to submit a PR.  

# Prerequisites

- Java <16 (Java 16 and higher are incompatible with v4.3.0 of the connector due to issues reading the certificates).  Personally I am using openjdk 15.0.3 and openjdk 11.0.18
- Ubuntu (Windows/Mac will probably work with some minor modifications, eg. to set the CLASSPATH environment variable)

# Installation

- poetry install
- poetry run download-packages (Note that this download 4.3.0 Physiotherapy connector, you may need another one)
- poetry run compile-bridge
- poetry run launch-bridge