# Flowchart

Shows the step-by-step logic of one function, process or workflow: actions, decisions and where each path ends. Use it for "how does this decide X", "what are all the paths through Y", or a business workflow, rather than for who-calls-whom (that's a sequence diagram).

## How to search

Flowcharts read **control flow inside the code**. You go deep into one function or process rather than wide across classes.

1. **Find the start.** Find the function, handler, job or process the user names, the same way you'd find a sequence entry point (feature terms, routes, handler names). If the user describes a business workflow ("order fulfilment"), find the orchestrating function or the chain of handlers that implement it.
2. **Read the body line by line.** Note:
   - every condition: `if`/`else`, `switch`/`match`, ternaries, guard clauses and early returns, `try`/`catch`, validation checks;
   - loops (`for`, `while`, retries) and their exit conditions;
   - each terminal outcome: a return value, thrown error, response status or emitted event.
3. **Descend into a called function only when its logic changes the paths.** For example, `inventory.reserve` returning `null` drives the out-of-stock branch, so open it to see *why* it returns null. Otherwise treat the call as a single action box.
4. Record the `file:line` of each decision and terminal.

## How to draw

- Use `flowchart TD` for most logic. Use `LR` for long linear pipelines.
- Shapes:
  - `([Start / End])` stadium for start and end points
  - `[Action]` rectangle for steps
  - `{Decision?}` rhombus for conditions, phrased as a question
  - `[(Database)]` cylinder for data stores touched
  - `[[Subroutine]]` for a call you didn't expand
  - `>Event]` for emitted events
- Label decision edges with the outcome: `-- yes -->`, `-- no -->`, `-- "status != succeeded" -->`.
- Loops and retries are a back-edge to the step that repeats, with the exit condition on the decision.
- End every path at a terminal that states the outcome (`([201 order])`, `([409 out of stock])`).
- Use `subgraph` to group phases. A `classDef` for error terminals (e.g. red fill) and success terminals (green) helps a lot.

**Split** when there are more than about 30 nodes. Pull a sub-process out into its own flowchart and reference it from the main one with a `[[Sub-process name]]` node.

## Reference table rows

One row per decision and terminal: `| D2 "out of stock?" | reserve() returns null when any sku has insufficient qty | src/services/inventoryService.ts:6-9 |`. Give decision nodes short IDs (D1, D2...) so the table can refer to them.
