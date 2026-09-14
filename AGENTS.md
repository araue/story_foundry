# AGENTS.md for a Literary Project

## Mission

Use this repository to develop an original work, a public-domain adaptation, or
a properly licensed narrative project. Treat research as evidence before
interpretation, interpretation before decisions, and decisions before prose.

The purpose is to build a coherent, readable work while keeping source facts,
interpretations, approved speculation, and deliberate unknowns distinguishable.

## Source boundary and rights

Record the permitted source corpus in `README.md` before Phase 1. For protected
material, use only material you may lawfully use and respect every licence or
permission. This template supplies a method, not rights in any source material.

Do not present remembered wording as a quotation. Use edition-and-location
references for source evidence, and verify every quotation against a permitted
edition before recording it.

## Project-wide principles

- Do not invent merely because an idea is interesting. Justify major decisions
  with source evidence or record them as approved assumptions.
- Preserve genuine mysteries. The reader must nevertheless understand the
  literal event, immediate motive, referent, and causal sequence.
- Maintain consistency in character, technology, ecology, religion, politics,
  chronology, geography, and terminology.
- Do not imitate a living or identifiable author's prose. Develop original,
  clear language informed by high-level analysis only.
- Every chapter permanently changes knowledge, judgment, relationship, identity,
  power, material conditions, or future possibility.
- When prose exposes an architectural problem, return to architecture rather
  than repairing it through an unapproved invention.

## Authority order

Resolve conflicts in this order:

1. permitted source material and documented project constraints;
2. explicit editor decisions;
3. approved assumptions;
4. approved architecture and chapter briefs;
5. approved arcs and world documents;
6. active cast dossiers and reviewed manuscript continuity;
7. local drafting choices.

`characters/` records source-grounded character evidence, `arcs/` records story
change, and `cast/` records the stable current drafting state. Lower-authority
documents may consolidate higher-authority decisions but may not override them.

## Phase workflow

| Phase | Work | Instructions |
|---|---|---|
| 1 | Literary analysis | `phase_instructions/phase_01_literary_analysis.md` |
| 2 | Character analysis | `phase_instructions/phase_02_character_analysis.md` |
| 3 | Open questions | `phase_instructions/phase_03_open_questions.md` |
| 4 | Assumptions and approval | `phase_instructions/phase_04_assumptions.md` |
| 5 | Story architecture and chapter briefs | `phase_instructions/phase_05_story_architecture.md` |
| 6 | Character arcs and active cast | `phase_instructions/phase_06_character_arcs_and_cast.md` |
| 7 | Required world building and maps | `phase_instructions/phase_07_world_building.md` |
| 8 | Chapter drafting, revision, and edition | `phase_instructions/phase_08_writing.md` |

At the start of work, read `status.md`, `phase_instructions/README.md`, and the
active phase instruction in full. Consult only the approved documents relevant
to the task. Do not skip phases.

## Approval gates

The editor decides. Present evidence first and a recommendation second, then
stop for approval before choosing a controversial interpretation, assumption,
thematic or ending direction, mystery answer, character turn, political outcome,
or new faction, ability, technology, ecology, or spatial fact.

A local edit may refine wording, scene order, emphasis, motive, and implication
within approved boundaries. It may not silently change an approved event,
revelation, viewpoint, knowledge boundary, identity, outcome, or mystery policy.

## Chapter workflow

- Prepare chapter briefs one at a time in `story/chapter_briefs/`.
- Draft or substantively revise only the current chapter and complete the Phase
  8 revision passes.
- Maintain `story/chapter_briefs/index.md`, `manuscript/index.md`, and
  `status.md` as review state changes.
- Do not begin the next chapter while the current one awaits review unless the
  editor explicitly directs otherwise.
- Rebuild and validate the EPUB after manuscript or edition-input changes.

## Project documentation and reset safety

`README.md` is stable onboarding; `status.md` is mutable project state; and
`manuscript/edition_notice.md` is the static notice placed below the title in
each EPUB. Keep planning and prose in Markdown; use project-local SVG or PNG
only for maps and other visual assets.

Use the dependency-free root utility `tool.py`:

- `reset_project()` / `python3 tool.py reset-project`
- `build_epub()` / `python3 tool.py build-epub`
- `validate_epub()` / `python3 tool.py validate-epub`

`reset_project()` is a dry run unless called with `confirm=True` or
`reset-project --yes`. It preserves Phase 1–3 research by default, removes the
authored Phase 4–8 solution, and returns the project to Phase 4. A confirmed
reset requires the editor's explicit direction after seeing the exact scope.

## Edition boundary

Set the book title in `epub/metadata.yaml`. The generated EPUB is
`dist/project.epub` by default. It may contain only the static notice, optional
map front matter, and numbered manuscript chapters. The stylesheet must never
force a background or white page color.
