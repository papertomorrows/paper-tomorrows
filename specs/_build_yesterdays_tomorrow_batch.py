"""Builds spec files 007-012 (Yesterday's Tomorrow series).

Run:  python3 specs/_build_yesterdays_tomorrow_batch.py [ids...]
Passing ids writes only those specs and marks them ready for production.
"""

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
STILL = "Buildings and machines keep their shape; no warping."
NOLOGO = " No logos, no brand names, no readable text."


def shot(prompt, move="push_in", motion=None, secs=3):
    d = {"prompt": prompt + NOLOGO, "move": move}
    if motion:
        d["motion"] = motion
        d["motion_seconds"] = secs
    return d


def metadata(num, name, titles, desc, sources, hashtags, tags, question, playlist):
    out = [f"# Short #{num} - {name}", "", "## Title options (1 = recommended)"]
    out += [f"{i}. {t}" for i, t in enumerate(titles, 1)]
    out += ["", "## Description", desc.strip(), "",
            "Visuals are AI-generated concept art, not photographs or historical footage.",
            "", "Sources:"] + [f"- {s}" for s in sources]
    out += ["", " ".join(hashtags), "", "## Tags", ", ".join(tags),
            "", "## First comment (post from the channel)", question,
            "", "## Playlist", playlist,
            "", "## Upload checklist",
            "- Altered or synthetic content disclosure: YES (realistic AI-generated scenes)",
            "- Made for kids: No", "- Category: Education; video, title and description language: English"]
    return "\n".join(out) + "\n"


PLAYLIST = "Yesterday's Tomorrow: How the Past Imagined the Future"
SPECS = []

# ------------------------------------------------------------------ 007 1900 predictions
SPECS.append({
    "id": "007_predictions_1900",
    "seed_base": 1900,
    "lines": [
        {"text": "In 1900, an American magazine made twenty-eight predictions about our world.",
         "shots": [shot("A Victorian family in 1900 clothing standing at a parlour window, gazing at a "
                        "glowing vision of a futuristic city floating in the night sky outside, warm "
                        "gaslight inside, cinematic.", "push_in",
                        "The glowing future city shimmers and lights pulse in the sky, curtains stir, "
                        "camera pushes slowly toward the window. " + STILL, 5)]},
        {"text": "Strawberries... as large as apples.",
         "shots": [shot("An Edwardian market stall piled with enormous strawberries the size of apples, "
                        "amazed shoppers in hats, morning light.", "push_in",
                        "Shoppers lean in and lift a giant strawberry, awnings flutter. " + STILL)]},
        {"text": "No more mosquitoes. No more flies.",
         "shots": [shot("A peaceful Edwardian summer evening picnic beside a calm marsh, people relaxed "
                        "in white clothes, golden light, perfectly still air.", "pull_out",
                        "Reeds sway gently, light glints on the water, a parasol turns slowly. " + STILL)]},
        {"text": "And everybody would walk ten miles a day.",
         "shots": [shot("A long country road crowded with Edwardian people of all ages walking briskly "
                        "into the distance, dust in the sunlight.", "pull_out",
                        "The crowd strides steadily down the road, dust rising in the sunlight. " + STILL)]},
        {"text": "Wrong. Wrong. And very wrong.",
         "shots": [shot("A present-day man asleep on a sofa scrolling his phone, a takeaway box beside "
                        "him, dim room, humorous cinematic tone.", "push_in")]},
        {"text": "But then... photographs, sent from any distance.",
         "shots": [shot("An early 1900s telegraph office, a brass machine slowly printing a photograph "
                        "line by line onto paper, an operator watching in awe, lamp light.", "push_in",
                        "The machine prints the photograph line by line, the operator leans in. " + STILL),
                   shot("Close-up of a hand holding a modern smartphone showing a photo just received, "
                        "warm evening light, shallow depth of field.", "pull_out")]},
        {"text": "Telephones... reaching around the world.",
         "shots": [shot("A Victorian woman speaking into a candlestick telephone, glowing lines of light "
                        "from the phone stretching across a large globe beside her.", "push_in",
                        "Lines of light race across the globe from the telephone, the woman smiles. "
                        + STILL)]},
        {"text": "Ready-cooked meals... you could simply buy.",
         "shots": [shot("A 1900 shop window filled with hot ready-made meals in boxes, steam rising, "
                        "customers in bowler hats queueing.", "push_in"),
                   shot("A modern delivery rider on a scooter at night in rain with a food bag, neon "
                        "reflections on wet streets.", "pull_out",
                        "The scooter rides past through the rain, neon lights streaking. " + STILL)]},
        {"text": "Not bad... for 1900.",
         "shots": [shot("A Victorian gentleman in 1900 clothes standing on a present-day city street at "
                        "night, looking up in wonder at glowing skyscrapers, people with phones "
                        "passing him.", "pan_up",
                        "Slow upward crane from the astonished Victorian man to the glowing skyline, "
                        "people flowing past. " + STILL, 5)]},
    ],
    "sfx": {"riser_into_lines": [5], "impact_on_lines": [5]},
    "metadata": metadata(
        "007", "Predictions from 1900 About the Year 2000",
        ["In 1900, They Predicted Our World. Some Came True.",
         "28 Predictions From 1900 About Today",
         "What People in 1900 Thought the Year 2000 Would Look Like"],
        "In December 1900, the Ladies' Home Journal published \"What May Happen in the Next Hundred "
        "Years\" by engineer John Elfreth Watkins Jr.: 28 predictions about the year 2000. Some "
        "missed (no C, X or Q in the alphabet, strawberries as large as apples, everybody walking ten "
        "miles a day). Others came true: photographs telegraphed from any distance, telephones around "
        "the world, ready-cooked meals bought from shops.",
        ["Open Culture: \"In 1900, Ladies' Home Journal Publishes 28 Predictions for the Year 2000\"",
         "Scanalyst: list of the article's prediction headings",
         "Wikipedia: J. Elfreth Watkins"],
        ["#YesterdaysTomorrow", "#Predictions", "#Year2000", "#History", "#Future"],
        ["predictions from 1900", "year 2000 predictions", "ladies home journal 1900",
         "john elfreth watkins", "what may happen in the next hundred years", "past predictions",
         "how people imagined the future", "retrofuturism", "predictions that came true",
         "history of the future", "1900s", "futurism"],
        "Which 1900 prediction would you most want to come true?",
        PLAYLIST),
})

