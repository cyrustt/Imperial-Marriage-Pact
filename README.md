# Imperial Marriage Pact (Custom Implementation)

This project is a student-built implementation of a campus-wide matching system inspired by the Marriage Pact concept, which uses algorithms to pair individuals based on compatibility.

The version I worked on focuses on building a functional matching pipeline from survey data to final pairings, with an emphasis on algorithm design and practical deployment.

---

## Overview

The goal of the project is to:

- Collect structured preference data via survey  
- Convert qualitative responses into numerical features  
- Compute compatibility between participants  
- Generate stable matches using algorithmic methods  

The system is inspired by the **Gale-Shapley stable matching algorithm**, which ensures that no two individuals would both prefer each other over their assigned match.

As described in a student news feature, the project was:

> “an algorithm-based form that matches students to find the optimal life partner”  [oai_citation:0‡Felix](https://felixonline.co.uk/articles/imperial-marriage-pact/?utm_source=chatgpt.com)  

Article: https://felixonline.co.uk/articles/imperial-marriage-pact/

---

## Implementation

The core implementation is located in:

/files

This subfolder contains:
- the matching algorithm  
- data preprocessing logic  
- compatibility scoring functions  

The pipeline works as follows:

1. **Survey Processing**
   - Responses are mapped to numerical values  

2. **Feature Construction**
   - Each participant is represented as a vector of preferences  

3. **Compatibility Scoring**
   - Pairwise scores are computed between participants  

4. **Matching Algorithm**
   - A stable matching algorithm is used to generate final pairings  

---

## What I Built

Through this project, I implemented:

- Data processing pipeline from raw survey inputs  
- Compatibility scoring logic  
- Matching algorithm (stable matching variant)  
- End-to-end workflow from input → output  

The system was designed and implemented under real constraints (time, data quality, participation imbalance), which required making practical tradeoffs in both modeling and engineering.

---

## Challenges

Some key challenges included:

- Designing a scoring system from subjective survey data  
- Handling imbalanced participant groups  
- Ensuring stability and fairness in matching  
- Working with incomplete or noisy real-world inputs  

---

## Notes

- This implementation is independent and not affiliated with the official Marriage Pact organization  
- The goal was to build a working system rather than replicate proprietary methods  

---

## Why this project

This project reflects my interest in:

- algorithmic decision-making  
- translating theory (matching algorithms) into real systems  
- building end-to-end products from scratch  

---

## Future Improvements

- More advanced compatibility modeling (e.g. learned weights)  
- Better handling of heterogeneous preferences  
- Scalable deployment for larger participant pools  
