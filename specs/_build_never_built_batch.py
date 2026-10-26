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
         "shots": [shot("Very wide shot from far across Tokyo Bay: a colossal see-through pyramid made of an "
                        "open steel lattice, its peak high above the clouds. At its base stands a modern "
                        "skyscraper that looks tiny next to it, reaching only a small fraction of the "
                        "pyramid's height. Dramatic dusk sky, the whole pyramid visible.", "pull_out"),
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
         "shots": [shot("Victorian workers in caps riveting giant iron girders at ground level, the first "
                        "low stage of a tower only a few storeys high, a wide iron platform on four "
                        "broad legs, nothing built above it yet, wooden scaffolding, overcast sky.",
                        "push_in"),
                   shot("Wide view of a muddy Victorian park with a short unfinished iron structure only "
                        "about fifty metres tall, a flat iron platform on four legs, no tower above "
                        "it, workers and horses below, overcast sky.", "pull_out")]},
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


# ------------------------------------------------------------------ extra 3-second motion shots
STILL = "Buildings and structures stay rigid and unchanged."
MORE_MOTION = {
    ("002_atlantropa", 2, 0): "The huge sluice gates grind slowly shut, water churning and foaming below. " + STILL,
    ("002_atlantropa", 2, 1): "Shallow water slowly retreats across the mud, the beached boats settle and tilt slightly, haze drifts. " + STILL,
    ("002_atlantropa", 4, 0): "Camera glides forward over the new fields, cloud shadows sweep across the land, canals glint. " + STILL,
    ("002_atlantropa", 6, 0): "The ferry moves slowly across the strait, gentle waves roll, mist drifts over the water.",
    ("002_atlantropa", 8, 1): "Small boats move along the long canal toward the distant sea, lights flicker on in the town. " + STILL,
    ("003_shimizu_pyramid", 1, 0): "Clouds drift slowly past the upper half of the pyramid, boats cross the bay, light shifts. " + STILL,
    ("003_shimizu_pyramid", 3, 0): "Tiny people walk across the sky bridges between the hanging towers, light beams shift slowly. " + STILL,
    ("003_shimizu_pyramid", 4, 0): "The walkways move steadily, glass elevators glide up the incline, people ride along. " + STILL,
    ("003_shimizu_pyramid", 5, 0): "Robotic arms swing and lift a dark strut into place, sparks of welding light, sea moving below. " + STILL,
    ("003_shimizu_pyramid", 6, 0): "Fog drifts slowly over the calm water, city lights twinkle on the horizon, small ripples.",
    ("003_shimizu_pyramid", 8, 1): "Camera pushes slowly forward between the struts toward the view, clouds drift below, sunrise glow grows. " + STILL,
    ("004_watkins_tower", 2, 0): "Gas lamps flicker, diners move between the tables, clouds drift far below the windows. " + STILL,
    ("004_watkins_tower", 2, 1): "Steam swirls and rises slowly through the tiled arches, light shimmers on the water. " + STILL,
    ("004_watkins_tower", 3, 0): "Workers swing hammers onto glowing rivets, sparks fly, a crane slowly lifts a girder. " + STILL,
    ("004_watkins_tower", 4, 1): "Rain falls steadily, puddles ripple, a loose tarp flaps in the wind. " + STILL,
    ("004_watkins_tower", 7, 0): "Crowds stream toward the stadium, lights shimmer along the giant arch, camera pulls back slowly. " + STILL,
    ("005_tatlins_tower", 3, 0): "Camera rises slowly past the three glowing glass buildings inside the spiral. " + STILL,
    ("005_tatlins_tower", 4, 0): "The whole glass cube hall slowly rotates, light sliding across the seats. The iron frame stays rigid.",
    ("005_tatlins_tower", 5, 0): "Workers type at their desks as the glass pyramid slowly turns, light angles shifting. The iron frame stays rigid.",
    ("005_tatlins_tower", 8, 1): "Reflections ripple on the river, the glowing tower's lights shimmer, a boat glides past. " + STILL,
    ("006_newton_cenotaph", 1, 0): "Mist drifts around the base, tiny figures walk, camera tilts slowly up the curve of the sphere. " + STILL,
    ("006_newton_cenotaph", 2, 0): "The shaft of light shimmers, dust floats through it, camera pushes slowly toward the tomb. " + STILL,
    ("006_newton_cenotaph", 4, 0): "The points of starlight twinkle across the dome as the camera rises slowly. " + STILL,
    ("006_newton_cenotaph", 7, 0): "Patterns of light ripple across the giant sphere's surface, crowds walk below. " + STILL,
}
for spec in SPECS:
    for (sid, li, si), motion in MORE_MOTION.items():
        if spec["id"] == sid:
            shot_ = spec["lines"][li]["shots"][si]
            assert not shot_.get("motion"), (sid, li, si)
            shot_["motion"] = motion
            shot_["motion_seconds"] = 3



