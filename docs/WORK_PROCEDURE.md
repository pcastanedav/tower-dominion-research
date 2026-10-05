# Work Procedure

This document defines the standard procedure for substantial work in the Tower Dominion analysis repository. Its purpose is to make work incremental, auditable, and easy to resume after an interruption or in a new conversation/session.

## 1. Start every task with a task plan

Before beginning substantive work on a new task, create a task-level planning document in the repository.

The plan must record:
- the task and intended final outcome;
- the ordered implementation/research slices;
- a concise description of what each slice is intended to achieve;
- relevant dependencies or prerequisites between slices;
- the current status of each slice;
- which slice is currently active;
- any task-wide assumptions or constraints that materially affect the work.

A slice should be a small, coherent unit of work that can be completed, checked, documented, and committed independently. Prefer slices that produce a meaningful verified increment rather than arbitrary amounts of work.

The task plan is a living document. Update it as slices complete or when verified findings require the remaining plan to change.

## 2. Maintain an active-slice report

The currently active slice must have its own report file from the time work on that slice begins.

At minimum, the active-slice report records:
- task and slice identity;
- start status/time or session context sufficient to identify when work began;
- the slice objective and expected completion condition;
- starting assumptions and relevant known state;
- substantive intermediate findings;
- decisions that affect subsequent work;
- commands, files, symbols, assets, tests, or other anchors useful for resuming the work when appropriate;
- errors, failures, blockers, or unresolved observations;
- current state and next intended action.

Intermediate chat notifications that materially change an assumption, explain an important discovery, alter the implementation/research direction, or would be useful after an interruption must also be preserved in the slice report. Important state must not exist only in chat history.

The report should contain enough information that partial work can be resumed without reconstructing the entire prior conversation.

## 3. Successful slice completion

A slice is complete only when its intended outcome has been achieved and its relevant verification/checks have succeeded.

On successful completion:
1. Update the slice report with the result, verification performed, important findings, and any consequences for later slices.
2. Mark/update the slice status in the task plan and identify the next slice.
3. Update other durable project documentation when the completed slice changes established knowledge.
4. Commit the completed work and documentation to Git as a slice checkpoint.
5. When the requested workflow calls for continued progress, begin the next slice and create/update its active-slice report before substantive work on it.

Successful slice boundaries are intended to be reliable Git checkpoints from which work can be inspected or resumed.

## 4. Failure or blocker behavior

If an error, failed verification, unexpected result that prevents safe continuation, or other blocker occurs:
1. Do not mark the current slice complete.
2. Do not advance to the next slice.
3. Record the failure/blocker in the current slice report, including enough evidence/context to resume diagnosis.
4. Record the current state and the next plausible diagnostic/recovery action when known.
5. Report the problem to the user and wait for instructions.

A blocked or failed slice must not be represented as a successful checkpoint merely to maintain forward progress.

## 5. Meaning of `progress <n>`

The instruction:

`progress <n>`

means to continue working from the **currently active slice** for up to `<n>` slice progressions/completions, without asking for routine permission between successful slices.

For each slice:
- continue the current slice until its completion condition is met or a failure/blocker occurs;
- if successful, update its report and task plan, update durable documentation as warranted, commit the checkpoint, and continue automatically to the next slice;
- repeat until the requested `<n>` progression count has been satisfied or there are no further planned slices;
- if an error/failure/blocker occurs at any point, document it in the current slice report, report it, stop progression, and wait for instructions.

Routine intermediate discoveries do not by themselves stop `progress <n>` when they can be safely incorporated into the current slice. Findings that invalidate the current plan should be documented and the plan adjusted; if they create uncertainty that prevents safe continuation, treat that as a blocker.

## 6. Resumability requirement

At any normal interruption point, the repository should make it possible to determine, without relying on chat history:
- what task is being performed;
- what the overall slice plan is;
- which slices are complete;
- which slice is active;
- what has already been discovered or changed in that slice;
- what verification has or has not succeeded;
- whether the current slice is blocked;
- what action should be taken next.

Documentation is therefore part of the work itself, not an end-of-task cleanup step.

## 7. Verification and commits

Tests, consistency checks, source verification, or other validation appropriate to a slice should be performed before declaring it complete. The slice report should state what was verified and any remaining caveats.

Commits should correspond to meaningful successful checkpoints. A commit message should make the completed slice or achieved outcome identifiable when practical.

Unless explicitly instructed otherwise, do not mix unrelated work into a slice checkpoint.

## 8. Research-specific application

For reverse engineering and analytical work, distinguish clearly between:
- verified current-build behavior;
- evidence-supported inference;
- provisional model assumptions;
- experimental/simulation results;
- unresolved questions.

When new evidence invalidates a previous model assumption, preserve that correction in the active-slice report and update the durable mechanics/model documentation at the appropriate successful checkpoint.
