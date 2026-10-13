<p align="center">
  <img src="docs/assets/readme-logo.svg" alt="Tennis tournament mark" width="144" height="144">
</p>

<h1 align="center">Aces &amp; Ale</h1>

<p align="center"><strong>Eight players. Every match. Beyond the court.</strong></p>

Current display wording and assets are recorded in [Brand and Logo](DESIGN.md#brand-and-logo).

> [!NOTE]
> **Project stage: specification.** This repository contains approved launch specifications,44 full requirement records, a decision register, SVG assets and a specification validator. Application code and its dependency/build/test tooling have not been implemented. Documentation does not demonstrate implementation conformance or operational readiness.

## Explore the Specifications

| Document | Owner |
| --- | --- |
| [Requirements](REQUIREMENTS.md) | Product purpose, actors, behavior, business records, acceptance criteria and open product decisions. |
| [Architecture](ARCHITECTURE.md) | Technology choices, approved components, interfaces, data flows and boundary topology. |
| [Security](SECURITY.md) | Security posture, threats, authentication, permissions/disclosure, controls, enforcement and verification. |
| [Design](DESIGN.md) | Brand/assets, approved visual rules, presentation and accessibility. |
| [Agent instructions](AGENTS.md) | Conditional specification loading, authoring and development workflow guidance. |
| [Requirement template](REQUIREMENT_TEMPLATE.md) | Fields for one atomic requirement and its owner references. |
| [Clarification interview checklist](docs/clarification-interview.json) | Closed interview/default-decision register for all 51 audited topics; owner documents remain authoritative. |
| [Original mark](logo.svg) / [README variant](docs/assets/readme-logo.svg) | Asset use is governed by Design. |

This README is an entry point, not a second specification. Follow owner links for resolved scope and required deployment inputs. Setup/build/test/run and deployment guidance is maintained in [AGENTS.md](AGENTS.md#development-workflow).

Run the available documentation checks with `python3 scripts/check_specs.py`. Re-render formal records after catalog changes with `python3 scripts/render_requirements.py`; review owner consistency before committing.
