# Class diagram

Shows the static structure of object-oriented code: classes, interfaces and enums, their attributes and methods, and how they relate.

## How to search

Class diagrams read **declarations across a scope**, not a call path.

1. **Settle the scope.** The scope is a module, package, folder or feature, e.g. "payments", "src/services", or "the classes involved in checkout". If the user names a feature rather than a folder, find its entry point and collect the classes it touches, then diagram those. If they say "the whole project" and it's large, start with the main domain layer and offer the rest.
2. **Find the declarations** in scope. Search for:
   - `class`, `interface`, `abstract class`, `enum` and `type X = {` (TS);
   - `class` and `@dataclass` (Python);
   - `struct` and `interface` (Go);
   - `record` (Java/C#).
   For each one, note:
   - **Attributes:** fields, constructor-injected or initialized members (`private carts = new CartRepository()`), and properties. Include their type and visibility (`+` public, `-` private, `#` protected).
   - **Methods:** their public API, with parameters and return types. Include private methods only when they matter for understanding.
3. **Find the relationships**, and record the evidence line for each:
   - **Inheritance / realization:** `extends`, `implements`, base classes in Python, embedding in Go.
   - **Composition:** the class creates and owns the other (`new X()` in a field or constructor), so the part's lifecycle is bound to the whole.
   - **Aggregation / association:** it holds a reference that it receives from outside (constructor or DI parameters, setters).
   - **Dependency:** it only uses the other type in a method signature or body, as a parameter, return type, thrown error or local.
   - **Multiplicity:** arrays, lists and maps of another type (`items: CartItem[]` → `"1" *-- "*"`).
4. Include data and DTO types and custom errors when they're part of the picture (e.g. `OutOfStockError` thrown by `CheckoutService`). Leave out framework base types unless the user's classes extend them.

## How to draw

- Use `classDiagram`, and `direction LR` or `TB`, whichever reads better.
- Write members as `+checkout(userId, cartId, paymentMethodId) Promise~Order~`. Use `~T~` for generics and `<<interface>>`, `<<abstract>>`, `<<enumeration>>` annotations.
- Relationship arrows:
  - `<|--` inheritance
  - `<|..` realization
  - `*--` composition
  - `o--` aggregation
  - `-->` association
  - `..>` dependency
  Label them when it adds meaning (`: uses`, `: throws`), and add multiplicities in quotes.
- Group related classes with `namespace Services { ... }` when there are several layers.
- Use `classDef` / `cssClass` sparingly to colour layers, e.g. external clients vs domain.

**Split** when there are more than about 15 classes, or when there are clear layers or packages. Make one diagram per layer or package, and show cross-package links as a thin overview diagram of just the class names.

## Reference table rows

One row per class: `| CheckoutService | Orchestrates checkout; composes CartRepository, InventoryService, PaymentGateway | src/services/checkoutService.ts:10 |`. Add relationship evidence where it's not obvious.
