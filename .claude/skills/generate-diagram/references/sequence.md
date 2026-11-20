# Sequence diagram

Shows one flow over time: who calls whom, in what order, what comes back, and where it branches.

## How to search

Sequence diagrams follow **calls from a single entry point**, depth-first.

1. **Find where the flow starts.** Turn the user's words into search terms: the feature noun and its synonyms (`cancel`, `cancellation`, `refund`), likely route paths (`/checkout`, `password-reset`), handler or command names, UI event handlers, queue or topic names, and cron job names. Grep for them, then confirm which hit is the real start: an HTTP route, a UI event, a scheduled job, a message consumer or a CLI command.
2. **Check what runs before the handler.** Look at how the router is mounted in the app entry file for middleware, interceptors, guards and decorators (auth, validation, rate limits).
3. **Follow every call.** Read each function on the path and follow each call into the next file until you reach a boundary:
   - the **database** (SQL or ORM calls), labelled with the operation (`SELECT order by id`) rather than the full SQL;
   - an **external system**: a payment provider, SMTP, a third-party HTTP API, a queue or a cache;
   - **library internals** that don't matter here (stop at "verify token").
4. **Watch for:**
   - error branches: early returns, throws, and where they're caught and mapped to responses (`OutOfStockError` → 409);
   - compensating actions: releasing a reservation, refunds, rollbacks;
   - loops and retries;
   - async or fire-and-forget calls that aren't awaited;
   - return values and the final response or status code.
5. If the request covers several distinct flows (e.g. password reset = *request* + *confirm*), cover them all.

## How to draw

- `sequenceDiagram` with `autonumber`, so the numbers match the reference table.
- **Participants** are at class or module level. Make one per class or module that does real work on the path, plus an `actor` for whoever starts the flow and one participant per external system (`Database`, `Stripe`, `SMTP`). You can fold several repositories' queries into one `Database` participant. Order participants by first call so arrows mostly go left to right. Collapse pure pass-through glue: a router that only forwards to the controller becomes the first arrow, `Client->>OrderController: POST /orders/checkout`.
- **Arrows:** `->>` for calls (real method name plus key arguments), `-->>` for returns (what comes back), and `-)` for async or fire-and-forget.
- **Blocks:** `alt`/`else` for branches, `opt` for optional steps, `loop` for loops and retries. Show where each error ends up as a response.
- **Phases:** use `rect rgb(...)` to group and colour phases, and `Note over` only for neutral facts.
- Use aliases for names with dots or spaces: `participant PG as PaymentGateway (Stripe)`.

**Split** when there are more than about 30 numbered arrows, or when the flow has distinct phases (request/confirm, sync/async worker). Each part restarts numbering and starts with a `Note` saying where it picks up.

## Reference table rows

One row per numbered step or range of steps: `| 8–11 | CartRepository.findForUser: SELECT cart + items | src/repositories/cartRepository.ts:3-7 |`.
