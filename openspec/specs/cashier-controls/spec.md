# Cashier controls

## Requirements

### Requirement: Prevent overselling from the cart

Caja MUST compare the requested quantity plus any quantity already in the cart with current stock before accepting a product. It MUST keep the final stock check at checkout.

#### Scenario: Cart already contains the available stock

- **WHEN** adding more units would exceed current stock
- **THEN** Caja MUST leave the cart unchanged and explain how many units remain available

### Requirement: Adjust cart quantities

Caja MUST allow the user to add or remove a single unit from a cart line, subject to current stock. The cart MUST continue to offer a way to remove the entire line.

### Requirement: Calculate cash change

For cash payments, Caja MUST accept an amount received and show the change. A blank amount means exact payment. It MUST refuse to charge when a supplied amount is invalid or less than the sale total. Transfer and fiado sales MUST not display cash change.

#### Scenario: Cash received covers the total

- **WHEN** the received amount is greater than or equal to the total
- **THEN** Caja MUST report the calculated change with the completed sale

#### Scenario: Cash received is insufficient

- **WHEN** the received amount is less than the total
- **THEN** Caja MUST leave the sale, stock, and debt data unchanged
