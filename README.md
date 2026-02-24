# Sustainable Agriculture Smart Farming Ontology Project

#### Student Details
Name: SABAR S.A.

## Overview
This project contains a simple ontology modeling crops and their hierarchical relationships. The ontology allows users to query information about different crop types, their subclasses, and individuals.

The project includes:
- Ontology file (`.owl`)
- SPARQL queries to answer competency questions
- A simple interface for querying the ontology

---

## Classes and Individuals

### Classes
- **Crop**: The top-level class representing all crops.
- **Paddy**: A subclass of `Crop`, representing rice-type crops.

### Individuals
- **Rice1**: An instance of the `Paddy` class.

---

## Relationships
- **Subclass Relationships**
  - `Paddy` is a subclass of `Crop` (`Paddy rdfs:subClassOf Crop`).
- **Type Assertions**
  - `Rice1` is explicitly typed as a `Paddy` (`Rice1 rdf:type Paddy`).
  - By inference, `Rice1` is also recognized as a `Crop`.

---

## Reasoner
- **Reasoner Used:** HermiT
- **Purpose:**  
  The reasoner is used to compute inferred types and subclass relationships. For example, although `Rice1` is explicitly typed as a `Paddy`, the reasoner infers that it is also a `Crop` through the subclass hierarchy. This ensures that all hierarchical relationships are logically consistent and can be queried correctly.

---

## Competency Questions
The ontology is designed to answer the following questions:

1. Which crops belong to the `Crop` class?  
2. What are the types of a given individual (e.g., `Rice1`)?  
3. Which individuals are of type `Paddy`?  
4. What are the subclasses of `Crop`?  
5. Find all individuals along with their types and superclasses.

---

## SPARQL Queries
Example SPARQL queries for the competency questions:

- **All Crops**
```sparql
SELECT ?crop WHERE { ?crop rdf:type sasfo:Crop . }

- **Types of Rice1**
```sparql
SELECT ?type WHERE { sasfo:Rice1 rdf:type ?type . }

- **All Individuals of Paddy**
```sparql
SELECT ?individual WHERE { ?individual rdf:type sasfo:Paddy . }

- **Subclasses of Crop**
```sparql
SELECT ?subclass WHERE { ?subclass rdfs:subClassOf sasfo:Crop . }

- **Individuals with Types and Superclasses**
```sparql
SELECT ?individual ?type ?superclass
WHERE {
    ?individual rdf:type ?type .
    ?type rdfs:subClassOf ?superclass .
}

## Interface

A simple web or desktop interface can be connected to a SPARQL endpoint (e.g., Apache Jena Fuseki or GraphDB).

Users can perform queries, search for individuals or types, and see results dynamically.

The interface interacts with the ontology to provide recommendations or search results based on the defined hierarchy.

## Files Included

*angriculture.owl* – The OWL ontology file

*queries.sparql* – Example SPARQL queries for the competency questions

interface/ – Optional folder for the web/desktop interface files