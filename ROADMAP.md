# EmberVault Web Roadmap

## Purpose

Publish the reviewed, sanitized EmberVault catalog, research summaries,
knowledge, compatibility records, and community-facing project data.

## Scope

Included: schemas, validation, publication review, static catalog rendering,
and sanitized imports from Control Center.

Excluded: private profiles, save data, logs, private evidence, credentials,
and direct desktop runtime control.

## Dependencies

- EmberVault-Contracts: public record schemas.
- Control Center: sanitized export source.
- Mod Research and module records: reviewed content.

## Milestones

1. Align public schemas with shared Contracts.
2. Validate incoming sanitized snapshots.
3. Preserve capability and verification states.
4. Add reviewed project and research publication workflows.
5. Verify static deployment and privacy boundaries.
6. Add community blueprint and content-library records for reviewed custom
   projects, including previews, tags, authorship, licenses, compatibility,
   evidence state, and version history.
7. Add upload intake for blueprints, editable project files, preview images,
   evidence attachments, and generated package metadata.
8. Validate uploads for file type, size, unsafe paths, malware, required
   metadata, hashes, and supported schema versions before review.
9. Require authorship and license declarations, preserve provenance, and label
   uploads as verified, experimental, research-only, blocked, or unsupported.
10. Add manual and automated review queues with rejection reasons, resubmission,
    moderation history, and explicit publication approval.
11. Publish approved content as downloads or handoff packages only; never
    execute uploaded code, install uploaded mods, or mutate a user's game.
12. Add search, categories, tags, favorites, compatibility filters, and
    separate blueprint, fixture, export, and evidence views.

## Definition of done

- [ ] Public snapshots contain no private workspace data.
- [ ] Incoming records are schema-validated.
- [ ] Publication requires explicit review.
- [ ] Build and compatibility context is preserved.
- [ ] Site verification and deployment checks pass.
- [ ] Upload intake, quarantine, scanning, hashing, and metadata validation
      pass without executing or installing uploaded content.
- [ ] Community publication preserves authorship, license, provenance,
      compatibility, evidence state, and moderation history.
- [ ] Approved downloads are separated from private evidence and runtime
      operations.
- [ ] Changes are committed and pushed.
