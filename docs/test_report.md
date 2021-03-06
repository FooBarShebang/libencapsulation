# Test Report on the Library libencapsulation

## Conventions

Each test is defined following the same format. Each test receives a unique test identifier and a reference to the ID(s) of the requirements it covers (if applicable). The goal of the test is described to clarify what is to be tested. The test steps are described in brief but clear instructions. For each test it is defined what the expected results are for the test to pass. Finally, the test result is given, this can be only pass or fail.

The test format is as follows:

**Test Identifier:** TEST-\[I/A/D/T\]-XYZ

**Requirement ID(s)**: REQ-uvw-xyz

**Verification method:** I/A/D/T

**Test goal:** Description of what is to be tested

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

The test ID starts with the fixed prefix 'TEST'. The prefix is followed by a single letter, which defines the test type / verification method. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the test ordering number for this object. E.g. 'TEST-T-112'. Each test type has its own counter, thus 'TEST-T-112' and 'TEST-A-112' tests are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Tests definition (Test)

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-000        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-FUN-001        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-FUN-002        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-FUN-003        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-FUN-004        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-FUN-005        | TEST-T-003             | YES                      |
| REQ-FUN-006        | TEST-T-000             | YES                      |
| REQ-AWN-000        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-AWN-001        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-AWN-002        | TEST-T-001, TEST-T-002 | YES                      |
| REQ-AWN-003        | TEST-T-001, TEST-T-002 | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | all tests are passed          |
