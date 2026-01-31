# Skill: social-post-generator

**Category**: SUPPORTING (Phase 3)
**Purpose**: Generate daily question posts for LinkedIn with proper formatting, hashtags, and character limits

## Description

The social-post-generator skill creates engaging LinkedIn posts featuring practice questions from the exam question bank. It selects questions using subject rotation, formats them according to the LinkedIn template, adds appropriate hashtags, validates character limits, and saves drafts for human approval.

## Input

```json
{
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "excluded_question_ids": ["string array of question IDs to skip (optional)"],
  "target_topic": "string (optional, for specific topic focus)",
  "scheduled_for": "string ISO 8601 (optional, defaults to next day 9 AM PKT)"
}
```

## Output

```json
{
  "success": "boolean",
  "post": {
    "post_id": "string linkedin-YYYY-MM-DD",
    "platform": "linkedin",
    "created_at": "string ISO 8601",
    "scheduled_for": "string ISO 8601",
    "status": "draft | pending_approval",
    "content": {
      "text": "string (full post text)",
      "hashtags": ["string array"],
      "question": {
        "id": "string",
        "text": "string",
        "options": {"A": "", "B": "", "C": "", "D": ""},
        "topic": "string",
        "exam_type": "string"
      },
      "image_path": "string | null"
    },
    "character_count": "integer",
    "approval": {
      "submitted_at": "string ISO 8601 | null",
      "reviewed_at": "null",
      "reviewer": "null",
      "decision": "null",
      "feedback": "null"
    }
  },
  "draft_path": "string (needs_action path)",
  "error": "string | null"
}
```

## Workflow

### 1. Select Question

Use daily-question-selector skill with subject rotation:

```javascript
const selection = await daily_question_selector({
  exam_type: exam_type,
  mode: "linkedin",
  excluded_ids: excluded_question_ids
})

// Get question details
const question = selection.question
```

### 2. Load Template

```
Read: specs/phase-3-core-tutoring/contracts/linkedin-post-template.json
```

### 3. Select Hashtags

```javascript
function selectHashtags(exam_type, topic, template) {
  const hashtags = []

  // Add exam-specific hashtags (pick 2)
  const exam_tags = template.hashtag_mapping[exam_type] || []
  hashtags.push(...exam_tags.slice(0, 2))

  // Add topic-specific hashtags (pick 1)
  const topic_tags = template.topic_hashtags[topic] || []
  if (topic_tags.length > 0) {
    hashtags.push(topic_tags[0])
  }

  // Add general hashtags to fill up to 5
  const general_tags = ["#ExamPreparation", "#MCQ", "#Pakistan"]
  while (hashtags.length < 5 && general_tags.length > 0) {
    hashtags.push(general_tags.shift())
  }

  return hashtags.slice(0, 5) // Max 5 hashtags
}
```

### 4. Format Post

```javascript
function formatPost(question, exam_type, hashtags, template) {
  const format = template.template.format

  let post_text = ""

  // Build post from template sections
  post_text += format.intro.replace("{{exam_type}}", exam_type)
  post_text += format.topic_line.replace("{{topic}}", question.topic)
  post_text += format.question.replace("{{question_text}}", question.text)
  post_text += format.options
    .replace("{{option_a}}", question.options.A)
    .replace("{{option_b}}", question.options.B)
    .replace("{{option_c}}", question.options.C)
    .replace("{{option_d}}", question.options.D)
  post_text += format.engagement
  post_text += hashtags.join(" ")

  return post_text
}
```

### 5. Validate Character Limit

```javascript
function validateCharacterLimit(post_text, max_length = 3000) {
  const char_count = post_text.length

  if (char_count > max_length) {
    return {
      valid: false,
      error: `Post exceeds ${max_length} character limit (${char_count} chars)`,
      char_count: char_count
    }
  }

  return {
    valid: true,
    char_count: char_count
  }
}
```

### 6. Build SocialPost Object

```javascript
const today = new Date().toISOString().split('T')[0]
const post_id = `linkedin-${today}`

const social_post = {
  "$schema": "exam-tutor/social-post/v1",
  "post_id": post_id,
  "platform": "linkedin",
  "created_at": new Date().toISOString(),
  "scheduled_for": scheduled_for || getNextScheduledTime(),
  "status": "pending_approval",
  "approval": {
    "submitted_at": new Date().toISOString(),
    "reviewed_at": null,
    "reviewer": null,
    "decision": null,
    "feedback": null
  },
  "content": {
    "text": post_text,
    "hashtags": hashtags,
    "question": {
      "id": question.id,
      "text": question.text,
      "options": question.options,
      "topic": question.topic,
      "exam_type": exam_type
    },
    "image_path": null
  },
  "published_at": null,
  "engagement": {
    "likes": null,
    "comments": null,
    "shares": null
  }
}
```

### 7. Save Draft for Approval

```javascript
const draft_path = `needs_action/social-posts/${post_id}.json`
write_file(draft_path, JSON.stringify(social_post, null, 2))
```

