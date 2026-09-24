# Product Entry UI Specification

## Requirements

### Requirement: Keep the inventory list primary and make product creation easy to find

The Stock screen MUST keep search, filters and the product list as its primary content. A clearly labelled create action MUST remain available in the screen header and open a focused form. Cancelling MUST close the form without changing the catalog. A valid save MUST add the product, close the form, refresh the list and show the outcome. Invalid values MUST leave the form open and preserve the user's input.

#### Scenario: Open the new product form

- GIVEN the user is on Stock
- WHEN the user selects "Nuevo producto"
- THEN a focused product form appears without moving the inventory table below a long entry form

Cost and price are required fields. A numeric zero remains valid when explicitly entered; a blank value MUST never be silently converted to zero. Cancelling MUST discard the draft and clear validation feedback before the next opening.

#### Scenario: Cancel product creation

- GIVEN the new product form is open
- WHEN the user selects "Cancelar"
- THEN the form closes, the product list is unchanged, and a later opening starts with a clean form

#### Scenario: Save product

- GIVEN valid values in the new product form
- WHEN the user selects "Guardar producto"
- THEN the product appears in Stock, the form closes and the fields return to their defaults

#### Scenario: Correct invalid product data

- GIVEN one or more invalid values in the form
- WHEN the user attempts to save
- THEN the form stays open, the catalog stays unchanged and a corrective message is shown
- AND the corrective message is visible in the form and reflects the current error after a correction attempt