# ------------------------------------------------------------------ 008 Pan Am Moon flights
SPECS.append({
    "id": "008_moon_flights_club",
    "seed_base": 1968,
    "lines": [
        {"text": "Ninety-three thousand people... signed up for a flight to the Moon.",
         "shots": [shot("A sleek 1960s passenger spaceplane in blue and white airline livery soaring above "
                        "the curve of the Earth toward a bright Moon, retro-futuristic, cinematic.",
                        "push_in",
                        "The spaceplane glides forward toward the Moon, Earth's glow sliding beneath it. "
                        + STILL, 5)]},
        {"text": "Not with NASA. With an airline.",
         "shots": [shot("A glamorous 1960s airline ticket counter, travellers in sixties fashion queueing, "
                        "a large poster of the Moon on the wall.", "pull_out",
                        "Travellers shuffle forward in the queue, an agent stamps a ticket. " + STILL)]},
        {"text": "In 1968, Pan Am started a club... called First Moon Flights.",
         "shots": [shot("A 1968 airline office with a long row of filing cabinets and a typist preparing "
                        "membership cards, a model spaceplane on the desk.", "push_in",
                        "The typist types quickly, papers move, a ceiling fan turns. " + STILL)]},
        {"text": "Membership was free.",
         "shots": [shot("Close-up of a hand holding a blank 1960s membership card with a small spaceplane "
                        "illustration, a family kitchen table behind.", "push_in")]},
        {"text": "And the first flight was expected... around the year two thousand.",
         "shots": [shot("A 1960s family in their living room looking at a wall calendar showing a distant "
                        "future year, the Moon visible through the window.", "pull_out",
                        "The family smiles and points out the window at the Moon, curtains move. "
                        + STILL),
                   shot("A retro-futuristic lunar spaceport with a domed terminal and a passenger "
                        "spaceplane parked on the grey surface, Earth in the black sky.", "pan_up",
                        "Lights blink on the terminal, the spaceplane's engines glow softly. " + STILL)]},
        {"text": "In 1971, the club stopped taking new names.",
         "shots": [shot("A 1970s office being cleared out, a stack of membership cards in a closed "
                        "cardboard box, fading light.", "push_in")]},
        {"text": "Twenty years later... Pan Am itself was gone.",
         "shots": [shot("An empty abandoned airport terminal at dusk, rows of vacant seats, departure "
                        "boards dark, dust in the air.", "pull_out",
                        "Dust drifts through shafts of fading light in the empty terminal. " + STILL)]},
        {"text": "But imagine, for a moment... boarding that flight.",
         "shots": [shot("Inside a 1960s-style passenger spaceplane cabin, passengers in sixties fashion "
                        "looking out of round windows at the Earth below, a flight attendant serving "
                        "drinks, warm cabin light.", "push_in",
                        "The cabin drifts gently, passengers turn to the windows as Earth slides past, "
                        "a glass floats in low gravity. " + STILL, 5)]},
        {"text": "Today, those cards hang in museums.",
         "shots": [shot("A museum display case lit softly, holding a single 1960s spaceflight membership "
                        "card and a small spaceplane model, visitors reflected in the glass.", "push_in")]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "008", "Pan Am's First Moon Flights Club",
        ["93,000 People Booked a Flight to the Moon. With an Airline.",
         "Pan Am Took Reservations for Flights to the Moon",
         "The Airline That Sold Tickets to the Moon"],
        "Pan Am issued more than 93,000 free \"First Moon Flights\" club cards between 1968 and 1971, "
        "with the first flight expected around the year 2000. The airline stopped taking new names in "
        "1971 and declared bankruptcy in 1991. Some of the cards are now in museum collections.",
        ["Smithsonian National Air and Space Museum: \"Were you a member of the First Moon Flights Club?\"",
         "National Endowment for the Humanities: \"Long before SpaceX, Pan Am was booking flights to the Moon\""],
        ["#YesterdaysTomorrow", "#PanAm", "#Moon", "#SpaceTravel", "#History"],
        ["pan am moon flights", "first moon flights club", "pan am moon", "flights to the moon",
         "space tourism history", "pan am", "moon tourism", "1960s future", "retrofuturism",
         "how people imagined the future", "space age", "past predictions"],
        "Would you have signed up for the first flight to the Moon?",
        PLAYLIST),
})

# ------------------------------------------------------------------ 009 Lunar Hilton
SPECS.append({
    "id": "009_lunar_hilton",
    "seed_base": 1967,
    "lines": [
        {"text": "In 1967, Hilton planned a hotel... on the Moon.",
         "shots": [shot("A glowing retro-futuristic hotel entrance dome on the grey lunar surface at "
                        "night, the Earth hanging in the black sky, soft warm light from the doors.",
                        "push_in",
                        "Camera glides low over the lunar dust toward the glowing entrance, the Earth "
                        "shining above. " + STILL, 5)]},
        {"text": "Built thirty feet underground... to keep the temperature steady.",
         "shots": [shot("Cross-section view of a hotel buried beneath the lunar surface, three levels "
                        "lit warmly underground, grey rock above, Earth in the sky.", "pan_down",
                        "Camera descends slowly from the surface through the rock to the lit levels "
                        "below. " + STILL)]},
        {"text": "A hundred rooms... decorated just like hotels on Earth.",
         "shots": [shot("A 1960s hotel room with patterned carpet, a neatly made bed and a lamp, but the "
                        "window shows the grey lunar landscape and the Earth.", "push_in",
                        "The lamp glows, a curtain sways slightly, Earth drifts in the window. "
                        + STILL),
                   shot("A long 1960s hotel corridor carved under the Moon, numbered doors, warm "
                        "lighting, a guest in a sixties suit walking.", "push_in",
                        "The guest walks slowly down the corridor, lights reflecting. " + STILL)]},
        {"text": "A lounge. A piano bar. And a dome for watching the stars.",
         "shots": [shot("A stylish 1960s lounge with a piano bar under a glass observation dome on the "
                        "Moon, guests with cocktails, the stars and Earth above.", "pull_out",
                        "The pianist plays, guests raise glasses, stars glitter through the dome. "
                        + STILL, 5)]},
        {"text": "Drinks... at the push of a button.",
         "shots": [shot("A retro-futuristic bar console with chrome buttons, a cocktail glass filling "
                        "automatically beneath a nozzle, 1960s styling.", "push_in",
                        "A finger presses a glowing button and the glass fills with a bright drink. "
                        + STILL)]},
        {"text": "Even the kitchen... would run on nuclear power.",
         "shots": [shot("A gleaming automated 1960s kitchen under the Moon with chrome machines and a "
                        "glowing blue reactor core behind glass, robot arms cooking.", "pan_up",
                        "Robot arms stir and plate food, the blue core pulses softly. " + STILL)]},
        {"text": "It was never built.",
         "shots": [shot("An empty, untouched lunar plain under black sky, footprint-free grey dust, the "
                        "Earth small on the horizon.", "pull_out")]},
        {"text": "But imagine, for a moment... checking in.",
         "shots": [shot("A 1960s hotel lobby beneath the Moon's surface, a guest in a sixties suit at the "
                        "front desk receiving a key, a huge round window behind showing the Earth "
                        "hanging above grey lunar hills.", "push_in",
                        "The receptionist hands over the key, the guest turns to the giant window as "
                        "the camera pushes toward the Earth. " + STILL, 5)]},
        {"text": "Hilton even made room keys for it.",
         "shots": [shot("Close-up of an old brass hotel room key with a tag shaped like a crescent Moon "
                        "resting on velvet, soft spotlight.", "push_in")]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "009", "The Lunar Hilton",
        ["In 1967, Hilton Planned a Hotel on the Moon",
         "The Moon Hotel With a Piano Bar",
         "Hilton's Plan for a Hotel 30 Feet Under the Moon"],
        "In a 1967 speech, Barron Hilton described a Lunar Hilton: a hotel about 30 feet below the "
        "Moon's surface with 100 rooms, a lounge, a piano bar, an observation dome, drinks at the push "
        "of a button and a nuclear-powered kitchen. It was never built, but Hilton handed out "
        "promotional room keys for it.",
        ["Supercluster: \"Space was always the plan for Hilton\"",
         "CNN Travel: Hilton hotel on the Moon"],
        ["#YesterdaysTomorrow", "#Moon", "#Hilton", "#SpaceAge", "#History"],
        ["lunar hilton", "hilton on the moon", "hotel on the moon", "moon hotel", "barron hilton",
         "space hotel", "1967 moon hotel", "space tourism history", "retrofuturism", "space age",
         "how people imagined the future", "past predictions"],
        "Would you book a room 30 feet under the Moon?",
        PLAYLIST),
})

# ------------------------------------------------------------------ 010 Futurama 1939
SPECS.append({
    "id": "010_futurama_1939",
    "seed_base": 1939,
    "lines": [
        {"text": "In 1939, people waited in long lines... to see the year 1960.",
         "shots": [shot("A huge crowd in 1939 clothing queueing outside a sweeping streamline-moderne "
                        "exhibition pavilion at a world's fair, flags and banners, bright summer sky.",
                        "pull_out",
                        "The crowd shuffles forward, flags flutter, camera rises over the queue. "
                        + STILL, 5)]},
        {"text": "It was called Futurama.",
         "shots": [shot("Inside a dark 1939 exhibition hall, a vast glowing miniature landscape of a "
                        "future city stretching into the distance, visitors silhouetted.", "push_in",
                        "Tiny lights twinkle across the miniature city, visitors lean forward. "
                        + STILL)]},
        {"text": "A model of America's future... one acre wide.",
         "shots": [shot("A colossal detailed miniature model of a futuristic American landscape with "
                        "cities, farms, rivers and highways, seen from above, warm exhibition light.",
                        "pan_up",
                        "Camera glides smoothly over the enormous model like an aircraft. " + STILL)]},
        {"text": "Half a million buildings. Fifty thousand cars.",
         "shots": [shot("Macro view of a miniature futuristic city with streamlined skyscrapers and "
                        "thousands of tiny cars on elevated roads.", "push_in",
                        "Tiny model cars glide along the miniature roads between the towers. "
                        + STILL)]},
        {"text": "Visitors rode in moving chairs... gliding high above it.",
         "shots": [shot("1939 visitors seated in a row of moving armchairs travelling on a track above a "
                        "giant illuminated model landscape, faces lit with wonder.", "pan_down",
                        "The chairs glide slowly along the track above the glowing model. " + STILL)]},
        {"text": "Up to thirty thousand people a day.",
         "shots": [shot("Aerial view of a 1939 world's fair with an enormous line of people winding "
                        "around a futuristic pavilion, crowds everywhere.", "pull_out")]},
        {"text": "Its giant highways... looked like science fiction.",
         "shots": [shot("Close view of the miniature model's wide multi-lane highways sweeping through "
                        "curved interchanges between skyscrapers, tiny streamlined cars.", "push_in",
                        "Tiny cars stream along the curving lanes of the model highway. " + STILL)]},
        {"text": "Less than twenty years later... America began building its interstate highways.",
         "shots": [shot("A real 1950s highway construction site, bulldozers and workers laying a wide new "
                        "concrete road across open country, dust and sunlight.", "pull_out",
                        "Bulldozers push earth, trucks roll past, dust drifts in the sun. " + STILL),
                   shot("Present-day aerial view of a vast highway interchange at sunset, streams of car "
                        "lights flowing through looping ramps.", "pan_up",
                        "Rivers of car lights flow through the looping interchange at dusk. "
                        + STILL, 5)]},
        {"text": "The future... had been on display all along.",
         "shots": [shot("A 1939 visitor's hand holding a small souvenir pin over a photo-like view of a "
                        "modern highway city, past and present blending, warm light.", "push_in")]},
    ],
    "sfx": {"riser_into_lines": [7], "impact_on_lines": [7]},
    "metadata": metadata(
        "010", "Futurama: The 1939 World's Fair Vision of 1960",
        ["In 1939, Millions Lined Up to See the Year 1960",
         "Futurama: The 1939 Model That Predicted America's Highways",
         "The One-Acre Model of the Future From the 1939 World's Fair"],
        "Futurama, designed by Norman Bel Geddes for General Motors at the 1939 New York World's Fair, "
        "showed America around 1960: a one-acre model with more than 500,000 buildings and about "
        "50,000 cars, viewed from moving chairs. Up to 30,000 people a day waited in line. Its vision of "
        "a national expressway network is widely credited with influencing the Interstate Highway "
        "System.",
        ["Wikipedia: Futurama (New York World's Fair)",
         "Harry Ransom Center: \"I Have Seen the Future\""],
        ["#YesterdaysTomorrow", "#Futurama", "#WorldsFair", "#1939", "#History"],
        ["futurama 1939", "1939 world's fair", "new york world's fair", "norman bel geddes",
         "general motors futurama", "world of tomorrow", "interstate highway history",
         "how people imagined the future", "retrofuturism", "1930s future", "past predictions",
         "streamline moderne"],
        "Which 1939 idea of the future would you have lined up to see?",
        PLAYLIST),
})

# ------------------------------------------------------------------ 011 En L'An 2000
SPECS.append({
    "id": "011_en_lan_2000",
    "seed_base": 1899,
    "lines": [
        {"text": "In 1899, French artists drew the year 2000.",
         "shots": [shot("A flying hansom cab with wings and a propeller carrying passengers in 1900 "
                        "clothing above the rooftops of Paris, the Eiffel Tower behind, soft "
                        "pastel sky, cinematic.", "push_in",
                        "The winged cab flies toward the camera over the Paris rooftops, wings beating, "
                        "propeller spinning. " + STILL, 5)]},
        {"text": "Flying taxis.",
         "shots": [shot("Several winged flying cabs with propellers parked on a Parisian rooftop "
                        "platform, a gentleman in a top hat climbing aboard.", "pan_up",
                        "A cab lifts off from the rooftop, coat tails flapping in the wind. " + STILL)]},
        {"text": "Police patrolling the sky.",
         "shots": [shot("A Belle Epoque policeman in uniform and cap flying with mechanical wings above "
                        "Paris, chasing a winged figure, clouds around.", "pull_out",
                        "The flying policeman swoops forward through the clouds. " + STILL)]},
        {"text": "Machines that scrub the floor... all by themselves.",
         "shots": [shot("An ornate 1900 French parlour where a brass electric machine with brushes scrubs "
                        "the parquet floor by itself while a maid watches, amused.", "push_in",
                        "The brass machine glides across the floor, brushes spinning. " + STILL)]},
        {"text": "A bus... pulled by a whale.",
         "shots": [shot("A Belle Epoque passenger carriage floating on the sea, pulled by a large whale in "
                        "a harness, passengers in hats, gentle waves.", "pull_out",
                        "The whale swims forward pulling the carriage, waves splashing gently. "
                        + STILL)]},
        {"text": "And croquet... under the sea.",
         "shots": [shot("Elegant people in 1900 clothing and old diving helmets playing croquet on the "
                        "seabed, fish swimming by, shafts of light from above.", "push_in",
                        "A diver swings a mallet, bubbles rise, fish drift past. " + STILL)]},
        {"text": "The cards were made for the 1900 World's Fair in Paris... but they were never released.",
         "shots": [shot("A dusty abandoned toy factory in France, stacks of old illustrated cards in "
                        "wooden crates, cobwebs, light through grimy windows.", "pull_out",
                        "Dust drifts through the light, a loose card slides off a stack. " + STILL)]},
        {"text": "They sat forgotten for decades... until Isaac Asimov published them in 1986.",
         "shots": [shot("An antique shop in Paris, an old crate of colourful illustrated cards being "
                        "opened by curious hands, warm lamplight.", "push_in"),
                   shot("A 1980s writer's desk with a typewriter, piles of books and colourful old "
                        "illustrated cards spread out, evening lamp light.", "pull_out")]},
        {"text": "We got the robot cleaners. We're still waiting on the whale bus.",
         "shots": [shot("A modern apartment where a round robot vacuum glides across the floor, through "
                        "the window a whale-drawn carriage floats past on a misty sea, playful "
                        "cinematic tone.", "push_in",
                        "The robot vacuum glides across the floor as the whale carriage drifts past "
                        "the window. " + STILL, 5)]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "011", "En L'An 2000: France in the Year 2000",
        ["In 1899, French Artists Drew the Year 2000",
         "Flying Taxis and Whale Buses: 1899 Predictions for the Year 2000",
         "The 1899 Cards That Predicted the Robot Vacuum"],
        "En L'An 2000 (\"In the Year 2000\") is a series of at least 78 French illustrated cards, the "
        "first made by Jean-Marc Côté for the 1900 World Exhibition in Paris. They imagined air cabs, "
        "flying police, an electric floor scrubber, a whale-drawn bus and underwater croquet. The cards "
        "were never distributed; they were rediscovered decades later and published by Isaac Asimov in "
        "Futuredays (1986).",
        ["The Public Domain Review: \"Lost Futures: A 19th-Century Vision of the Year 2000\"",
         "Wikipedia: En L'An 2000",
         "Open Culture: \"How French Artists in 1899 Envisioned What Life Would Look Like in the Year 2000\""],
        ["#YesterdaysTomorrow", "#Year2000", "#Paris", "#Retrofuturism", "#History"],
        ["en l'an 2000", "en lan 2000", "france in the year 2000", "jean-marc cote", "jean marc côté",
         "isaac asimov futuredays", "1899 predictions", "year 2000 predictions", "belle epoque future",
         "retrofuturism", "how people imagined the future", "past predictions"],
        "Which one should we build first: the flying taxi or the whale bus?",
        PLAYLIST),
})

# ------------------------------------------------------------------ 012 Miracle Kitchen
SPECS.append({
    "id": "012_miracle_kitchen",
    "seed_base": 1959,
    "lines": [
        {"text": "In 1959, America showed the Soviet Union... the kitchen of the future.",
         "shots": [shot("A gleaming retro-futuristic 1950s kitchen in pastel colours with chrome "
                        "appliances, a small round robot floor cleaner gliding across the tiles, "
                        "visitors in fifties clothing watching from a rope line.", "push_in",
                        "The little robot glides across the shining floor, visitors lean in to watch. "
                        + STILL, 5)]},
        {"text": "A robot that cleaned the floor... all by itself.",
         "shots": [shot("Close-up of a small domed 1950s robot floor cleaner with blinking lights "
                        "polishing a checkerboard floor.", "push_in",
                        "The robot turns and polishes the floor, its lights blinking. " + STILL)]},
        {"text": "A dishwasher that rolled... to the dining table.",
         "shots": [shot("A chrome 1950s dishwasher unit gliding along a track in the floor toward a "
                        "dining table set with dishes, a smiling housewife watching.", "pan_down",
                        "The dishwasher rolls smoothly along its track to the table. " + STILL)]},
        {"text": "Push-button controls... for everything.",
         "shots": [shot("A 1950s control panel full of colourful push buttons and small lights built into "
                        "a pastel kitchen wall, a finger pressing a button.", "push_in",
                        "A finger presses a button and the panel lights up in sequence. " + STILL)]},
        {"text": "And a planning centre... like a computer for the home.",
         "shots": [shot("A 1950s home planning centre desk with a small screen, dials and blinking "
                        "lights built into a kitchen, a woman reading a printout.", "pull_out",
                        "The screen flickers, lights blink across the console. " + STILL)]},
        {"text": "It looked like magic.",
         "shots": [shot("Faces of amazed visitors in 1950s clothing watching a demonstration, mouths "
                        "open, warm exhibition light.", "push_in")]},
        {"text": "But there was a secret.",
         "shots": [shot("A large mirror on the wall of a 1950s show kitchen, faint shadowy outline of a "
                        "man barely visible behind the glass, ominous lighting.", "push_in")]},
        {"text": "Behind a mirror... a man was steering the robot by radio.",
         "shots": [shot("Behind a two-way mirror, a man in a 1950s shirt and tie sits at a radio "
                        "control box with joysticks, watching the kitchen through the glass, "
                        "the visitors unaware.", "pull_out",
                        "The man works the joysticks, through the glass the robot turns on cue. "
                        + STILL, 5)]},
        {"text": "Today... the robot really does clean the floor by itself.",
         "shots": [shot("A modern bright apartment where a round robot vacuum cleans the floor alone, "
                        "sunlight through the window, nobody around.", "pull_out",
                        "The robot vacuum glides across the floor and turns, sunlight shifting. "
                        + STILL)]},
    ],
    "sfx": {"riser_into_lines": [6], "impact_on_lines": [6]},
    "metadata": metadata(
        "012", "The Miracle Kitchen of 1959",
        ["The 1950s Kitchen of the Future Had a Secret",
         "This 1959 Robot Floor Cleaner Was Secretly Remote-Controlled",
         "The Miracle Kitchen America Showed the Soviet Union"],
        "RCA/Whirlpool's Miracle Kitchen, shown at the 1959 American National Exhibition in Moscow, "
        "featured a robot floor cleaner, a dishwasher that rolled to the table, push-button controls "
        "and a home planning centre. The robot and the dishwasher were not automatic: a person behind "
        "a two-way mirror operated them by radio.",
        ["Gizmodo: \"The 1950s Miracle Kitchen of the Future Had Its Own Robot\"",
         "Whirlpool Corporation: \"The future is now\" (museum exhibit)"],
        ["#YesterdaysTomorrow", "#KitchenOfTheFuture", "#1950s", "#Retrofuturism", "#History"],
        ["miracle kitchen", "rca whirlpool miracle kitchen", "kitchen of the future",
         "1950s kitchen of the future", "1959 american national exhibition moscow",
         "robot floor cleaner 1959", "before roomba", "retrofuturism", "1950s future",
         "how people imagined the future", "past predictions", "cold war kitchen"],
        "Would you have believed the robot was real?",
        PLAYLIST),
})

if __name__ == "__main__":
    only = sys.argv[1:]
    for spec in SPECS:
        if only and not any(spec["id"].startswith(o) for o in only):
            continue
        if only:
            spec = {**spec, "status": "ready"}
        path = HERE / f"{spec['id']}.json"
        path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
        n = sum(len(l["shots"]) for l in spec["lines"])
        m = sum(1 for l in spec["lines"] for s in l["shots"] if s.get("motion"))
        w = sum(len(l["text"].split()) for l in spec["lines"])
        print(f"{path.name}: lines={len(spec['lines'])} shots={n} motion={m} words={w}")
