# Contributing to Ember Vault

Ember Vault is a reviewed public catalog, not a mirror of private development
data. Submit only material that is safe to publish.

## Submission paths

- Mod records belong in `content/mods/`.
- Research summaries belong in `content/research/`.
- Reusable explanations belong in `content/knowledge/`.
- Compatibility evidence belongs in `content/compatibility/`.
- Design proposals must identify themselves as design-only and must not claim
  live in-game behavior without reproducible evidence.

## Required review information

Every research submission should identify the game build, question or
hypothesis, setup, observed result, confidence, reproduction steps, and
whether the result has been independently reproduced. Experimental and
unsupported findings must remain labeled.

Do not submit save files, private profiles, logs containing personal paths,
unpublished evidence, credentials, or generated data from a private workspace.

## Publication gate

Run the catalog validator before opening a pull request:

```text
python tools/verify_catalog.py embervault-catalog.json
```

Public catalog records are accepted only after schema validation, maintainer
review, and confirmation that private data has been removed.