# ------------------------------------------------------------------ dynamic motion (big camera moves)
SHAPE = "Structures keep their shape."
DYNAMIC = {
    "002_atlantropa": {
        (0, 0): "Fast dramatic aerial swoop diving down the cliffs toward the stranded harbour, the sea rushing away from the shore, waves pulling back hard. " + SHAPE,
        (1, 0): "Fast low drone flight racing along the top of the dam just above the water, huge Atlantic waves smashing into the wall and exploding into spray. " + SHAPE,
        (2, 0): "The giant gates slam down and a torrent of water explodes beneath them, the camera pushes in fast through flying spray. " + SHAPE,
        (2, 1): "Camera flies fast and low over the mud between the stranded boats toward the old town, a flock of seagulls bursts into flight. " + SHAPE,
        (3, 0): "Camera plunges fast straight down the cliff face from the old waterline to the sea far below, gulls swirling past the lens. " + SHAPE,
        (4, 0): "Fast low flyover skimming across the new fields, a train races along a track below, cloud shadows sweep quickly across the land. " + SHAPE,
        (5, 0): "Camera rushes toward the roaring spillways, massive white water thundering out, mist billowing over the lens. " + SHAPE,
        (6, 0): "Camera orbits around the lone ferry as it cuts through the waves at dusk, spray and wake churning behind it.",
        (7, 0): "Majestic sweeping flight forward along the dam, steady and smooth but fast, rising slightly to reveal the lowered sea and the glowing new coastline ahead, city lights twinkling. " + SHAPE,
        (8, 1): "Fast flight down the long canal between the buildings toward the distant sea, boats passing quickly beneath. " + SHAPE,
    },
}
for spec in SPECS:
    for (li, si), motion in DYNAMIC.get(spec["id"], {}).items():
        shot_ = spec["lines"][li]["shots"][si]
        assert shot_.get("motion"), (spec["id"], li, si)
        shot_["motion"] = motion



