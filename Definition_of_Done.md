# **MediLink — Definition of Done (DoD)**

## **1. Purpose**

The Definition of Done establishes the minimum quality standards that every MediLink work item must satisfy before being considered complete.

This checklist helps the team maintain consistent quality, reduce defects, improve collaboration, and ensure that verification activities are not skipped.

## **2. Definition of Done Checklist**

A work item can only move to the **Done** column when all applicable criteria below have been satisfied.

### **Requirements and Acceptance Criteria**

- [ ] The issue has a clear description and assigned owner.
- [ ] All applicable acceptance criteria have been satisfied.
- [ ] The completed work matches the agreed requirements.
- [ ] Any changes to the original requirements are documented.

### **Implementation and Code Quality**

- [ ] Required implementation or documentation changes are completed.
- [ ] Code follows the team's agreed coding standards, where applicable.
- [ ] Relevant changes are committed to the GitHub repository.
- [ ] No known critical defects remain unresolved.

### **Code Review**

- [ ] A pull request or documented review activity has been completed.
- [ ] At least one other team member has reviewed the work.
- [ ] Reviewer feedback has been addressed or documented.
- [ ] Required approvals have been obtained before merging, where applicable.

### **Testing and Verification**

- [ ] Relevant tests or verification activities have been completed.
- [ ] Test results or verification evidence are documented.
- [ ] All applicable acceptance criteria have been verified.
- [ ] Any identified defects have been resolved or documented for follow-up.
- [ ] Verification is completed before moving the issue to Done.

### **Documentation**

- [ ] Relevant technical documentation has been updated when necessary.
- [ ] Important implementation decisions are documented.
- [ ] The GitHub issue includes references to related pull requests, test results, or supporting evidence.

### **Workflow Completion**

- [ ] The issue has passed through the required workflow stages.
- [ ] All required checklist items are completed.
- [ ] The Engineering Manager or designated reviewer confirms that the Definition of Done has been satisfied.
- [ ] The issue is moved to the **Done** column only after verification is complete.

## **3. Workflow Stages**

The MediLink team follows this development workflow:

**Backlog → Ready → In Progress → Code Review → Verification → Done**

Each work item must satisfy the relevant requirements of its current stage before advancing to the next.

## **4. Application of the Definition of Done**

The Definition of Done applies to all MediLink work items, including:

- **Features:** Required functionality meets acceptance criteria and passes testing.
- **Defects:** The reported problem is addressed and relevant verification is completed.
- **Maintenance:** Changes improve maintainability without introducing regressions.
- **Technical Tasks:** Technical objectives are achieved and verified.
- **Documentation Tasks:** Documentation is complete, accurate, and reviewed by another team member.

For simulated work without an implemented application, the team must clearly identify the scope of the simulation and provide evidence of the activities actually completed. An untested or unimplemented feature must not be reported as successfully verified.

## **5. Team Responsibility**

- **Developers:** Complete assigned work, document progress, perform appropriate tests, and request reviews.
- **Reviewers:** Evaluate submitted work, provide feedback, and confirm relevant quality requirements.
- **Engineering Manager:** Monitor workflow compliance, resolve process blockers, and ensure that verification activities are not skipped.

## **6. Continuous Improvement**

The team will review the Definition of Done when recurring defects, incomplete handoffs, or missed verification activities are identified.

Any proposed changes to the Definition of Done should be discussed collaboratively and documented.

**A work item is considered Done only when the team has sufficient evidence that all applicable quality requirements have been met.**
