# Paper Tomorrows - project status (handoff)

Last updated: 2026-10-26

## Channel
- English YouTube Shorts channel "Paper Tomorrows" (@papertomorrows), brand channel.
- Series: Never Built / Yesterday's Tomorrow / Abandoned Futures.
- Owner uploads manually (scheduled, 1 short per day, ~06:00 KST). Altered-content disclosure = YES.

## Production system
- Code: this repo. Pipeline: `modal_app/pipeline.py` (runs on Modal), triggered by GitHub Actions
  `.github/workflows/produce-short.yml` when a `specs/*.json` file changes AND its `status` starts with
  `ready`. Nothing is produced without a `ready` status (owner must confirm before spending).
- Keys (GitHub secrets): MODAL_TOKEN_ID, MODAL_TOKEN_SECRET, FAL_KEY, ELEVENLABS_API_KEY.
- Tools: FLUX.2 [pro] images, Kling v3 Pro image-to-video (5 s hook/climax, 3 s others),
  ElevenLabs voice "Brian" (rhythm delivery), Stable Audio 2.5 music/ambience/SFX (shared cache).
- Generated assets are cached in Modal volume `paper-tomorrows-cache`, keyed by prompt.
- Fact checks are recorded in `specs/FACTCHECK_*.md`. Every narration line must be sourced.

## Approved format ("retention" template) - owner loved it
1. Hook-first opening line (most shocking fact), not a date.
2. Open loop early ("Wait until you see...", "It ended... with dynamite").
3. Big number callouts on screen (`callout` field).
4. Every shot moving (no stills), big camera moves + living elements; per-line `ambience` sound;
   vivid grade; quiet softened transition whoosh; NO punch-in zoom on cuts (owner disliked);
   short shake only on the "never built" impact.
5. Loop ending that leads back into the first line.
- Visual style C (cinematic matte painting). Label "AI CONCEPT VISUALIZATION" first 3 s.
- Cost ~US$7.5 per new short (mostly motion clips).

## Done
- 001 mile-high skyscraper: uploaded 2026-10-26 (old format). Early stats: 100+ views, 10+ likes,
  65.2% viewed (vs swiped).
- 002-006 (Never Built) in the new format: delivered to owner's Downloads/PaperTomorrows with
  `PaperTomorrows_upload_guide.txt` (titles, descriptions, tags, first comments).
  Planned upload order: 006, 002, 004, 003, 005 (one per day).

## Owner rules
- Produce at most 2 shorts per day (owner's rule from 2026-10-26). Confirm with owner before each paid run.
- Owner reviews videos before they are saved to the owner's PC.

## Next
- 007-012 (Yesterday's Tomorrow): specs + fact checks written
  (`specs/_build_yesterdays_tomorrow_batch.py`, `specs/FACTCHECK_007-012.md`) in the OLD structure.
  Rewrite them in the retention template (as done for 002-006 in `_build_never_built_batch.py`),
  then get owner confirmation and mark `ready`. Budget ~US$45; owner should top up fal first.
- Track per short: viewed-vs-swiped %, average % viewed, likes; compare 001 (old) vs new format.
