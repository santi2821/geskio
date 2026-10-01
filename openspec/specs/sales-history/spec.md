# Sales history

## Purpose

Let a shop owner review stored sales without changing their financial or inventory records.

## Requirements

### Requirement: Filter saved sales

The app MUST provide a paginated Sales screen with the most recent sale dates first. It MUST filter by today, the last seven calendar days, all dates, payment method, and customer name. The screen MUST show the count and total of all matching sales, even when results span multiple pages.

#### Scenario: No sales match

- **WHEN** the chosen filters return no sale
- **THEN** the screen MUST explain that there are no sales for those filters
- **AND** it MUST keep the total at zero

#### Scenario: Commerce has no sales

- **WHEN** the commerce has no recorded sales
- **THEN** the screen MUST show that no sales have been registered

### Requirement: Inspect saved sale details

Each sale MUST offer its customer or Mostrador label, date, payment method, total, and a read-only detail of its saved products, quantities, unit prices, and subtotals. Details MUST use sale snapshots rather than the current catalogue. Historical records contain a date, not a time of day; the app MUST NOT invent a time.

#### Scenario: Review a historical sale after catalogue edits

- **WHEN** a product is renamed or repriced after the sale
- **THEN** the sale detail MUST still show the name and price captured when the sale was made

### Requirement: Keep history read-only

Filtering, paging, refreshing, or opening a detail MUST NOT mutate sales, stock, or debt balances.
