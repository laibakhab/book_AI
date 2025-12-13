---
id: 1
title: Create Project Constitution
stage: constitution
date: 2025-12-14
surface: agent
model: gpt-4
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "physical-ai", "robotics"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution   Project Name:
Physical AI & Humanoid Robotics

You are an expert system architect, robotics engineer, and curriculum designer.

You are working on a hackathon and textbook project titled:

"Physical AI & Humanoid Robotics"

Your thinking must strictly follow these principles:

1. Physical AI first
   - AI must operate in the real or simulated physical world
   - Embodied intelligence is mandatory

2. Clear system separation
   - Brain: AI models, planning, reasoning
   - Nervous System: ROS 2 nodes, topics, services
   - Body: Robot or simulator (Gazebo / Isaac)

3. Simulation-first approach
   - All designs must work in simulation before real hardware
   - Prefer Isaac Sim and Gazebo

4. Practical over theoretical
   - Focus on deployable systems
   - Avoid abstract ML theory unless needed

5. Modularity
   - Every component must be replaceable
   - Designed for teaching and hackathon demos

6. Tooling constraints
   - ROS 2 (Python)
   - NVIDIA Isaac ecosystem
   - Jetson Orin for edge deployment
   - LLMs only for planning and language understanding

7. Output expectations
   - Clear architecture diagrams (text-based if needed)
   - Step-by-step breakdowns
   - Content suitable for a technical textbook
   - No unnecessary verbosity

Acknowledge and follow this constitution in all future responses.

## Response snapshot

I've successfully created the updated constitution file based on your requirements. Here's a summary of the changes:

## Summary

- **New Version**: 1.0.0 (initial version for the "Physical AI & Humanoid Robotics" project)
- **Changes Made**: Created a complete constitution document with 6 core principles and additional sections based on your specifications
- **Files Updated**: `.specify/memory/constitution.md`

### Core Principles Established:
1. Physical AI First - requiring AI to operate in the real or simulated physical world
2. Clear System Separation - defining Brain, Nervous System, and Body architecture
3. Simulation-First Approach - all designs must work in simulation first
4. Practical Over Theoretical - focus on deployable systems
5. Modularity - ensuring all components are replaceable
6. Tooling Constraints - specifying ROS 2, NVIDIA Isaac, Jetson Orin, etc.

### Additional Sections:
- Technology Stack Requirements
- Development Workflow
- Governance

There were no dependent templates requiring updates, as the existing templates are compatible with the new constitution.

**Suggested commit message**: `docs: add constitution for Physical AI & Humanoid Robotics project v1.0.0`

## Outcome

- ✅ Impact: Created initial project constitution with 6 core principles and governance structure
- 🧪 Tests: none (documentation update only)
- 📁 Files: Updated .specify/memory/constitution.md with new content
- 🔁 Next prompts: Implementation of features following the new constitution
- 🧠 Reflection: The constitution successfully captures all the key principles from the user requirements and provides clear guidance for the Physical AI & Humanoid Robotics project.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A