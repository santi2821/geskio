# Product Data Integrity Specification

## Requirements

### Requirement: Product values are valid at the domain boundary

The system MUST reject a product with a blank name, non-finite or negative cost/price, or negative/non-integer stock/minimum, regardless of which screen or caller requests the create or update. The product screen MUST show the reason next to the active workflow and preserve the user's values for correction.

#### Scenario: Create product with negative price

- GIVEN a product form with a name, cost, stock and minimum
- WHEN the price is negative
- THEN the product is not added and the user sees how to correct the price

#### Scenario: Update product with invalid stock

- GIVEN an existing product
- WHEN an update attempts to set stock to a negative or fractional value
- THEN the existing product remains unchanged and the update returns a clear validation error

#### Scenario: Reject non-finite amount

- GIVEN a create or update request with NaN or infinity as cost/price
- WHEN the domain validates the product
- THEN the product is rejected without changing the catalog

#### Scenario: Allow a below-cost price with a warning

- GIVEN a valid product whose sale price is below its cost
- WHEN the product is saved
- THEN it can be saved and the UI warns about the resulting negative margin
