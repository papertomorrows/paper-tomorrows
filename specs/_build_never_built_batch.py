"""Builds spec files 002-006 (Never Built series). Run: python3 specs/_build_never_built_batch.py"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
KEEP = "The architecture stays rigid and unchanged."
SFX = {"riser_into_lines": [], "impact_on_lines": []}


def shot(prompt, move="push_in", motion=None):
    d = {"prompt": prompt, "move": move}
    if motion:
        d["motion"] = motion
    return d


def metadata(num, name, titles, desc, sources, tags):
    lines = [f"# Short #{num} - {name}", "", "## Title options (1 = recommended)"]
    lines += [f"{i}. {t}" for i, t in enumerate(titles, 1)]
    lines += ["", "## Description", desc.strip(), "",
              "Visuals are AI-generated concept art, not photographs or plans of a real structure.",
              "", "Sources:"] + [f"- {s}" for s in sources]
    lines += ["", " ".join(tags), "", "## Upload checklist",
              "- Altered or synthetic content disclosure: YES (realistic AI-generated scenes)",
              "- Made for kids: No", "- Category: Education, language: English"]
    return "\n".join(lines) + "\n"


SPECS = []

# ------------------------------------------------------------------ 002 Atlantropa
SPECS.append({
    "id": "002_atlantropa",
    "seed_base": 1928,
    "lines": [
        {"text": "In the 1920s, a German architect wanted to drain part of the Mediterranean Sea.",
         "shots": [shot("High aerial view of a rocky Mediterranean coastline at golden hour where the "
                        "sea has dropped far below the old shoreline, exposing wet pale cliffs and an "
                        "old harbour standing high and dry above the water.", "push_in",
                        "The sea level visibly drops, water draining down the exposed cliffs and "
                        "pulling away from the stranded harbour, camera slowly descends. " + KEEP)]},
        {"text": "One dam. Across the Strait of Gibraltar. Thirty-five kilometres long.",
         "shots": [shot("A colossal concrete dam stretching across the Strait of Gibraltar from Europe "
                        "to Africa, huge Atlantic waves breaking against its outer wall, the Rock of "
                        "Gibraltar on one side, wide aerial view at dusk.", "pan_up",
                        "Camera glides fast along the top of the endless dam, Atlantic waves "
                        "crashing and spraying against the wall. " + KEEP),
                   shot("Close view of the towering face of a gigantic 1930s-style concrete dam "
                        "with art deco details, tiny figures of workers on top for scale, sea spray.",
                        "pan_up")]},
        {"text": "Close it... and the sea would slowly sink.",
         "shots": [shot("Enormous steel sluice gates in a giant dam slowly closing, water churning "
                        "below, dramatic low angle, 1930s industrial design.", "push_in"),
                   shot("Fishing boats resting on mud in a Mediterranean harbour as the water has "
                        "retreated far out, old stone town behind, hazy sunlight.", "pull_out")]},
        {"text": "Up to two hundred metres lower.",
         "shots": [shot("Looking down a tall coastal cliff with a pale band marking the old sea "
                        "level high above, the new sea far below, tiny ships for scale.", "pan_down",
                        "Camera tilts slowly down the cliff face from the old waterline to the "
                        "sea far below, gulls wheeling. The cliffs stay rigid and unchanged.")]},
        {"text": "More than six hundred thousand square kilometres of brand-new land.",
         "shots": [shot("Vast new farmland and young towns spreading across a former seabed, "
                        "irrigation canals glinting, the shrunken blue sea on the horizon, aerial.",
                        "pull_out"),
                   shot("A new 1930s-style city with white modernist buildings built on land that "
                        "was once the sea floor, old coastal cliffs rising behind it.", "push_in")]},
        {"text": "And power stations... for all of Europe and Africa.",
         "shots": [shot("A giant hydroelectric power station at the foot of a colossal dam at night, "
                        "water thundering out of spillways, lights glowing.", "push_in",
                        "Water thunders out of the spillways in great white plumes, mist rising, "
                        "lights glowing. " + KEEP),
                   shot("Rows of tall electricity pylons marching across a newly dried plain "
                        "toward distant cities at dusk.", "pan_up")]},
        {"text": "It was never built.",
         "shots": [shot("Calm present-day Strait of Gibraltar at dusk, open water between two "
                        "coastlines, a single ferry, no dam, soft haze.", "pull_out")]},
        {"text": "But imagine, for a moment... that it was.",
         "shots": [shot("Present-day aerial view over the Strait of Gibraltar with a colossal dam "
                        "joining Europe and Africa, the Atlantic high on the left, the Mediterranean "
                        "visibly far lower on the right, modern cities glowing along the new "
                        "coastline at dusk.", "push_in",
                        "Slow majestic flight over the dam toward the lowered Mediterranean, "
                        "city lights twinkling, waves rolling against the Atlantic side. " + KEEP)]},
        {"text": "The coastline of southern Europe... would be unrecognisable.",
         "shots": [shot("A satellite-style view of southern Europe at night where the "
                        "Mediterranean has shrunk and new land glows with city lights along a "
                        "redrawn coastline.", "pull_out"),
                   shot("A historic Mediterranean port city now standing far inland, a long "
                        "canal leading to the distant sea, warm evening light.", "push_in")]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "002", "Atlantropa: The Plan to Drain the Mediterranean",
        ["In the 1920s, Someone Planned to Drain the Mediterranean",
         "The Dam That Would Have Shrunk the Mediterranean Sea",
         "One Dam Would Have Lowered the Mediterranean by 200 Metres"],
        "A dam across the Strait of Gibraltar. A sea up to 200 metres lower. More than 600,000 "
        "square kilometres of new land.\n\nIn the late 1920s, German architect Herman Sörgel "
        "began promoting Atlantropa: a plan to dam the Strait of Gibraltar and partly drain the "
        "Mediterranean Sea (about 100 metres in the west, 200 in the east), with hydroelectric "
        "power for Europe and Africa. It was never built. This is a concept visualization of "
        "what might have been.",
        ["Cabinet Magazine: \"Herman Sörgel's plan to drain the Mediterranean\"",
         "Gizmodo: \"The insane 1920s plan to dam the Mediterranean\""],
        ["#neverbuilt", "#atlantropa", "#mediterranean", "#megaprojects", "#history"]),
})

# ------------------------------------------------------------------ 003 Shimizu pyramid
SPECS.append({
    "id": "003_shimizu_pyramid",
    "seed_base": 2110,
    "lines": [
        {"text": "Japan designed a pyramid... about fourteen times taller than Giza.",
         "shots": [shot("A colossal glass and steel lattice pyramid rising out of Tokyo Bay, so tall "
                        "its peak pierces the clouds, tiny ships on the water at its base, dawn light.",
                        "pan_up",
                        "Camera rises fast up the face of the colossal lattice pyramid from the "
                        "water toward its cloud-wrapped peak. " + KEEP)]},
        {"text": "Two thousand metres high. Rising out of Tokyo Bay.",
         "shots": [shot("The Tokyo skyline seen across the bay, dwarfed by a gigantic open-frame "
                        "pyramid on the water, its upper half above the clouds, golden hour.",
                        "pull_out"),
                   shot("Looking straight up one edge of a vast pyramid made of a geometric steel "
                        "lattice, the edges converging far into the sky.", "pan_up")]},
        {"text": "A single structure... for one million people.",
         "shots": [shot("Inside a gigantic pyramid made of open lattice, a vast airy space filled "
                        "with suspended towers, gardens and light, small crowds far below.",
                        "push_in",
                        "Slow drifting camera through the vast interior of the lattice pyramid, "
                        "light beams shifting, tiny transit pods gliding along the struts. " + KEEP)]},
        {"text": "Thirty-storey skyscrapers... hanging inside the frame.",
         "shots": [shot("Several 30-storey skyscrapers suspended by cables inside a giant pyramid "
                        "lattice, hanging in mid-air with lit windows, people on sky bridges.",
                        "pan_down"),
                   shot("Close-up of thick dark cables holding a skyscraper in the air inside a "
                        "geometric frame, clouds visible through the lattice.", "pan_up")]},
        {"text": "Moving walkways. Inclined elevators. Robot pods running through the struts.",
         "shots": [shot("Futuristic accelerating walkways and inclined glass elevators inside a "
                        "colossal lattice structure, people travelling, warm light.", "push_in"),
                   shot("Small automated transit pods racing along the inside of giant steel "
                        "struts in a pyramid city, motion blur, bright interior.", "pan_up",
                        "Transit pods race along the struts, light streaks behind them, camera "
                        "follows smoothly. " + KEEP)]},
        {"text": "Building it would take eighty years... and materials still being invented.",
         "shots": [shot("Robotic construction arms assembling a gigantic lattice of dark carbon "
                        "struts over the sea, a half-finished pyramid frame, overcast sky.", "pull_out"),
                   shot("Macro view of a glowing black carbon nanotube cable, futuristic "
                        "laboratory light, shallow depth of field.", "push_in")]},
        {"text": "It was never built.",
         "shots": [shot("Present-day Tokyo Bay at dusk, calm water, distant city lights, empty "
                        "horizon where nothing rises, soft fog.", "pull_out")]},
        {"text": "But imagine, for a moment... that it was.",
         "shots": [shot("Present-day Tokyo at night seen from the bay, a colossal glowing lattice "
                        "pyramid two kilometres tall rising from the water, its upper half above "
                        "the clouds, millions of lights inside.", "push_in",
                        "Slow upward crane shot rising along the glowing pyramid, clouds "
                        "drifting around its middle, lights twinkling inside. " + KEEP)]},
        {"text": "It would be more than twice as tall as anything on Earth.",
         "shots": [shot("A colossal see-through pyramid made of an open steel lattice of geometric struts, "
                        "not stone, standing in Tokyo Bay beside a modern supertall skyscraper that "
                        "reaches less than half its height, dramatic dusk sky.", "pull_out"),
                   shot("View from inside the top of a two-kilometre open steel lattice pyramid, looking "
                        "out through the geometric struts over a sea of clouds at sunrise, Mount Fuji "
                        "in the distance. Steel framework, not stone.", "push_in")]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "003", "The Shimizu Mega-City Pyramid",
        ["Japan Designed a Pyramid 14 Times Taller Than Giza",
         "A City for a Million People Inside One Pyramid",
         "The 2-Kilometre Pyramid Japan Never Built"],
        "Two kilometres high. A million residents. Skyscrapers hanging inside the frame.\n\n"
        "Japan's Shimizu Corporation designed the Mega-City Pyramid for Tokyo Bay: a 2,004-metre "
        "structure with suspended 30-storey towers and transit pods running through its struts. "
        "It needs materials that are still being researched, and it was never built. This is a "
        "concept visualization of what might have been.",
        ["Wikipedia: Shimizu Mega-City Pyramid"],
        ["#neverbuilt", "#tokyo", "#megaprojects", "#futurecity", "#architecture"]),
})

# ------------------------------------------------------------------ 004 Watkin's Tower
SPECS.append({
    "id": "004_watkins_tower",
    "seed_base": 1890,
    "lines": [
        {"text": "In 1890, London wanted to beat the Eiffel Tower.",
         "shots": [shot("A towering Victorian iron lattice tower, taller and broader than the "
                        "Eiffel Tower, rising over green parkland outside London, crowds in "
                        "Victorian dress, dramatic clouds.", "pan_up",
                        "Camera sweeps up the iron lattice of the giant tower toward its summit, "
                        "clouds racing past, flags fluttering. " + KEEP)]},
        {"text": "A railway tycoon planned a tower... forty-six metres taller.",
         "shots": [shot("A Victorian railway station with a steam train arriving, a gigantic iron "
                        "tower under construction visible beyond the platform, steam and smoke.",
                        "push_in",
                        "A steam train pulls in, smoke billowing, the giant tower looming behind. "
                        + KEEP),
                   shot("Two iron towers side by side for comparison at dusk, the left one "
                        "noticeably taller and wider at the base, Victorian style.", "pan_up")]},
        {"text": "A hotel. Theatres. Turkish baths... all in the sky.",
         "shots": [shot("An ornate Victorian theatre and restaurant on an observation deck high "
                        "inside an iron tower, gas lamps, views of the countryside far below.",
                        "pull_out"),
                   shot("A luxurious Victorian Turkish bath with tiled arches and steam, windows "
                        "showing clouds outside, high in a tower.", "push_in")]},
        {"text": "Work began in 1893.",
         "shots": [shot("Victorian workers in caps riveting giant iron girders on a construction "
                        "site, cranes and scaffolding, the base of a huge tower rising.", "pan_up"),
                   shot("The four massive iron legs of an unfinished tower in a muddy field, "
                        "workers and horses below, overcast sky.", "pull_out")]},
        {"text": "But the money ran out... and the ground began to sink.",
         "shots": [shot("Close-up of a cracked concrete foundation under an iron tower leg, "
                        "muddy waterlogged ground, tilted planks, grey light.", "push_in",
                        "Mud slowly oozes into the widening crack, water seeping, a plank tilts. "
                        "The iron stays rigid and unchanged."),
                   shot("An abandoned Victorian construction site with idle cranes and rusting "
                        "girders, rain, empty.", "pull_out")]},
        {"text": "It reached forty-seven metres. Less than one-seventh of the plan.",
         "shots": [shot("A stubby unfinished iron tower base only a few storeys high in an empty "
                        "park, a faint ghostly outline of the full planned tower rising far above "
                        "it into the sky.", "pan_up")]},
        {"text": "So they blew it up.",
         "shots": [shot("A dynamite demolition of a Victorian iron tower base, a burst of smoke "
                        "and dust, iron girders collapsing, sepia tones, early 1900s.", "push_in",
                        "A burst of dust and smoke as the iron structure collapses, debris "
                        "falling, smoke billowing outward.")]},
        {"text": "Today, Wembley Stadium stands on the same spot.",
         "shots": [shot("A modern stadium with a giant white arch at dusk, lit up, crowds "
                        "arriving, wide aerial view.", "pull_out")]},
        {"text": "But imagine, for a moment... that the tower was finished.",
         "shots": [shot("Present-day London skyline at dusk seen from a distance, a colossal "
                        "Victorian iron lattice tower towering over everything near a modern "
                        "stadium, lights glowing on its iron frame.", "push_in",
                        "Slow upward crane shot rising along the giant iron tower, city lights "
                        "twinkling, clouds drifting. " + KEEP),
                   shot("View from the top observation deck of a giant Victorian iron tower over "
                        "modern London at night, glowing city stretching to the horizon.", "pull_out")]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "004", "Watkin's Tower: London's Eiffel Tower",
        ["London Tried to Beat the Eiffel Tower. It Failed.",
         "The Tower That Would Have Been Taller Than the Eiffel Tower",
         "Why Wembley Stadium Sits on a Failed Tower"],
        "Taller than the Eiffel Tower. A hotel, theatres and Turkish baths in the sky.\n\n"
        "In the 1890s, railway entrepreneur Sir Edward Watkin began building a tower at Wembley "
        "Park, planned to rise about 46 metres higher than the Eiffel Tower. The money ran out "
        "and the foundations subsided at 47 metres. The stump was demolished with dynamite in "
        "1904-1907, and Wembley Stadium now stands on the site. This is a concept visualization "
        "of what might have been.",
        ["Wikipedia: Watkin's Tower"],
        ["#neverbuilt", "#london", "#wembley", "#eiffeltower", "#history"]),
})

# ------------------------------------------------------------------ 005 Tatlin's Tower
SPECS.append({
    "id": "005_tatlins_tower",
    "seed_base": 1920,
    "lines": [
        {"text": "In 1920, an artist designed a tower... where the buildings inside would spin.",
         "shots": [shot("A colossal leaning double spiral of dark iron rising into a stormy sky, "
                        "glass buildings glowing inside it, constructivist style, dramatic low angle.",
                        "push_in",
                        "Camera circles and rises around the colossal iron spiral, the glass "
                        "blocks inside slowly rotating, storm clouds moving. " + KEEP)]},
        {"text": "Four hundred metres of iron, glass and steel. Taller than the Eiffel Tower.",
         "shots": [shot("A giant leaning spiral iron tower beside a smaller Eiffel-like lattice "
                        "tower for scale, the spiral much taller, dusk sky.", "pan_up"),
                   shot("Close view of massive riveted iron spiral beams curving upward, "
                        "early 20th century industrial detail, red sunset light.", "pan_up")]},
        {"text": "A giant twin spiral, tilted like the Earth's axis... over the city of Petrograd.",
         "shots": [shot("A colossal leaning iron spiral tower rising over the river and classical "
                        "palaces of 1920s Petrograd, misty morning, ships on the river.", "pull_out",
                        "Slow wide flight across the river toward the giant spiral tower, mist "
                        "drifting, boats moving. " + KEEP)]},
        {"text": "Inside, three glass buildings... stacked on top of each other.",
         "shots": [shot("Inside a giant iron spiral, three huge glass buildings stacked vertically: "
                        "a cube at the bottom, a pyramid in the middle, a cylinder above, glowing.",
                        "pan_up")]},
        {"text": "The bottom one would turn once a year.",
         "shots": [shot("A massive glass cube hall inside an iron frame, a grand assembly room with "
                        "rows of seats, slowly rotating, constructivist design.", "push_in")]},
        {"text": "The middle one... once a month.",
         "shots": [shot("A glass pyramid of offices inside a giant iron spiral, desks and "
                        "typewriters, 1920s workers, light through angled glass.", "push_in")]},
        {"text": "And the top one... once a day.",
         "shots": [shot("A glowing glass cylinder high inside an iron spiral tower, an information "
                        "centre with radio equipment and screens, the city far below.", "push_in",
                        "The glass cylinder turns slowly, light sweeping across it, the city "
                        "far below. " + KEEP)]},
        {"text": "It was never built.",
         "shots": [shot("An empty riverside in Petrograd at dusk, fog over the water, classical "
                        "buildings, nothing towering above the skyline.", "pull_out")]},
        {"text": "But imagine, for a moment... that it was.",
         "shots": [shot("Present-day Saint Petersburg at dusk seen across the river, a colossal "
                        "400-metre leaning iron spiral tower with glowing glass buildings inside, "
                        "towering over the historic skyline.", "push_in",
                        "Slow upward crane shot rising along the iron spiral, the glass blocks "
                        "inside glowing and slowly turning, city lights twinkling. " + KEEP),
                   shot("The glowing spiral tower reflected in a river at night, historic "
                        "palaces along the bank, still water.", "pull_out")]},
    ],
    "sfx": {"riser_into_lines": [7], "impact_on_lines": [7]},
    "metadata": metadata(
        "005", "Tatlin's Tower: The Tower That Spun",
        ["This Tower Was Designed to Spin. Once a Day.",
         "The 400-Metre Spinning Tower That Was Never Built",
         "In 1920, They Designed a Tower With Rotating Buildings Inside"],
        "Four hundred metres of iron and glass. Three buildings inside, each turning at its own "
        "speed: once a year, once a month, once a day.\n\nVladimir Tatlin designed the "
        "Monument to the Third International in 1919-1920 for Petrograd (now Saint Petersburg). "
        "It was never built. This is a concept visualization of what might have been.",
        ["Wikipedia: Tatlin's Tower", "Sainsbury Centre: Model of the Monument to the Third International"],
        ["#neverbuilt", "#tatlin", "#constructivism", "#architecture", "#history"]),
})

# ------------------------------------------------------------------ 006 Newton's Cenotaph
SPECS.append({
    "id": "006_newton_cenotaph",
    "seed_base": 1784,
    "lines": [
        {"text": "In 1784, a French architect designed a monument... about the size of the Las Vegas Sphere.",
         "shots": [shot("A colossal smooth stone sphere resting on a tiered circular base ringed "
                        "with tall dark cypress trees, tiny 18th-century figures at its foot, "
                        "dramatic sky.", "pull_out",
                        "Camera pulls back and rises to reveal the full size of the colossal "
                        "sphere, cypress trees swaying, clouds drifting. " + KEEP)]},
        {"text": "A hollow sphere... one hundred and fifty metres across.",
         "shots": [shot("A vast stone sphere seen from below its curve, people in 18th-century "
                        "clothes tiny beside it, cypress trees, morning mist.", "pan_up"),
                   shot("Neoclassical architectural elevation drawing on aged parchment of a giant plain "
                        "smooth sphere resting directly on a low stepped circular base ringed with "
                        "cypress trees, tiny human figures for scale, no other buildings.", "push_in")]},
        {"text": "A memorial for Isaac Newton.",
         "shots": [shot("A single small stone sarcophagus alone on the floor of an immense dark "
                        "spherical hall, a shaft of light falling on it.", "push_in")]},
        {"text": "By day, sunlight through tiny holes...",
         "shots": [shot("Inside a colossal dark stone sphere, hundreds of thin beams of daylight "
                        "shining through tiny holes in the curved ceiling.", "pan_up",
                        "Beams of sunlight slowly shift and shimmer through the tiny holes, dust "
                        "floating in the light. " + KEEP)]},
        {"text": "...would turn it into a sky full of stars.",
         "shots": [shot("The inside of an immense dark dome glittering with thousands of points of "
                        "light like a star-filled night sky, a tiny figure standing below.",
                        "pull_out")]},
        {"text": "At night, a glowing orb would hang inside... like a sun.",
         "shots": [shot("A huge glowing orb suspended in the centre of a vast dark spherical hall, "
                        "lighting the curved stone walls golden, a tiny visitor below.", "push_in",
                        "The glowing orb pulses softly, golden light rippling across the curved "
                        "walls. " + KEEP)]},
        {"text": "It was never built.",
         "shots": [shot("An empty misty field at dawn with a few cypress trees, no monument, "
                        "18th-century countryside, quiet.", "pull_out")]},
        {"text": "Almost two hundred and forty years later... Las Vegas built one almost the same size.",
         "shots": [shot("A giant glowing spherical entertainment venue at night in a desert city, "
                        "its surface lit with colourful light, crowds below, generic modern design.",
                        "pull_out"),
                   shot("An old neoclassical sphere design and a modern glowing sphere side by side "
                        "at dusk, the same size, desert and cypress trees blending.", "push_in")]},
        {"text": "Now imagine standing inside the original.",
         "shots": [shot("Inside a colossal hollow stone sphere: the entire curved interior wall all around "
                        "is pierced by thousands of tiny holes shining like stars, so the visitor "
                        "seems to stand inside the night sky, one tiny lone figure at the bottom "
                        "centre, awe-inspiring scale.", "pan_up",
                        "Slow upward crane from the tiny visitor up into the star-filled curved "
                        "dome, the points of light twinkling and glinting. " + KEEP)]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "006", "Boullée's Cenotaph for Newton",
        ["The Las Vegas Sphere Was Designed in 1784",
         "In 1784, an Architect Designed a Sphere for Isaac Newton",
         "The 150-Metre Sphere That Turned Day Into Night"],
        "A hollow sphere 150 metres across. By day, sunlight through tiny holes turned the inside "
        "into a sky full of stars. By night, a giant glowing orb hung in the centre.\n\nFrench "
        "architect Étienne-Louis Boullée designed this cenotaph for Isaac Newton in 1784. It was "
        "never built. Almost 240 years later, a sphere of nearly the same size opened in Las "
        "Vegas. This is a concept visualization of what might have been.",
        ["Physics World: \"The Las Vegas Sphere and its curious link with Isaac Newton\"",
         "Wikipedia: Étienne-Louis Boullée"],
        ["#neverbuilt", "#isaacnewton", "#lasvegassphere", "#architecture", "#history"]),
})

if __name__ == "__main__":
    import sys
    only = sys.argv[1:]
    for spec in SPECS:
        if only and not any(spec["id"].startswith(o) for o in only):
            continue
        spec = {**spec, "status": "ready-fix"} if only else spec
        path = HERE / f"{spec['id']}.json"
        path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
        n_shots = sum(len(l["shots"]) for l in spec["lines"])
        n_motion = sum(1 for l in spec["lines"] for s in l["shots"] if s.get("motion"))
        words = sum(len(l["text"].split()) for l in spec["lines"])
        print(f"{path.name}: lines={len(spec['lines'])} shots={n_shots} motion={n_motion} words={words}")
