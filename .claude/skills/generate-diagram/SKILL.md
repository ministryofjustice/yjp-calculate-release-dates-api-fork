---
name: generate-diagram
description: Read a codebase and draw accurate diagrams of it in Mermaid, rendered to images and saved in the repo under .claude/diagrams. Invoked as /generate-diagram -t TYPE -d DESCRIPTION. Supports sequence diagrams (the default), class diagrams, C4 architecture diagrams, flowcharts, state machine diagrams and ER (database) diagrams, and can list the available diagram types. Use this whenever the user wants to see how some code works or is structured — "diagram the checkout flow", "how does password reset work, draw it", "class diagram of the payments module", "show me the architecture", "what states can an order be in", "ERD of our database", "map the tables", "flowchart of this function", "what diagram types can you make", "/generate-diagram -t er -d user accounts" — even if they don't say "diagram" or "Mermaid".
---

# Generate diagram

The user names some part of their code and a kind of diagram. You read the code and give back a diagram that matches what the code actually does. Accuracy is the whole point. People will trust the diagram, so one that looks tidy but invents a class, drops a table or skips the error branch is worse than none. Everything you draw should be something you saw in the code, and the answer links back to where you saw it.

## Command usage

The user can call this skill as a command:

```
/generate-diagram -t <type> -d <description>
```

For example: `/generate-diagram -t sequence -d Delete a user`, `/generate-diagram -t er -d orders and payments tables`, `/generate-diagram -d password reset`, or `/generate-diagram -l`.

Read the arguments like this:

- **`-t <type>`** (also `--type`) is the diagram type. Accepted values, case-insensitive:
  - `sequence` / `seq`
  - `class`
  - `c4` / `architecture`
  - `flowchart` / `flow`
  - `state` / `state-machine`
  - `er` / `erd`
  - any of the synonyms listed under "Choosing the type"
  If `-t` is missing, use **sequence**. If the value isn't recognized, say so in one line, show the list of types, and stop. Don't guess a type for an unknown value.
- **`-d <description>`** (also `--desc` / `--description`) is the functionality or area to diagram. It's everything after `-d` up to the next flag, with or without quotes (`-d Delete a user` = `-d "Delete a user"`). Treat it as the search subject. For example, "Delete a user" means find the delete-user entry point (a route like `DELETE /users/:id`, a `deleteUser`/`removeUser` method, an admin action), then follow the type's guide.
- **`-l`** (also `--list`, `-t list`, or `-t` with no value) lists the diagram types as described below, without searching any code.
- **Missing `-d`.** If there's no `-d` and no other text, ask what to diagram in one short question. For whole-system types (C4, ER), a missing description means "the whole project", so go ahead.
- **Text without flags** (`/generate-diagram how checkout works`) is fine. Treat it as the description and use the type rules below.
- **Tolerate small slips**, like a colon after the command name (`/generate-diagram: -t ...`), `--t`, or `-type`.

The project is the current working directory's repo unless the user says otherwise.

## Diagram types

| Type | Shows | Mermaid | Guide |
|---|---|---|---|
| **Sequence** (default) | Interactions over time: calls, API requests, messages between objects and services for one flow | `sequenceDiagram` | `references/sequence.md` |
| **Class** | Classes, attributes, methods, and their relationships (inheritance, composition, dependencies) | `classDiagram` | `references/class.md` |
| **C4** | High-level system structure: people, systems, containers/services, components, and how they connect | `C4Context` / `C4Container` / `C4Component` | `references/c4.md` |
| **Flowchart** | Step-by-step logic, workflows and branching decisions in a function or process | `flowchart` | `references/flowchart.md` |
| **State machine** | The states an object/entity can be in, and the events/calls that move it between them | `stateDiagram-v2` | `references/state.md` |
| **ER** | Database tables, columns, keys and relationships | `erDiagram` | `references/er.md` |

**Listing types.** If the user asks which diagrams you can make ("list diagram types", "what styles are there?"), reply with the table above, leaving out the Mermaid and Guide columns. Mention that sequence is the default and give one example request per type. Don't search any code for this.

**Choosing the type.** Use the type the user names. Accept the obvious synonyms: "UML class", "object model" → class; "architecture", "system context", "containers", "component diagram" → C4; "activity diagram", "logic", "decision tree", "workflow" → flowchart; "lifecycle", "statuses", "state transitions" → state; "ERD", "schema", "data model", "tables" → ER; "call flow", "interaction", "request lifecycle" → sequence. If they name no type, make a **sequence diagram**. Say in one line at the top of the answer which type you made, and that the others are available.

The user may ask for more than one type ("class + sequence for checkout"). Then do each one in turn, sharing the code reading between them.

**Before you search, read the guide for the chosen type.** Each type needs different evidence, so you look for different things. A sequence diagram follows calls from one entry point. A class diagram reads type declarations across a module. C4 reads deployment and config files more than functions. An ER diagram reads migrations and models, not services. The guide tells you where to look, what to trace, how to draw it, and when to split.

## Workflow

### 1. Find the project

