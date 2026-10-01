# Inventory movement history

## Requirements

### Requirement: Record stock changes with a reason

Manual adjustments and stock changes made while editing a product MUST record the date, product name and ID snapshot, quantity before and after, signed quantity change, and a non-empty reason.

### Requirement: Record changes caused by sales

Completed sales and sale reversals MUST record their stock changes as sale or reversal entries with the corresponding sale reference.

### Requirement: Browse stock changes

The Movements screen MUST show newest entries first, support product or reason search, and paginate results. It MUST distinguish adjustment, sale, and reversal entries and show the quantity change and before/after amounts.

### Requirement: Do not invent historical movements

Migration and restore MUST preserve existing product stock without synthesizing movements for old sales or adjustments. The movement log begins when v3 tracking is available; this limit MUST be documented to the user.
