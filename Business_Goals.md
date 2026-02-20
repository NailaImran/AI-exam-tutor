# Exam Tutor — Business Goals & KPI Tracker

**Last Updated**: 2026-02-20
**Review Frequency**: Weekly (every Sunday, auto-updated by orchestrator)

---

## Q1 2026 Objectives

### Enrollment & Revenue Targets

| Metric | Target | Current | Alert Threshold |
|--------|--------|---------|-----------------|
| Active Students | 50 | 0 | < 10 |
| Monthly Revenue (PKR) | 50,000 | 0 | < 20,000 |
| Trial-to-Paid Conversion | 40% | 0% | < 25% |
| Monthly Churn Rate | < 5% | 0% | > 10% |

### Exam Readiness Targets

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Students at ERI ≥ 60 | 70% | < 50% |
| Avg ERI across all students | 65 | < 50 |
| Students completing diagnostic | 90% | < 70% |
| Daily question response rate | 60% | < 40% |

### Engagement Targets

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| WhatsApp reply rate | 60% | < 40% |
| Avg sessions/student/week | 3 | < 1 |
| Study plan adoption rate | 80% | < 60% |
| LinkedIn post engagement | 100 interactions/post | < 30 |

---

## Active Students

| Student ID | Exam | ERI | Last Session | Days to Exam | Status |
|------------|------|-----|-------------|--------------|--------|
| _(auto-updated by weekly report workflow)_ | | | | | |

---

## Weekly Audit Logic

The orchestrator runs this audit every Sunday at 9 PM PKT.

### Subscription / Cost Audit Rules

Flag for review if:
- Any API cost increases > 20% week-over-week
- WhatsApp API messages fail > 5% of sends
- LinkedIn MCP connection errors > 3 in a week

### Student Engagement Audit Rules

Flag students for intervention if:
- No session in the last 7 days → `disengagement_risk`
- ERI drops more than 5 points in a week → `regression_alert`
- Test answer accuracy < 40% for 3+ consecutive sessions → `struggling`
- Daily question ignored for 5+ consecutive days → `ghosting`

### Revenue Audit Rules

Flag if:
- Monthly revenue < 50% of target by mid-month
- Any payment fails or is disputed
- Trial period expires without conversion

---

## Weekly CEO Briefing

Generated every Monday morning by the orchestrator. Saved to:
`logs/briefings/YYYY-MM-DD_Monday_Briefing.md`

### Briefing Template

```
# Monday Morning Briefing — {date}

## Executive Summary
{1-2 sentence summary}

## Student Metrics
- Active students: {n}
- Avg ERI this week: {score}
- Sessions completed: {n}
- Questions answered: {n}

## Engagement
- WhatsApp reply rate: {pct}%
- Daily question opens: {n}
- Students at risk (no activity 7+ days): {n}

## Highlights
{Top 3 wins this week}

## Flags Requiring Attention
{Any triggered alert thresholds}

## Recommended Actions
{AI-generated suggestions}
```

---

## Exam Calendar

| Exam | Typical Announcement | Test Window |
|------|---------------------|-------------|
| PPSC | 3-4 months before test | Rolling |
| SPSC | 2-3 months before test | Rolling |
| KPPSC | 2-3 months before test | Rolling |

---

*Auto-updated by AI Exam Tutor Orchestrator | Review every Sunday*
