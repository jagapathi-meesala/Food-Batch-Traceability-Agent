# Explainability

## Inputs
The agent accepts ingredient-lot records (`lot_id`, `ingredient`, `supplier`, `received_date`, `quantity`), production-batch records (`batch_id`, `product`, `production_date`, `input_lot_ids`, `quantity`), and shipment records (`shipment_id`, `batch_id`, `destination`, `ship_date`, `quantity`).

## Decision
It validates required fields and identifiers, checks duplicate IDs, then builds links only when the supplied references match known lot or batch IDs. It identifies missing or unresolved references and summarizes the known downstream shipments for each production batch.

## Limits
The tool cannot verify physical product identity, prove that all records have been entered, determine contamination, or establish legal compliance. A missing link means the supplied dataset has no matching reference; it does not prove that no real-world relationship exists.

## Tool: validate-batch-record
### Inputs and Data Sources
A supplied batch-traceability dataset containing ingredient lots, production batches, and shipments.
### Decision and Reasoning
Checks required fields, duplicate IDs, and references to known records.
### Outputs and Evidence
Returns validation issues and record counts.
### Limits and Constraints
Does not verify external source systems or physical labels.
### Failure Handling
Malformed sections and unresolved IDs are reported as issues.
### Human Review
Compare flagged records with approved production, receiving, and shipping logs.

## Tool: build-traceability-links
### Inputs and Data Sources
Ingredient lots, production batches, and shipment records with explicit identifiers.
### Decision and Reasoning
Creates incoming-lot-to-production and production-to-shipment links using exact IDs.
### Outputs and Evidence
Returns known relationships and unresolved references.
### Limits and Constraints
No inferred links are created.
### Failure Handling
Missing or unknown IDs are listed for reconciliation.
### Human Review
Confirm traceability with the authoritative ERP or paper records.

## Tool: prepare-recall-summary
### Inputs and Data Sources
The validated traceability graph and a selected production batch ID.
### Decision and Reasoning
Summarizes known ingredient lots and downstream shipments associated with the selected batch.
### Outputs and Evidence
Returns a mock recall-support summary with explicit evidence gaps.
### Limits and Constraints
Does not decide whether a recall is necessary or notify customers.
### Failure Handling
Unknown batch IDs produce a clear not-found result.
### Human Review
Authorized food-safety and regulatory personnel must decide next actions.
