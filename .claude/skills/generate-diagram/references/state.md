# State machine diagram

Shows the states one object or entity can be in (an order, a payment, a subscription, a UI component, a connection) and the events or calls that move it between them.

## How to search

State diagrams follow **one state field across the whole codebase**. Every place that writes it is a transition, and every place that checks it is a guard.

1. **Identify the entity and its state field.** If the user names an entity ("order"), find where it's modelled and which field holds its state: `status`, `state`, `phase`, `stage`, boolean flags like `used` or `committed`, or an explicit state-machine library (XState, AASM, django-fsm, Spring Statemachine, `transitions`).
2. **Find all possible values.** Look in:
   - enums and union types (`'pending' | 'paid' | ...`)
   - constants, DB check constraints and enum columns in migrations
   - string literals assigned to the field
   Grep for each literal as well, because some values only appear in one place.
3. **Find every write to the field.** These are the transitions. Search for:
   - assignments and `update...status` / `setStatus` calls
   - SQL `UPDATE ... SET status`
   - ORM `.update({status})`
   - `INSERT`s with an initial status, which give the initial state
   For each write, record:
   - the **trigger**: which endpoint, method, job, webhook or event causes it;
   - the **from** state(s): whatever is guaranteed when that code runs, often implied by the guards;
   - the **to** state.
4. **Find guards.** These are the checks that allow or block a transition (`if (order.status === "shipped") throw ...`). They become guard labels or forbidden transitions.
5. **Look for writers outside the main code:** admin scripts, webhooks, cron jobs, DB triggers. If a value appears in the type but nothing in the code ever writes it (e.g. `shipped`), still draw the state, but mark the transition into it as "not found in this repo" and mention it in the notes.

## How to draw

- Use `stateDiagram-v2`. Put `[*] --> initial` for the creation state and `final --> [*]` for terminal states.
- Label transitions `event / trigger [guard]`, e.g. `paid --> cancelled : POST /orders/:id/cancel [not shipped]`.
- Use composite states (`state Active { ... }`) for nested lifecycles, and `<<choice>>` for branching on a condition.
- Use `note right of State` only for neutral facts, e.g. "refund issued on entry".
- A `classDef` can colour terminal or error states.

**Split** when there are more than about 15 states, or several independent entities. Make one diagram per entity, or one per composite sub-machine.

## Reference table rows

One row per transition: `| paid → cancelled | CancellationService.cancel, guarded by status not shipped/cancelled | src/services/cancellationService.ts:17-29 |`. Also list where the set of states is defined.