# ------------------------------------------------------------------ retention structure (002 test)
def _restructure_002(spec):
    old = spec["lines"]
    S = lambda li, si: dict(old[li]["shots"][si])          # reuse = cache hit

    def moving(shot_, motion, secs=3):
        shot_ = dict(shot_); shot_["motion"] = motion; shot_["motion_seconds"] = secs
        return shot_

    life = "Structures keep their shape."
    architect = shot("A 1920s architect in a waistcoat leaning over a huge drafting table covered with a "
                     "map of the Mediterranean, a long dam drawn across the Strait of Gibraltar, warm "
                     "lamp light, blueprints and pencils, cinematic.", "push_in")
    spec["lines"] = [
        {"text": "This one dam... would have lowered the entire Mediterranean Sea.",
         "ambience": "Huge ocean waves crashing against a concrete sea wall, strong wind and spray",
         "shots": [S(1, 0), S(0, 0)]},
        {"text": "Wait until you see what Europe would look like today.",
         "ambience": "Deep low cinematic rumble, high wind, distant city hum",
         "shots": [moving(S(8, 0), "Camera rushes down from high above toward the glowing redrawn "
                                   "coastline, city lights flickering below, clouds racing past. " + life)]},
        {"text": "In the 1920s, a German architect proposed it.",
         "ambience": "Quiet 1920s office, pencil scratching on paper, clock ticking, rain on a window",
         "shots": [moving(architect, "The architect's pencil sweeps along the dam line on the map, the "
                                     "lamp flickers, papers stir, the camera pushes in. " + life)]},
        {"text": "A wall across the Strait of Gibraltar. Thirty-five kilometres long.",
         "callout": "35 KM",
         "ambience": "Ocean waves pounding a giant dam, seagulls crying, strong wind",
         "shots": [moving(S(1, 1), "Camera tilts fast up the towering dam face as spray bursts upward, "
                                   "tiny workers walk along the top, gulls wheel past. " + life)]},
        {"text": "Close it... and the sea would sink, up to two hundred metres.",
         "callout": "\u2212200 M",
         "ambience": "Rushing water thundering through giant sluice gates, deep rumble",
         "shots": [S(2, 0), S(3, 0)]},
        {"text": "More than six hundred thousand square kilometres of new land.",
         "callout": "600,000 KM\u00b2",
         "ambience": "Open countryside, birdsong, light wind, distant train",
         "shots": [S(4, 0), moving(S(4, 1), "Camera glides down a busy boulevard of the white 1930s city, "
                                            "cars and pedestrians moving, flags fluttering in the sun. " + life)]},
        {"text": "Power for all of Europe and Africa.",
         "ambience": "Roaring waterfall spillway and deep electrical hum",
         "shots": [S(5, 0), moving(S(5, 1), "Camera races along the line of pylons as pulses of light run "
                                            "through the cables, a train speeds past below at dusk. " + life)]},
        {"text": "It was never built.",
         "ambience": "Calm sea, gentle waves, a distant ship horn",
         "shots": [S(6, 0)]},
        {"text": "But if it had been...",
         "ambience": "Wind over the sea at dusk, distant city hum",
         "shots": [S(7, 0)]},
        {"text": "The coastline of southern Europe would be unrecognisable. All because of one dam.",
         "ambience": "Harbour ambience, water lapping, seagulls, distant church bells",
         "shots": [S(8, 1), moving(S(1, 0), "Slow sweeping pull back revealing the full length of the "
                                            "colossal dam at dusk, waves rolling against it. " + life)]},
    ]
    spec["sfx"] = {"riser_into_lines": [7], "impact_on_lines": [7]}
    spec["settings"] = {"voice_settings": {"stability": 0.35, "similarity_boost": 0.80, "style": 0.45,
                                           "use_speaker_boost": True, "speed": 0.97}}
    spec["metadata"] = spec["metadata"].replace(
        "1. In the 1920s, Someone Planned to Drain the Mediterranean",
        "1. This One Dam Would Have Lowered the Entire Mediterranean")


for spec in SPECS:
    if spec["id"] == "002_atlantropa":
        _restructure_002(spec)



# ------------------------------------------------------------------ retention structure (003-006)
VOICE_RETENTION = {"voice_settings": {"stability": 0.35, "similarity_boost": 0.80, "style": 0.45,
                                      "use_speaker_boost": True, "speed": 0.97}}
LIFE = "Structures keep their shape."


def _mv(shot_, motion, secs=3):
    shot_ = dict(shot_); shot_["motion"] = motion + " " + LIFE; shot_["motion_seconds"] = secs
    return shot_


