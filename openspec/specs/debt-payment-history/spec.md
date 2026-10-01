# Debt payment history

## Requirements

### Requirement: Record each payment against a debt

Each newly registered payment against a fiado account MUST retain its amount, calendar date, and method (cash or transfer). The account MUST retain its existing cumulative paid and outstanding totals.

#### Scenario: View account payments

- **WHEN** the user opens an account's payment history
- **THEN** the app MUST list dated payments with amount and method
- **AND** MUST identify any migrated amount whose date and method are unknown

### Requirement: Preserve legacy paid balances

Migration from JSON v1 or v2 MUST preserve the previously paid amount without assigning dates or payment methods that were never recorded. The unknown-history amount MUST be separate from new itemized payments.

### Requirement: Reflect today's collections accurately

The Dashboard MUST report today's direct sales by their recorded method and today's itemized debt collections by their collection method as separate totals. It MUST NOT report either figure as the shop's cash balance.
