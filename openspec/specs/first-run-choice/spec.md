# First-run choice

## Requirements

### Requirement: Choose how to start an uninitialized commerce

When no local data file exists, the app MUST offer a choice between sample data and an empty commerce. The app MUST save the choice and MUST NOT offer this initial setup again after a successful save.

#### Scenario: Start with examples

- **WHEN** the user chooses sample data
- **THEN** the app MUST save the sample catalogue and example sales locally
- **AND** it MUST open the normal app shell

#### Scenario: Start empty

- **WHEN** the user chooses an empty commerce
- **THEN** the app MUST save an empty catalogue, client list, supplier list, sale list, and debt list
- **AND** it MUST open the normal app shell

#### Scenario: Existing local data

- **WHEN** a local data file already exists and is valid
- **THEN** the app MUST load it and skip first-run setup

- **WHEN** a local data file is invalid or uses an unsupported version
- **THEN** the app MUST preserve the file and report a load error