The code usually lives in a folder on the user's computer: a connected folder reached through the device tools, or the current working directory. If several folders are connected, pick the one that clearly contains the project. Ask only if it's genuinely ambiguous. The **repo root** is the folder holding the VCS root or the top-level manifest (`.git`, `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, ...).

Get oriented before searching. Read the manifest and the top-level layout so you know the language, framework and layering. If you have a shell on the user's machine, search there with `rg`/`grep -rn`. Otherwise stage just the relevant source files and search the copies. Skip `node_modules`, `vendor`, build output and lockfiles.

### 2. Gather evidence (type-specific)

Follow the search strategy in the type's guide. Whatever the type, keep a running list of each element you'll draw with the `file:line` where you saw it. That list becomes the reference table in the answer, and it keeps you honest. If you inferred something but didn't see it, leave it out, or label it as inferred in the notes.

If you can't find what the user named, say what you searched for and what you found nearby, then ask. Don't draw a guess.

### 3. Draw, and split for readability

Write the Mermaid following the type's guide. Readability matters more than putting everything in one picture. When a diagram passes the split threshold in its guide, or has distinct phases or areas, split it into several diagrams. Each one gets its own title and file, and each should make sense on its own. Examples: request vs confirm phases; one class diagram per package; C4 context, then container; ER per domain area. Briefly say how the parts connect.

**Keep diagrams descriptive.** A diagram shows what the code *does*: calls, branches, states, structure. Notes inside a diagram should only state neutral facts that the shapes can't show, such as "not awaited", "retries up to 3 times" or "TTL 30 min". Opinions, risks, bugs and suggestions never go inside the diagram. They go in the **Worth noticing** list at the bottom of the answer.

Colors are fine where they help. Use them to separate phases, external systems or error paths, and keep them consistent within a diagram.

Mermaid pitfalls that break rendering, for every type:
- Use simple IDs and put labels with spaces or punctuation in quotes or aliases.
- Avoid `;`, `#`, `{}` and unbalanced quotes inside labels. Use `<br/>` for line breaks.
- Never use the bare word `end` as a node or participant ID.
- Every block (`alt`, `loop`, `subgraph`, `state X {`, `System_Boundary(...) {`) must be closed.

### 4. Save into the repo, render, and check

Save every diagram in **`<repo-root>/.claude/diagrams/`**, creating `.claude/` and `.claude/diagrams/` if they don't exist. `.claude/` may already hold Claude settings; add only the `diagrams/` folder and never touch anything else in it. Don't write anywhere else in the repo, and never modify source files.

Name files **`<what>_<when>`**:
- `<what>` is a lowercase, hyphenated subject plus the type, e.g. `checkout-sequence`, `payments-class`, `shop-c4-container`, `order-state`, `database-er`. When a diagram is split, add the part: `password-reset-sequence-1-request`, `password-reset-sequence-2-confirm`.
- `<when>` is the local date and time it was generated, `YYYY-MM-DD_HHMM` (`date +%Y-%m-%d_%H%M`). Use the same timestamp for every file from one request so they group together.

**Only two kinds of file are kept: `.png` (one per diagram) and `.md` (one per request).** Don't leave `.mmd` or `.svg` files in the folder. The Mermaid source lives in the `.md`.

For each diagram, write a temporary `<what>_<when>.mmd`, then render it with the bundled script. The script also checks the syntax:

```bash
python3 <skill-dir>/scripts/render_mermaid.py .claude/diagrams/<what>_<when>.mmd
```

This writes `<what>_<when>.png` next to the `.mmd` using mermaid-cli (`mmdc`, or `npx @mermaid-js/mermaid-cli`), then deletes the `.mmd`. If rendering fails, the `.mmd` is kept: read the error, fix the Mermaid and render again. If mermaid-cli isn't available, the script writes a self-contained `.html` that renders in a browser instead of a PNG, and says so. Tell the user, because then there's no PNG. Never hand over a diagram you haven't seen render. Open the PNG and check that it's legible: nothing overlapping, and not absurdly wide. If it's cramped, split it further or change the direction (`LR` ↔ `TD`).

Also write one companion doc per request, `<subject>-<type>_<when>.md`, containing the full answer (step 5) with each diagram in a ```mermaid block. GitHub and most editors render those blocks, so the doc reads well straight from the repo.

If you can't write to the user's machine (no shell or write-back tool), produce the same files, send them to the user, and tell them which folder they're meant for.

### 5. Answer format

Keep it compact and in this order:

1. **One line** naming the diagram type (and "default" if you chose it), plus one or two sentences summarizing what the diagram shows.
2. **The diagram(s).** Show each rendered image (send the PNG, or render it inline if the interface supports that) with its Mermaid source in a ```mermaid block. If there are several parts, give each a short heading.
3. **Reference table** mapping diagram elements to code. The guide says what the rows are: numbered steps for sequence, classes for class, tables for ER, and so on.
   | # / Element | What | Location |
   |---|---|---|
4. **Files saved:** the paths in `.claude/diagrams/`.
5. **Worth noticing**, at the very bottom, as a separate list, and only if the reading surfaced something real. Examples: an un-awaited call that fails silently, a missing rollback, a swallowed error, a state with no exit, a foreign key with no index, a circular dependency. Don't pad it, and don't repeat these points inside the diagram. Also mention here, in one line, anything you couldn't resolve (dynamic dispatch, config-driven wiring, a schema you couldn't see).
