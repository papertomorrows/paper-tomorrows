# Paper Tomorrows - project status (handoff)

Last updated: 2026-10-27

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
6. HOOK RULES (lesson from data, 2026-10-27): 001 "One mile." + looking up a cloud-piercing tower = 65%
   viewed-vs-swiped; 006 long first sentence ("A sphere as big as the one in Las Vegas... drawn in 1784.")
   + plain stone ball = 37%. So: first line 2-4 words, the payoff word first; first shot must show scale /
   shock instantly (tiny people, something filling the frame, looking up/down); no knowledge needed to get it.
- Visual style C (cinematic matte painting). Label "AI CONCEPT VISUALIZATION" first 3 s.
- Cost ~US$7.5 per new short (mostly motion clips).

## Done
- 001 mile-high skyscraper: uploaded 2026-10-26 (old format). Early stats: 100+ views, 10+ likes,
  65.2% viewed (vs swiped).
- 002-006 (Never Built) in the new format: delivered to owner's Downloads/PaperTomorrows with
  `PaperTomorrows_upload_guide.txt` (titles, descriptions, tags, first comments).
  Planned upload order: 006, 002, 004, 003, 005 (one per day).

## HOUSE STYLE (owner approved 007 v7 on 2026-10-27: "make every video like this")
Reference: `specs/007_hindenburg_host.json` (v7) + `outputs/shorts/007_hindenburg_host/`.
1. First frame = the most shocking moment (flash-forward to the climax) + impact sound; first line 3-5
   words with the key word first ("This ship burns tonight.").
2. A real STORY, not a list of facts: recurring host character (same face: curly hair, round glasses,
   green rain jacket; keep as-is, not "super handsome") who has a goal, tries, fails, escalates, acts.
   History facts stay true and sourced; the host's actions are labelled as dramatization in the description.
3. Escalation all the way: countdown callouts that speed up (3:00:00 ... 0:00:05), rising heartbeat bed
   (`heartbeat_lines`), riser before the climax.
4. Pace: a new picture every ~1-1.5 s in the second half; no shot over ~2.5 s unless it is the climax.
5. End right after the climax (no epilogue, no "where next?" in the video; ask it in the pinned comment).
   The cut back to the first frame makes the loop.
6. Shots: any shot where a person DOES something -> Kling v3 Pro (3 s). Cheap model (Hailuo 2.3 Fast) only
   for camera/smoke/light/landscape moves. No odd isolated close-ups (e.g. just a cigar). Host's
   expression must match the line (never looks like joking in a serious beat).
7. Never reuse the same image or clip twice in one short. Narration speed max 1.10 (1.15 = robotic).
8. ~34-40 s total, ~20 shots. Expected cost ~US$5-6 per short once the script is right.
9. Workflow: script -> cheap still preview (~$0.5-1) -> owner OK -> full production. Quote cost and get
   permission before every paid run.

## Lessons from 008 (Titanic, Time Travel #2)
- Host voice is now Chris (iP95p4xoKVk53GoZ742B, eleven_multilingual_v2, speed 1.05) with `voice_fx: vlog`.
- Talking scenes: Kling v3 Pro motion clip + lip sync (`talk_motion`) looks more natural than the photo
  avatar. Keep the face roughly frontal WHILE speaking (head turns break lip sync); optional `resync`
  (Sync lipsync-2, $3/min) for the most visible frontal shots.
- Talking clips are keyed on the WHOLE narration: any text or voice change re-generates every talking
  scene (~$0.5 each). Lock the script before making talking scenes.
- Story that worked best on preview: dramatic irony (viewer knows, host doesn't), fun first half, turn,
  tragedy, meaningful ending (no "I survived while others died").
- Always quote the cost and get an explicit yes before each paid run, even after the owner picks an option.

## Owner rules
- NEVER start any video production (never set a spec to `ready`, never run the pipeline) without asking
  the owner first and getting explicit permission for that specific run. No exceptions.
- Produce at most 2 shorts per day (owner's rule from 2026-10-26).
- Owner reviews videos before they are saved to the owner's PC.

## Next
- 007-012 (Yesterday's Tomorrow): specs + fact checks written
  (`specs/_build_yesterdays_tomorrow_batch.py`, `specs/FACTCHECK_007-012.md`) in the OLD structure.
  Rewrite them in the retention template (as done for 002-006 in `_build_never_built_batch.py`),
  then get owner confirmation and mark `ready`. Budget ~US$45; owner should top up fal first.
- Track per short: viewed-vs-swiped %, average % viewed, likes; compare 001 (old) vs new format.
- COST TEST (next session, needs owner permission + quoted cost first): keep EVERY shot moving (owner says
  fewer moving shots = boring). Use the premium model (Kling v3 Pro) only for hook + climax shots and a
  cheaper image-to-video model on fal for the other shots. Render the same short in both versions and
  show them side by side so the owner can judge. Goal: ~US$4-5 per short.
- Second channel research (next session): check YouTube/TikTok directly for channels doing
  "1990s TV news / sports broadcast format + weird true history stories". Owner wants a fresh topic with
  dopamine-heavy editing.
- TikTok-specific channel: later, after Paper Tomorrows data. First confirm whether South Korea is
  eligible for the TikTok Creator Rewards Program (needs 1 min+ videos, 10k followers, 100k views/30 days).
- Owner will cross-post the same shorts to Instagram Reels, Threads and TikTok (AI label on).

## PYOG bilingual plan (2026-10-29)
- Two separate channels: English = "Play Your Own Game" (existing channel); Korean = new channel, Korean name not decided yet (KR renders use brand_mark=false until then).
- Every episode: Korean version (voice Korean_CalmGentleman, speed 0.92, owner likes it, never change) + English adaptation (pyog/en/*.md, voice English_CaptivatingStoryteller "D", speed 0.95, lang English, spec id pyog_epXXX_en).
- English is rewritten naturally, not literal; stock keywords partly different from KR.
- Chapter title cards: yes for story/info episodes, NO for meditation/affirmation/sleep episodes.
- Cost: EN voice ~$0.1 per 1k chars (~$0.45-0.65/ep), KR re-render with cached voice ~$0.3.
- EP001+EP002 KR final and EN v1 delivered; EP003 on hold (status hold-ep003), needs EN script.