### 8. Track Subject Rotation

```javascript
// Update rotation tracking to avoid repeats
const rotation_file = "schedules/linkedin-rotation.json"
const rotation = read_file(rotation_file) || { last_topics: [], last_questions: [] }

rotation.last_topics.unshift(question.topic)
rotation.last_topics = rotation.last_topics.slice(0, 7) // Keep 7 days

rotation.last_questions.unshift(question.id)
rotation.last_questions = rotation.last_questions.slice(0, 30) // Keep 30 days

write_file(rotation_file, JSON.stringify(rotation, null, 2))
```

## Hashtag Reference

### Exam-Specific Hashtags

| Exam | Hashtags |
|------|----------|
| SPSC | #SPSC, #SindhPublicServiceCommission, #SindhJobs |
| PPSC | #PPSC, #PunjabPublicServiceCommission, #PunjabJobs |
| KPPSC | #KPPSC, #KPKPublicServiceCommission, #KPKJobs |

### Topic Hashtags

| Topic | Hashtags |
|-------|----------|
| Constitutional Development | #ConstitutionOfPakistan, #Law |
| Independence Movement | #PakistanHistory, #14August |
| Geography of Pakistan | #Geography, #PakistanGeography |
| General Knowledge | #GK, #GeneralKnowledge |
| Current Affairs | #CurrentAffairs, #News |
| Islamic Studies | #IslamicStudies, #Islam |

### General Hashtags

- #ExamPreparation
- #MCQ
- #Pakistan
- #CivilServices
- #DailyQuiz

## Constraints

| Constraint | Value | Source |
|------------|-------|--------|
| Max text length | 3000 characters | LinkedIn API |
| Max hashtags | 5 | Best practice |
| Image required | No | Optional |
| Mentions allowed | No | Disabled |

## MCP Tools Used

- `mcp__filesystem__read_file` - Load template, question bank, rotation tracking
- `mcp__filesystem__write_file` - Save draft to needs_action/
- `mcp__linkedin__create_post` - Publish approved post (via approval-workflow)

## Error Handling

| Error | Action |
|-------|--------|
| No questions available | Return error, suggest adding questions for exam_type |
| Character limit exceeded | Truncate explanation or return error |
| Template not found | Return error with template path |
| All topics recently used | Reset rotation and pick any topic |
| Question already used | Skip and select next question |

## Example Usage

### Generate Daily Post

```json
Input: {
  "exam_type": "PPSC",
  "excluded_question_ids": []
}

Output: {
  "success": true,
  "post": {
    "post_id": "linkedin-2026-01-31",
    "platform": "linkedin",
    "created_at": "2026-01-31T03:00:00Z",
    "scheduled_for": "2026-02-01T04:00:00Z",
    "status": "pending_approval",
    "content": {
      "text": "📚 Daily PPSC Practice Question\n\nTopic: Constitutional Development\n\nThe 18th Amendment was passed in:\n\nA) 2008\nB) 2010\nC) 2012\nD) 2014\n\n💬 Comment your answer below!\n🔔 Follow for daily questions\n\n#PPSC #PunjabPublicServiceCommission #ConstitutionOfPakistan #ExamPreparation #MCQ",
      "hashtags": ["#PPSC", "#PunjabPublicServiceCommission", "#ConstitutionOfPakistan", "#ExamPreparation", "#MCQ"],
      "question": {
        "id": "PPSC-PK-089",
        "text": "The 18th Amendment was passed in:",
        "options": {"A": "2008", "B": "2010", "C": "2012", "D": "2014"},
        "topic": "Constitutional Development",
        "exam_type": "PPSC"
      },
      "image_path": null
    },
    "character_count": 298,
    "approval": {
      "submitted_at": "2026-01-31T03:00:00Z",
      "reviewed_at": null,
      "reviewer": null,
      "decision": null,
      "feedback": null
    }
  },
  "draft_path": "needs_action/social-posts/linkedin-2026-01-31.json",
  "error": null
}
```

### Generate for Specific Topic

```json
Input: {
  "exam_type": "SPSC",
  "target_topic": "Geography of Pakistan"
}

Output: {
  "success": true,
  "post": {
    "post_id": "linkedin-2026-01-31",
    "content": {
      "text": "📚 Daily SPSC Practice Question\n\nTopic: Geography of Pakistan\n\nThe highest peak of Pakistan is:\n\nA) Nanga Parbat\nB) K2\nC) Tirich Mir\nD) Rakaposhi\n\n💬 Comment your answer below!\n🔔 Follow for daily questions\n\n#SPSC #SindhPublicServiceCommission #Geography #ExamPreparation #MCQ",
      ...
    }
  }
}
```

## Constitution Compliance

- **Principle VI (Bounded Autonomy)**: Posts require human approval before publishing
- **Principle III (Data-Driven)**: Uses question bank data for content

## Related Skills

- daily-question-selector (selects questions with rotation)
- approval-workflow (handles approval/rejection)
- question-bank-querier (retrieves question details)
