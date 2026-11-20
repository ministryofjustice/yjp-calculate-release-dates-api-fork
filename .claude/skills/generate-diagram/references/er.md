# ER diagram

Shows the database: tables or collections, their columns, keys and the relationships between them.

## How to search

ER diagrams read **schema sources**, in this order of trust:

1. **Migrations and DDL.** These are the most authoritative. Look in:
   - `migrations/`, `db/migrate/`, `alembic/versions/`, `prisma/migrations/`, `flyway`/`liquibase` changelogs
   - `schema.sql`, `structure.sql`, `db/schema.rb`
   Replay migrations in order: later ones add, alter and drop.
2. **ORM model definitions:**
   - `schema.prisma`
   - TypeORM/Sequelize/MikroORM entities
   - Django `models.py`, SQLAlchemy models
   - ActiveRecord models (`belongs_to`, `has_many`)
   - JPA `@Entity`, GORM structs, Mongoose schemas
3. **Raw queries**, used only when there is no schema or model. Grep for `CREATE TABLE`, `INSERT INTO`, `SELECT ... FROM`, `UPDATE ... SET` and `JOIN ... ON`. Infer each table's columns from the column lists, and relationships from `JOIN` conditions and `*_id` columns. Mark everything inferred this way: the types are unknown, and nullability and keys are guesses.

For each table, record:
- columns and their types
- primary key (`PK`), foreign keys (`FK`) and unique constraints (`UK`)
- nullability
- the `file:line` of each

For each relationship, record its **cardinality** from the FK and constraints:
- non-null FK → exactly one on the parent side
- nullable FK → zero or one
- unique FK → one-to-one
- join table → many-to-many

If the scope is unclear ("the database"), cover every table. For a big schema, ask or pick the area the user mentioned.

## How to draw

- Use `erDiagram`. Write entity names in UPPER_SNAKE or exactly as in the DB.
- Attributes go one per line: `uuid id PK`, `uuid user_id FK`, `text email UK`. Add a quoted comment for notable defaults or enums: `text status "pending|paid|cancelled"`.
- Relationship lines: `USERS ||--o{ ORDERS : places`. The markers are:
  - `||` exactly one
  - `o|` zero or one
  - `}o` zero or many
  - `}|` one or many
  Use `--` for identifying relationships and `..` for non-identifying ones.
- Represent JSON or array columns as a column (`json items`). Mention in the notes if they hide a relationship, e.g. order items stored as JSON instead of a table.
- When schema sources were missing and you inferred types from queries, write the type as `unknown` rather than inventing one.

**Split** when there are more than about 15 tables. Make one diagram per domain area (auth, orders, inventory), and repeat a shared table like `USERS` with just its PK where it links areas.

## Reference table rows

One row per table: `| ORDERS | id PK, user_id FK→USERS, status, items (json) | migrations/003_orders.sql:1-12 |`. Note which tables were inferred from queries rather than from a schema.
