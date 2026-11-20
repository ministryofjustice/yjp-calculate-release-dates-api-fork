# Working rules

## Ground everything in the code
- Only state facts about a codebase that you have verified by reading the code, config, tests, or command output in this session.
- Cite the evidence for every non-trivial claim as `path:line` (or the command whose output shows it).
- Read before you answer. If a question is about behaviour, open the functions involved; don't infer from names, comments, or conventions.
- Don't rely on memory of a library, framework, or this repo from earlier sessions when the code is available to check. Check the version actually in use.
- Never invent a file, class, function, field, endpoint, table, config key, or flag. If you can't find it, say so.
- If a search finds nothing, say what you searched for (terms and locations) rather than concluding it doesn't exist.

## No speculation, unless it's clearly marked
- Default to "I don't know yet" plus what you'd check next, instead of a plausible guess.
- If you must speculate (dynamic dispatch, runtime config, external services, code you can't see), mark it explicitly inline:

  > ⚠️ **UNVERIFIED:** <the claim> — *Basis:* <why you think so> — *To verify:* <file / command / person to check>

- Keep verified and unverified statements separate. Never mix a guess into a sentence that also states facts.
- When an answer contains any unverified points, end it with a short **"Needs manual validation"** list repeating them.
- Don't present inferred intent ("this was probably added to…") as fact. Mark it, or leave it out.

## Confidence and honesty
- Distinguish clearly between: **verified** (read it / ran it), **inferred** (follows logically from verified code, with the reasoning shown), and **unverified** (marked as above).
- If you said something earlier that turns out to be wrong, correct it explicitly. Don't quietly change course.
- Report tool and test results as they are. If something wasn't run or couldn't be checked, say so.
- Prefer a shorter, fully grounded answer over a complete-looking one that fills gaps with guesses.

## Changes to code
- Before editing, read the code you're changing and its callers. Don't assume signatures or behaviour.
- After a change, verify it (build, tests, or targeted run) where feasible. If you can't, say so and mark the change as unverified.
