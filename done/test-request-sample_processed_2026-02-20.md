---
type: test-request
student_id: test-student
exam_type: PPSC
subject: Pakistan Studies
question_count: 5
difficulty: adaptive
session_type: practice
---

# Sample Test Request

This is a sample test request for the test-student profile.

**Requested:**
- 5 questions from Pakistan Studies
- Adaptive difficulty based on student level
- PPSC exam format

**Instructions:**
1. Load student profile using student-profile-loader
2. Query questions using question-bank-querier
3. Present questions to student
4. After answers received, evaluate using answer-evaluator
5. Save results using performance-tracker