def _restructure(spec):
    old = spec["lines"]
    S = lambda li, si: dict(old[li]["shots"][si])
    sid = spec["id"]
    if sid == "003_shimizu_pyramid":
        L = [
            ("This pyramid... would be taller than two Burj Khalifas stacked on top of each other.", None,
             "Deep wind howling high above the sea, distant waves",
             [S(0, 0), _mv(S(8, 0), "Camera rises fast past the skyscraper and keeps climbing up the "
                                    "face of the giant lattice pyramid into the clouds.")]),
            ("A million people... would live inside it.", "1,000,000",
             "Vast echoing interior, distant crowd murmur, soft wind", [S(2, 0)]),
            ("And the craziest part... is how it would be built.", None,
             "Low electric hum, mechanical whirring",
             [_mv(S(5, 1), "Camera glides fast along the glowing black cable as pulses of light race "
                           "through it.")]),
            ("Japanese builder Shimizu designed it for Tokyo Bay.", None,
             "Harbour ambience, boat engines, gulls, light wind",
             [_mv(S(1, 0), "Fast low aerial flight across the bay toward the giant pyramid, boats "
                           "speeding past below, clouds streaming around its peak.")]),
            ("Two thousand and four metres tall.", "2,004 M", "Strong high-altitude wind",
             [_mv(S(1, 1), "Camera races straight up along the lattice edge, struts flashing past, "
                           "bursting through the clouds.")]),
            ("Thirty-storey skyscrapers... hanging inside it on cables.", None,
             "Creaking cables, wind through a steel frame, distant city hum",
             [_mv(S(3, 0), "Camera swoops between the hanging towers, people crossing sky bridges, "
                           "light beams sweeping."),
              _mv(S(3, 1), "Camera spirals around the thick cable as it strains, clouds rushing past "
                           "outside the frame.")]),
            ("Moving walkways. Sloping elevators. Robot pods racing through the frame.", None,
             "Futuristic transit whoosh, footsteps, soft chimes",
             [_mv(S(4, 0), "Camera flies fast alongside the moving walkways and gliding elevators, "
                           "crowds riding past."), S(4, 1)]),
            ("Robots would build it... for eighty years. With materials still being invented.", "80 YEARS",
             "Construction robots, welding sparks, heavy machinery over the sea",
             [_mv(S(5, 0), "Robot arms swing fast and lock a dark strut into place, a shower of "
                           "welding sparks, the sea churning below.")]),
            ("It was never built.", None, "Calm water, distant foghorn", [S(6, 0)]),
            ("But if it had been...", None, "Night wind, distant city hum", [S(7, 0)]),
            ("A million lives, above the clouds... all inside one pyramid.", None,
             "High wind above the clouds, soft sunrise birdsong",
             [_mv(S(8, 1), "Camera pushes fast through the struts out into the open sky above a sea "
                           "of clouds at sunrise.")]),
        ]
        title = "1. This Pyramid Would Be Taller Than Two Burj Khalifas"
    elif sid == "004_watkins_tower":
        L = [
            ("London tried to build a tower... taller than the Eiffel Tower.", None,
             "Victorian crowd chatter, wind, flags flapping", [S(0, 0)]),
            ("It ended... with dynamite.", None, "Distant rumble, debris falling", [S(6, 0)]),
            ("In 1890, railway tycoon Edward Watkin wanted London to win.", None,
             "Steam train arriving, hissing steam, station bell", [S(1, 0)]),
            ("His tower would rise forty-six metres higher than Paris.", "+46 M", "High wind, flags",
             [_mv(S(1, 1), "Camera rises fast between the two towers, sweeping up past the summit of "
                           "the shorter one toward the top of the taller one.")]),
            ("A hotel. Theatres. Turkish baths... all in the sky.", None,
             "Elegant Victorian restaurant, cutlery, string quartet, murmuring diners",
             [_mv(S(2, 0), "Camera glides fast through the sky restaurant past the diners toward the "
                           "windows and the clouds below."),
              _mv(S(2, 1), "Camera pushes fast through swirling steam toward the bright window.")]),
            ("Work began in 1893.", None, "Hammering rivets, clanging iron, workers shouting",
             [_mv(S(3, 0), "Sparks fly as workers hammer glowing rivets, a crane swings a girder fast "
                           "overhead.")]),
            ("But the money ran out... and the ground began to sink.", None,
             "Heavy rain, wind, creaking timber",
             [S(4, 0), _mv(S(4, 1), "Heavy rain lashes the abandoned site, a flash of lightning, the "
                                    "tarp whipping in the wind.")]),
            ("It reached forty-seven metres. Less than one-seventh of the plan.", "47 M",
             "Empty park, cold wind, distant crows",
             [_mv(S(5, 0), "Camera rises from the stubby iron base up through the ghostly outline of "
                           "the planned tower, high into the sky.")]),
            ("So they blew it up.", None, "Dynamite blast, debris and dust",
             [_mv(S(3, 1), "A blast of dust and smoke erupts from the short iron structure, debris "
                           "flying, workers and horses scattering.")]),
            ("Today, Wembley Stadium stands on the same spot.", None,
             "Huge stadium crowd roar, chanting",
             [_mv(S(7, 0), "Fast drone flight over the stadium toward the giant arch, crowds streaming "
                           "in below.")]),
            ("But if it had been finished... it would still be the tallest structure in London.", None,
             "Night city wind, distant traffic",
             [S(8, 0), _mv(S(8, 1), "Camera pulls back fast from the observation deck, revealing the "
                                    "vast glowing city spreading in every direction.")]),
        ]
        title = "1. London Tried to Beat the Eiffel Tower. It Ended With Dynamite."
    elif sid == "005_tatlins_tower":
        cylinder = shot("Close-up of a glowing glass cylinder high inside a dark iron spiral tower at "
                        "night, a ring of lights around it like a clock face, the city far below.",
                        "push_in")
        L = [
            ("This tower was designed... with rooms that spin.", None,
             "Deep metallic groan, storm wind", [S(0, 0)]),
            ("One of them... would turn all the way around, every single day.", None,
             "Slow mechanical rotation, ticking gears",
             [_mv(cylinder, "The glass cylinder turns steadily, the ring of lights sweeping around, "
                            "camera circling it.")]),
            ("Russia, 1920. The artist Vladimir Tatlin designs a monument.", None,
             "River ambience, distant ship horn, wind", [S(2, 0)]),
            ("Four hundred metres of iron, glass and steel.", "400 M", "High wind, iron creaking",
             [_mv(S(1, 0), "Camera rises fast up the spiral, overtaking the smaller lattice tower and "
                           "climbing into the sunset sky.")]),
            ("Taller than the Eiffel Tower. Tilted like the Earth's axis.", None,
             "Wind whistling through iron beams",
             [_mv(S(1, 1), "Camera races along the curving iron beam as it spirals upward, sunset "
                           "light flaring.")]),
            ("Inside: three giant glass buildings, stacked.", None,
             "Echoing hall, soft machinery hum",
             [_mv(S(3, 0), "Camera flies up fast past the three glowing glass buildings inside the "
                           "spiral.")]),
            ("The bottom one turns once a year.", "1 / YEAR", "Large hall, murmuring assembly",
             [_mv(S(4, 0), "Camera orbits fast around the giant glass cube hall as it turns, light "
                           "sweeping across the rows of seats.")]),
            ("The middle one... once a month.", "1 / MONTH", "Typewriters clacking, office murmur",
             [_mv(S(5, 0), "Camera circles quickly around the turning glass pyramid of offices, "
                           "workers at desks sliding past.")]),
            ("And the top one... once every day.", "1 / DAY", "Radio static, ticking clock",
             [_mv(S(6, 0), "The glass cylinder spins visibly as the camera orbits it fast, lights "
                           "streaking, the city far below wheeling past.")]),
            ("It was never built.", None, "Fog over a river, lapping water",
             [_mv(S(7, 0), "Fog rolls along the river, a lone boat drifts past, lamps flicker.")]),
            ("But if it had been...", None, "Night city ambience, wind", [S(8, 0)]),
            ("...Saint Petersburg would have a skyline that never stands still.", None,
             "Night river, gentle water, distant bells",
             [_mv(S(8, 1), "Camera sweeps low over the river toward the glowing spiral tower, "
                           "reflections rippling, a boat cutting through them.")]),
        ]
        title = "1. This Tower Was Designed to Spin. Once a Day."
    elif sid == "006_newton_cenotaph":
        L = [
            ("A sphere as big as the one in Las Vegas... drawn in 1784.", None,
             "Wind through cypress trees, distant birds",
             [_mv(S(0, 0), "Fast dramatic aerial swoop circling the colossal sphere, cypress trees "
                           "rushing past in the foreground, tiny figures below.", 5)]),
            ("And what he planned inside it... is even stranger.", None,
             "Deep echoing silence, a single low drone",
             [_mv(S(2, 0), "Camera dives down the shaft of light toward the tomb, dust swirling "
                           "around it.")]),
            ("French architect Étienne-Louis Boullée designed it for Isaac Newton.", None,
             "Quill scratching on parchment, candle crackle",
             [_mv(S(1, 1), "Camera glides fast across the parchment drawing as warm light sweeps "
                           "over the sphere.")]),
            ("A hollow sphere, one hundred and fifty metres across.", "150 M",
             "Wind, mist, distant voices",
             [_mv(S(1, 0), "Camera rises fast up the curve of the giant sphere, tiny figures below, "
                           "mist swirling.")]),
            ("By day, sunlight through tiny holes in the shell...", None,
             "Vast echoing chamber, soft wind", [S(3, 0)]),
            ("...would turn the inside into a night sky.", None, "Night ambience, soft crickets",
             [_mv(shot("Inside a colossal stone dome, thousands of bright sparkling points of daylight "
                       "shine through tiny holes like a dense starry night sky, the Milky Way-like "
                       "band of light clearly visible, a tiny figure standing below looking up.",
                       "pan_up"),
                  "Camera turns and rises as the bright points of starlight glitter and twinkle "
                  "across the dome.")]),
            ("At night, a giant glowing orb... would light it like the sun.", None,
             "Low warm hum, soft resonance",
             [_mv(S(5, 0), "Camera circles fast around the glowing orb as its golden light flares and "
                           "pulses across the curved walls.")]),
            ("It was never built.", None, "Morning mist, distant birds",
             [_mv(S(6, 0), "Mist rolls across the empty field, the cypress trees sway in the wind.")]),
            ("Two hundred and thirty-nine years later, Las Vegas opened a sphere almost the same size.",
             "239 YEARS", "Busy Las Vegas street, crowd, traffic, distant music",
             [_mv(S(7, 0), "Fast drone flight toward the glowing sphere as patterns of light ripple "
                           "across its surface, crowds below."),
              _mv(S(7, 1), "Camera pulls back slowly between the two spheres as the sky darkens.")]),
            ("Now imagine standing inside the original... a whole sky, built for one man.", None,
             "Vast echoing chamber, soft celestial tones", [S(8, 0)]),
        ]
        title = "1. A Sphere as Big as the Las Vegas Sphere, Drawn in 1784"
    else:
        return
    spec["lines"] = []
    for text, callout, amb, shots_ in L:
        line = {"text": text, "ambience": amb, "shots": shots_}
        if callout:
            line["callout"] = callout
        spec["lines"].append(line)
    never = next(i for i, l in enumerate(spec["lines"]) if l["text"].startswith("It was never built")
                 or l["text"].startswith("So they blew it up"))
    spec["sfx"] = {"riser_into_lines": [never], "impact_on_lines": [never]}
    spec["settings"] = VOICE_RETENTION
    first_title = spec["metadata"].split("\n")[3]
    spec["metadata"] = spec["metadata"].replace(first_title, title, 1)


for spec in SPECS:
    _restructure(spec)


if __name__ == "__main__":
    import sys
    only = sys.argv[1:]
    for spec in SPECS:
        if only and not any(spec["id"].startswith(o) for o in only):
            continue
        spec = {**spec, "status": "ready-retention-fix"} if only else spec
        path = HERE / f"{spec['id']}.json"
        path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
        n_shots = sum(len(l["shots"]) for l in spec["lines"])
        n_motion = sum(1 for l in spec["lines"] for s in l["shots"] if s.get("motion"))
        words = sum(len(l["text"].split()) for l in spec["lines"])
        print(f"{path.name}: lines={len(spec['lines'])} shots={n_shots} motion={n_motion} words={words}")
