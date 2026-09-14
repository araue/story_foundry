# Phase 8: Chapter Writing and Edition

## Purpose and priority

Turn one approved chapter brief into clear, consequential prose. Do not redesign
the chapter or add an unapproved premise. Prioritize, in order: reader clarity,
present stakes, fully developed characters and consequences, then rhythm and
atmosphere.

Read this file, the current brief, relevant cast and arc files, world files, and
the necessary Phase 1 analysis before drafting or substantially revising.

## Reader orientation

Planning files tell the writer what is true; they tell the reader nothing. Near
each scene's beginning establish the place and relevant layout, viewpoint,
participants and roles, current event, viewpoint objective, immediate pressure,
and its connection to the preceding event. Make shifts in time, place,
participants, and causal situation explicit.

Before relying on a new person, practice, place, technology, relationship, or
term, let the reader encounter it, understand its immediate function and stakes,
receive necessary name and context, see a second dimension or consequence, and
then see it affect a choice. A reader should never need a dossier to understand
the literal event.

## Causality, viewpoint, and prose

Preserve the middle of important chains:

```text
evidence → interpretation → choice → action → consequence
```

Give characters room to register, test, dispute, and respond to important
discoveries or decisions. Use the assigned viewpoint; distinguish observation,
memory, inference, suspicion, and knowledge. Give dialogue a clear proposition
and a credible reason to be spoken.

Use concrete nouns and active verbs, clear referents, coherent paragraphs, and
precise imagery. Do not imitate an identifiable author's sentence-level style.
Mystery may concern a genuinely unknown cause, motive, identity, or future; it
must not come from vague pronouns, missing scene orientation, or withheld facts
the viewpoint would naturally use.

Ground abstract political, ecological, religious, technical, or philosophical
ideas in people making choices under material dependencies and costs. Establish
positions, hazards, goals, and constraints before action; give aftermath more
space than spectacle where consequence is the chapter's work.

## Required revision passes

Complete all six passes before presenting a draft or substantial revision:

1. **Literal clarity and orientation:** location, participants, chronology,
   referents, actions, and causal links are unambiguous.
2. **Reader knowledge and explanation:** new elements receive function and
   context before consequential use.
3. **Planning-language removal:** replace project shorthand with observable
   behavior, ordinary meaning, human need, risk, and decision.
4. **Depth and pacing:** restore missing reasoning, response, transition, and
   aftermath without decorative padding.
5. **Viewpoint, dialogue, and voice:** preserve attribution, distinct goals,
   credible disagreement, and original expression.
6. **Continuity and consequence:** check source constraints, assumptions,
   outline, brief, cast, arcs, world files, maps, and reviewed prose.

## Final reader test

A reader using only the manuscript should be able to explain where the scene
occurs, who is present, what happens, what the viewpoint wants, what prevents
it, what is new and why it matters, what is observed or unknown, why decisions
follow, and what changes next.

After all chapters are accepted, perform a manuscript-wide revision for repeated
abstraction, unclear terminology, cumulative exposition, voice drift, thematic
overstatement, rhythm, and emotional continuity. Return to the governing phase
if this exposes an architecture or world gap.

## Review and EPUB workflow

Maintain the chapter-brief and manuscript indexes as state changes, and update
`status.md` when the high-level review gate changes. Do not draft the next
chapter while the current one awaits review unless the editor directs otherwise.

Rebuild the EPUB after changes to a numbered chapter, edition notice, metadata,
stylesheet, or map:

```sh
python3 tool.py build-epub
```

The build may include only the static notice, optional map, and numbered chapters
in numerical order. `build_epub()` must call `validate_epub()`. The stylesheet
must never force a background or white page color. Report `dist/project.epub`.
