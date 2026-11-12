#!/usr/bin/env python3
"""
EduCrew: From a Little Dream to a Bigger World. Source of the 10-episode series.

Characters, voices and style are defined ONCE here and shared by every episode,
so nothing can drift between episodes. Run this file to (re)write the episode files:

    python series/educrew_biography.py

It writes episodes/EduCrew_Characters.json (the character bible images, make these first)
and episodes/EduCrew_Biography_Episode_01.json ... _10.json.
Narration and dialogue are copied exactly as supplied; nothing is reworded.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP_DIR = os.path.join(ROOT, "episodes")

# Visual language taken from the client's reference video (not its scenes, characters or watermark):
# painterly 3D storybook diorama, cosy high wide views full of small life, blue-hour skies, glowing windows,
# a big tree canopy framing the top, flowing water with ducks, flowers, hens, a cat, clotheslines; slow camera.
STYLE = ("high-quality painterly 3D animated storybook film still, cosy miniature-diorama feel, charming stylized 3D "
         "characters with soft simplified facial features, richly detailed Indian environment full of small life: "
         "birds, butterflies, ducks, hens, potted flowers, lush green trees, warm glowing windows, soft blue-hour or "
         "golden light, gentle realistic shadows, depth and atmosphere, rich warm colours, vertical cinematic composition")
NEGATIVE = ("photorealistic, photograph, live action, real people, 2D, flat illustration, anime, sketch, cartoon drawing, "
            "plastic doll, cheap TV animation, European house, Mediterranean villa, terracotta tiled roof, low quality, blurry, text, letters, watermark, logo, subtitles, signature, "
            "deformed, distorted face, scary, creepy, extra limbs, extra fingers, duplicated person, bindi, tilak, "
            "sindoor, temple, idol, diya, rangoli, religious symbols, music instruments")

# ---- PERMANENT CHARACTER BIBLE -------------------------------------------------------------
# Her signature, kept at every age: slim build, warm medium-brown skin, thick black hair,
# TEAL clothes with a MUSTARD-YELLOW dupatta/accent.
HER = "slim build, warm medium-brown skin, thick black hair"
CHARACTERS = {
    "GIRL6": "a 6-year-old Indian Muslim girl with two long black plaits tied with red ribbon bows, no hairband, "
             f"small and {HER}, knee-length teal frock with tiny white flowers over white churidar leggings, "
             "mustard-yellow cardigan",
    "GIRL11": f"the same Indian Muslim girl now 11 years old, {HER} in two long plaits with red ribbons, "
              "school uniform of white salwar kameez with a teal dupatta pinned across, navy school bag",
    "WOMAN19": f"a 19-year-old Indian Muslim young woman, 160 cm tall, {HER} in a single side plait, "
               "modest teal cotton salwar kameez, mustard-yellow dupatta loosely covering her head, cloth shoulder bag",
    "WOMAN22": f"the same Indian Muslim young woman now 22, 160 cm tall, {HER} in a single side plait, "
               "modest teal salwar kameez, mustard-yellow dupatta loosely covering her head",
    "BRIDE": f"the same Indian Muslim young woman as a bride, {HER}, modest deep red and gold embroidered gharara "
             "with a heavy dupatta covering her head, gold bangles",
    "WIFE": f"the same Indian Muslim young woman, now married, about 25, {HER} in a low bun, "
            "modest teal salwar kameez, mustard-yellow dupatta covering her head, gold bangles",
    "MOTHER": f"the same Indian Muslim woman now a young mother about 30, {HER} in a low bun, "
              "modest teal salwar kameez, mustard-yellow dupatta covering her head",
    "TEACHER": f"the same Indian Muslim woman now about 32, {HER} in a low bun, modest teal kurta with straight "
               "trousers, mustard-yellow dupatta draped over her head, steel-strap wristwatch, small black handbag",
    "TRAINER": f"the same Indian Muslim woman now about 37, {HER} in a low bun, modest teal kurta, "
               "mustard-yellow dupatta over her head, round reading glasses, steel-strap wristwatch",
    "DESIGNER": f"the same Indian Muslim woman now about 39, {HER} in a low bun, modest teal kurta with a navy "
                "long jacket, mustard-yellow dupatta over her head, round reading glasses, ID lanyard",
    "FOUNDER": f"the same Indian Muslim woman in her early 40s, confident graceful posture, {HER} in a low bun, "
               "elegant teal kurta, navy long jacket, mustard-yellow dupatta over her head, round reading glasses",
    "AMMI": "the mother, a kind Indian Muslim woman in her early 30s, medium build, wearing a deep maroon red "
            "salwar kameez (not teal, not green) with a cream dupatta covering her hair, green glass bangles",
    "AMMI_OLDER": "the mother, now in her early 50s, medium build, grey streaks in her hair, wearing a deep maroon red "
                  "salwar kameez (not teal, not green) with a cream dupatta covering her hair, green glass bangles, "
                  "reading glasses",
    "ABBU": "her father, an Indian Muslim man in his mid-30s, medium-tall, short black hair, neatly trimmed short "
            "black beard, pale blue shirt and grey trousers, steel-strap wristwatch",
    "DADI": "her grandmother, a small Indian Muslim woman about 65, silver hair, off-white salwar kameez, "
            "lavender dupatta covering her head, round spectacles",
    "BHAI": "her older brother, a thin 10-year-old Indian boy with short black hair, white half-sleeve shirt, khaki shorts",
    "GROOM": "her groom, a tall Indian Muslim man in his late 20s, short black hair, short beard, cream sherwani",
    "IN_LAW": "her mother-in-law, a gentle Indian Muslim woman in her late 50s, modest lilac salwar kameez, "
              "white dupatta covering her head",
    "DAUGHTER": "a 6-year-old Indian girl with warm medium-brown skin and curly black hair in a high ponytail with "
                "a yellow clip, pink frock with white leggings",
    "SON": "a 4-year-old Indian boy with warm medium-brown skin and short straight black hair, green t-shirt and "
           "blue shorts",
    "DAUGHTER11": "an 11-year-old Indian girl with warm medium-brown skin and curly black hair in a high ponytail "
                  "with a yellow clip, school uniform",
    "SON9": "a 9-year-old Indian boy with warm medium-brown skin and short straight black hair, school uniform with "
            "a green school bag",
    "FRIEND_SCHOOL": "her school friend, an 11-year-old girl with a short black bob, same school uniform",
    "FRIEND_COLLEGE": "her college friend, a cheerful young woman of 19 with a short black bob, lavender salwar kameez",
    "SCHOOL_TEACHER": "a kind schoolteacher in her 40s in a green cotton saree with spectacles",
    "COLLEAGUE": "a fellow teacher, a friendly woman in her 40s in a mustard cotton saree",
    "TEAM": "a friendly diverse team of Indian academic professionals, men and women in smart-casual clothes",
    "HOME": "a modest traditional North Indian family house in a small Indian town, flat roof terrace with a low "
            "parapet wall, cream lime-washed walls, teal-painted wooden doors and window grills, a small verandah "
            "with a charpai, potted plants and bougainvillea, a large mango tree, a small duck pond and "
            "a little stream beside it, not European, not Mediterranean, no tiled roof",
    "NEW_HOME": "a cosy modest apartment home with balconies full of potted plants, cream walls, wooden furniture",
}

# Character bible images (made first, then used as references so every episode matches them)
SHEET = [
    ("GIRL6", "{GIRL6}, full body, standing in a garden, three-quarter side view"),
    ("GIRL11", "{GIRL11}, full body, standing on a school path, three-quarter side view"),
    ("WOMAN19", "{WOMAN19}, full body, standing in a college corridor, three-quarter side view"),
    ("WOMAN22", "{WOMAN22}, full body, standing in a sunlit room holding books, three-quarter side view"),
    ("BRIDE", "{BRIDE}, full body, standing in a courtyard decorated with string lights, seen from the side"),
    ("WIFE", "{WIFE}, full body, standing in a kitchen doorway of {NEW_HOME}, three-quarter side view"),
    ("MOTHER", "{MOTHER}, full body, standing in a cosy living room, three-quarter side view"),
    ("TEACHER", "{TEACHER}, full body, standing in a bright classroom, three-quarter side view"),
    ("TRAINER", "{TRAINER}, full body, standing at a home desk with a laptop, three-quarter side view"),
    ("DESIGNER", "{DESIGNER}, full body, standing in a modern office, three-quarter side view"),
    ("FOUNDER", "{FOUNDER}, full body, standing in a bright modern workspace, three-quarter side view"),
    ("AMMI", "{AMMI}, full body, standing in a warm kitchen, three-quarter side view"),
    ("AMMI_OLDER", "{AMMI_OLDER}, full body, sitting on a sofa, three-quarter side view"),
    ("ABBU", "{ABBU}, full body, standing at the small iron garden gate of {HOME} at blue-hour dusk, "
             "three-quarter side view"),
    ("CHILDREN", "two Indian siblings only, no adults: {DAUGHTER} and {SON} standing side by side holding hands "
                 "in a cosy Indian home playroom with toys and a window, full body, three-quarter view"),
    ("HOME", "high-angle wide storybook view of {HOME} at blue-hour dusk, warm yellow light glowing from every "
             "window, deep blue evening sky, birds flying home"),
]
REFS = {name: f"work/EduCrew_Characters/keyframes/shot{i:02d}.png" for i, (name, _) in enumerate(SHEET, 1)}

VOICES = {
    # the same narrator in all 10 episodes; she is also the adult woman's speaking voice
    "NARRATOR": "Mary speaks in a warm, natural, expressive and conversational tone at a moderate pace, like a woman "
                "telling her own life story. The recording is very clear and close-up, with no background noise.",
    "WOMAN": "Mary speaks in a bright, natural and friendly conversational tone at a moderate pace. "
             "The recording is very clear, with no background noise.",
    "WOMAN_SOFT": "Mary speaks very softly and slowly, almost a whisper, gentle and hopeful. Very clear recording.",
    "GIRL": "A young girl speaks in a high-pitched, playful and cheerful voice at a quick pace. Very clear recording.",
    "GIRL_HI": "Divya speaks like a little girl, in a high-pitched, playful voice at a quick pace. Very clear recording.",
    "AMMI_HI": "Divya speaks softly and warmly, calling out affectionately at a relaxed pace. Very clear recording.",
    "AMMI": "Swapna speaks in a warm, gentle, motherly tone at a slow pace. Very clear recording.",
    "ABBU_HI": "Rohit speaks in a warm, calm and cheerful deep voice at a relaxed pace. Very clear recording.",
    "TEACHER_SCHOOL": "Meera speaks in a clear, kind and slightly formal teacher's voice. Very clear recording.",
    "FRIEND_CHILD": "A young girl speaks excitedly and quickly with a high-pitched voice. Very clear recording.",
    "FRIEND_COLLEGE": "Sneha speaks in a friendly, upbeat and warm voice at a moderate pace. Very clear recording.",
    "FAMILY_MEMBER": "Gauri speaks slowly in a gentle, caring, older woman's voice. Very clear recording.",
    "DAUGHTER": "A little girl about six speaks sweetly in a high-pitched voice. Very clear recording.",
    "SON": "A little boy about four speaks excitedly in a high-pitched voice. Very clear recording.",
    "CHILDREN": "Two young children call out together, excited and happy, high-pitched. Very clear recording.",
    "STUDENT": "A young boy about ten speaks politely and curiously. Very clear recording.",
    "COLLEAGUE": "Nisha speaks in a warm, friendly voice at a moderate pace. Very clear recording.",
    "PARTICIPANT": "Aakash speaks in a curious, polite voice, slightly distant as if on a video call.",
    "PARTICIPANT2": "Priya speaks in a pleased, appreciative voice, slightly distant as if on a video call.",
    "TEAM_MEMBER": "Kabir speaks in a confident, friendly professional voice. Very clear recording.",
    "COLLEAGUE2": "Riya speaks in a crisp, cheerful professional voice. Very clear recording.",
}


def N(text):
    return {"speaker": "NARRATOR", "text": text}


def L(speaker, text, tts=None):
    d = {"speaker": speaker, "text": text}
    if tts:
        d["tts_text"] = tts  # same words, spelt so the voice model pronounces them correctly
    return d


def S(image, motion, sfx, lines=(), ref=None):
    return {"image": image, "motion": motion, "sfx": sfx + ", no music", "lines": list(lines), "ref": ref}


EPISODES = [
    # ------------------------------------------------------------------ 1
    ("A Little World of Happiness", "GIRL6", [
        S("high-angle wide storybook view of {HOME} at blue-hour dusk, the large mango tree's leafy canopy framing the top, "
          "warm lights glowing in every window, a little stream with ducks flowing through the foreground, hens in the yard, "
          "a cat on the roof, washing on a clothesline, family members small in the scene, distant green fields and hills",
          "almost still camera with a very slow push-in, water flowing, ducks gliding, leaves swaying, birds flying home",
          "soft evening birds, leaves rustling, gentle flowing stream, ducks",
          [N("My story began in a simple, happy home.")], ref="HOME"),
        S("{GIRL6} chasing butterflies in the front garden of {HOME}, ducks by the pond, seen from behind",
          "the girl runs and twirls after a butterfly, tracking camera at child height", "children's laughter, birds, ducks quacking",
          [N("We were an ordinary middle-class Indian Muslim family, but our home was full of warmth.")]),
        S("{AMMI} cooking at the stove in a warm kitchen with steel utensils, {GIRL6} beside her helping roll dough, side view",
          "steam rises from the pot, the mother stirs, the girl rolls a small roti, gentle push-in",
          "sizzling pan, steel utensils, glass bangles clinking",
          [N("We didn't have everything, but we never felt that something was missing.")], ref="AMMI"),
        S("{GIRL6} sitting on the courtyard steps watching colourful birds in the mango tree, {DADI} smiling nearby, seen from behind",
          "birds hop between branches, the girl points up, slow tilt up into the tree", "birdsong, leaves, distant household sounds",
          [N("Family meals, little games, familiar voices and the love of my parents made my childhood special.")]),
        S("{AMMI} standing in the glowing doorway of {HOME} calling towards the garden at dusk, seen from the side",
          "the mother waves her hand to call the child inside, warm light spilling out", "evening crickets, door creak",
          [L("AMMI_HI", "Aa jao beta, khana tayyar hai!", "आ जाओ बेटा, खाना तैयार है!")], ref="AMMI"),
        S("{GIRL6} and {BHAI} playing with a small ball in the garden at dusk, the girl turning her head towards the house",
          "the girl holds up one finger towards the house and keeps playing", "children playing, ball bouncing, crickets",
          [L("GIRL_HI", "Ammi, bas ek minute!", "अम्मी, बस एक मिनट!")]),
        S("{ABBU} opening the small garden gate of {HOME} at dusk carrying a cloth bag, greeting the family with a "
          "gentle salaam gesture, seen from behind", "the father walks up the path, the girl runs to hug him",
          "gate creak, footsteps on gravel, happy giggle", [], ref="ABBU"),
        S("the family sitting together on a dastarkhwan floor cloth with steel plates of halal food, {ABBU}, {AMMI}, "
          "{DADI}, {BHAI} and {GIRL6}, warm lamp light, seen from a gentle high angle", "hands pass bowls, everyone settles to eat",
          "plates and spoons clinking, soft family murmur",
          [L("ABBU_HI", "Chalo, sab saath mein khana khate hain.", "चलो, सब साथ में खाना खाते हैं।")], ref="ABBU"),
        S("{GIRL6} at night sitting on the floor of her cosy room beside a small stack of schoolbooks, a folded prayer mat "
          "and a Quran resting on a wooden stand on a high shelf, soft lamp light, seen from the side",
          "the girl touches the books curiously", "quiet night crickets, ceiling fan hum",
          [N("Back then, I had no idea what life had planned for me.")]),
        S("close view of the little stack of schoolbooks beside {GIRL6}'s small hands, warm lamp glow",
          "the camera slowly moves towards the books", "quiet room, a page turning",
          [N("I was simply enjoying my little world.")]),
    ]),
    # ------------------------------------------------------------------ 2
    ("Not the Topper, but a Dreamer", "GIRL11", [
        S("the same stack of schoolbooks in morning light, {GIRL11} picking them up, close view", "morning light grows, she lifts the books",
          "morning birds, books being picked up", [N("I was never the class topper.")]),
        S("{AMMI} braiding {GIRL11}'s hair with red ribbons in the courtyard of {HOME} before school, seen from behind",
          "the mother ties the ribbon, the girl adjusts her school bag", "fabric rustle, birds, kitchen sounds",
          [N("I was an ordinary student, learning at my own pace, completing homework and preparing for examinations.")], ref="GIRL11"),
        S("{GIRL11} and {FRIEND_SCHOOL} walking to school along a tree-lined street with a cycle rickshaw, seen from behind",
          "they walk swinging their bags, tracking shot", "footsteps, bicycle bell, birds, distant traffic",
          [N("Sometimes I did well, and sometimes I struggled.")]),
        S("a 1990s Indian classroom with wooden desks, a blackboard and ceiling fans, {SCHOOL_TEACHER} at the front, "
          "{GIRL11} at her desk seen from behind", "the teacher walks between desks", "classroom murmur, chalk on blackboard",
          [L("TEACHER_SCHOOL", "Have you completed your homework?")]),
        S("{GIRL11} standing at her desk holding up her notebook, seen from the side", "she shows the notebook politely",
          "pages rustling, quiet classroom", [L("GIRL", "Yes, ma'am. I've tried all the questions.")]),
        S("{GIRL11} looking out of the classroom window at clouds and birds, daydreaming, side view",
          "clouds drift, a bird lands on the window grill", "birds, distant classroom voices",
          [N("But I always had an imagination of my own.")]),
        S("a school playground with a big neem tree, {FRIEND_SCHOOL} running ahead and waving back to {GIRL11}",
          "the friend runs, the girl hurries after her", "school bell, children laughing, running footsteps",
          [L("FRIEND_CHILD", "Come on! Let's go and play."), L("GIRL", "Wait for me!")]),
        S("{GIRL11} doing homework at a small wooden desk at home in the evening under a table lamp, seen from behind",
          "her pencil writes, she pauses and looks up thoughtfully", "pencil writing, pages turning, crickets",
          [N("I used to wonder what I would become when I grew up.")]),
        S("{GIRL11} on the rooftop of {HOME} at sunset looking at the sky, kites far away, seen from behind",
          "her plaits move in the breeze, slow push-in", "wind, distant birds, evening ambience",
          [N("I didn't have all the answers, but I had dreams.")]),
        S("{GIRL11} placing her schoolbooks on a table next to a college admission booklet, looking at it curiously, close side view",
          "she slides the booklet towards her, camera moves onto it", "books placed down, page turning",
          [N("And those dreams quietly stayed with me.")]),
    ]),
    # ------------------------------------------------------------------ 3
    ("The Year Everything Began", "WOMAN19", [
        S("a college admission booklet on a table in soft morning light, {WOMAN19}'s hand opening it, close view",
          "the booklet opens, camera rises to her", "page turning, morning birds", [N("Then came 2001.")]),
        S("wide establishing shot of an early-2000s Indian college campus with an old stone building, a big banyan tree and "
          "students with bags, {WOMAN19} walking in through the gate, seen from behind", "she walks through the gate, crane shot",
          "college ambience, footsteps, birds", [N("College opened a completely new chapter in my life.")]),
        S("{WOMAN19} walking down an arched college corridor, {FRIEND_COLLEGE} joining her, seen from behind",
          "the friend catches up and they walk together", "footsteps echoing, students chatting",
          [N("I met new people, experienced new challenges and began understanding myself better.")]),
        S("a college lecture hall with wooden benches, {WOMAN19} writing notes, side view", "she writes, raises her hand",
          "lecture murmur, pen writing", [N("Slowly, I became more confident.")]),
        S("{WOMAN19} studying in a college library between tall bookshelves, sunlight through high windows, side view",
          "she turns pages, dust glints in the light", "pages turning, quiet library",
          [N("I realised that I could learn, grow and take responsibility for my future.")]),
        S("{WOMAN19} and {FRIEND_COLLEGE} sitting on the campus lawn under a tree, the friend turning to her, side view",
          "leaves fall gently, the friend asks with a smile", "birds, light breeze, distant students",
          [L("FRIEND_COLLEGE", "So, what do you want to become?")], ref="FRIEND_COLLEGE"),
        S("{WOMAN19} sitting under the tree hugging her books, looking into the distance thoughtfully, side view",
          "she answers with a hopeful shrug", "breeze, birds",
          [L("WOMAN", "I want to do something meaningful. I just haven't figured out exactly what yet.")]),
        S("{FRIEND_COLLEGE} placing a reassuring hand on {WOMAN19}'s shoulder under the tree, seen from behind",
          "the friend pats her shoulder, both smile", "breeze, birds", [L("FRIEND_COLLEGE", "You'll find your way.")]),
        S("{WOMAN19} walking home at sunset along a small stream with reflections, seen from behind",
          "water flows and sparkles, ducks swim", "flowing stream, evening birds, footsteps",
          [N("I was still discovering what I wanted to become, but one thing was changing.")]),
        S("{WOMAN19} at night studying a thick law book with interest at her desk, lamp light, close side view",
          "she turns a page, the camera settles on the book", "page turning, crickets",
          [N("I had started believing in myself.")]),
    ]),
    # ------------------------------------------------------------------ 4
    ("The Dream That Took Another Road", "WOMAN22", [
        S("a stack of law books and legal notes on a desk, {WOMAN22} reading eagerly, side view", "she highlights a line",
          "pages, pen scratching", [N("I once dreamed of becoming a criminal lawyer.")]),
        S("dreamlike scene: {WOMAN22} wearing a black lawyer's coat over her modest clothes standing in a grand wooden "
          "courtroom, soft glowing light, seen from behind", "she steps forward confidently, soft dreamy glow",
          "quiet courtroom echo, footsteps", [N("I imagined studying law, standing in court and fighting for what was right.")]),
        S("{WOMAN22} back at her desk hugging a law book and smiling, warm afternoon light, side view",
          "she hugs the book, curtains move in the breeze", "breeze, birds outside",
          [N("It was a dream I genuinely loved.")]),
        S("{AMMI_OLDER} sitting in the living room of {HOME} looking up kindly as {WOMAN22} enters, side view",
          "the mother pats the sofa beside her", "household ambience, footsteps",
          [N("But my mother had a different wish for my future.")], ref="AMMI_OLDER"),
        S("{AMMI_OLDER} and {WOMAN22} sitting together on the sofa, the mother holding her daughter's hand, side view",
          "gentle hand squeeze, warm light", "soft room tone, clock ticking", [N("She wanted me to pursue teaching.")], ref="AMMI_OLDER"),
        S("close view of {AMMI_OLDER} speaking gently to {WOMAN22}, seen over the daughter's shoulder", "the mother speaks softly",
          "quiet room", [L("AMMI", "Beta, I feel teaching would be a good path for you.")], ref="AMMI_OLDER"),
        S("{WOMAN22} nodding respectfully to her mother, seen from the side", "she nods and smiles",
          "quiet room", [L("WOMAN", "Theek hai, Ammi. I'll give it my best.", "ठीक है, अम्मी. I'll give it my best.")]),
        S("{AMMI_OLDER} hugging {WOMAN22} warmly in the living room, seen from the side", "a warm hug",
          "fabric rustle, birds outside", [L("AMMI", "I'm sure you'll do well.")], ref="AMMI_OLDER"),
        S("{WOMAN22} placing her law books neatly on a high shelf and taking down teaching books, seen from behind",
          "she slides the law books onto the shelf and takes new books", "books sliding, footsteps",
          [N("I chose to respect her decision and took another road.")]),
        S("{WOMAN22} opening teaching books and a fresh lesson notebook at a sunny window desk, birds on the sill, side view",
          "she writes the first line, birds hop", "pen writing, birds",
          [N("I didn't know it then, but this new direction would eventually shape the person I would become.")]),
    ]),
    # ------------------------------------------------------------------ 5
    ("A Different Kind of Beginning", "WIFE", [
        S("the lesson notebook closing on the desk, warm afternoon light, close view", "the notebook closes gently",
          "notebook closing, birds", [N("Life moved forward, and marriage brought a new home, new relationships and new responsibilities.")]),
        S("a graceful Indian Muslim nikah in a courtyard with string lights, roses and jasmine, {BRIDE} sitting modestly "
          "beside {GROOM}, family around, seen from behind", "fairy lights twinkle, family members smile",
          "soft crowd murmur, bangles, gentle laughter", [N("Everything was different.")], ref="BRIDE"),
        S("{WIFE} arriving at {NEW_HOME} carrying a suitcase, looking around, seen from behind", "she steps inside",
          "door opening, footsteps, suitcase wheels",
          [N("I was learning to adjust, to manage a home and to understand a new phase of life.")]),
        S("{IN_LAW} welcoming {WIFE} in the living room of {NEW_HOME}, side view", "she places a hand on her shoulder",
          "soft room tone", [L("FAMILY_MEMBER", "Are you comfortable here?")]),
        S("{WIFE} smiling and nodding to {IN_LAW}, side view", "she nods warmly", "soft room tone",
          [L("WOMAN", "Yes, Alhamdulillah. I'm slowly settling in.")]),
        S("{WIFE} busy in the kitchen of {NEW_HOME} cooking and arranging steel containers, side view",
          "she moves quickly between pots", "utensils, sizzling pan, footsteps",
          [N("My professional dreams slowly moved into the background.")]),
        S("a wooden shelf holding her teaching books and lesson notebook, {WIFE}'s hand gently touching the spines, close view",
          "her fingers rest on the books", "quiet room, clock ticking", [N("But I hadn't forgotten them.")]),
        S("{WIFE} at the balcony of {NEW_HOME} at night looking at the moon over the trees, seen from behind",
          "her dupatta moves in the breeze", "night breeze, crickets",
          [L("WOMAN_SOFT", "One day, I'll return to my dreams.")]),
        S("{WIFE} on the balcony at dawn watching birds fly over green trees, seen from behind", "birds fly past, sky brightens",
          "dawn birds, breeze",
          [N("Somewhere inside me, the girl who wanted to achieve something was still waiting for her moment.")]),
        S("{WIFE}'s hands gently holding a pair of tiny baby shoes in a newly arranged child's room with a wooden crib",
          "she places the shoes beside the crib", "soft room tone", []),
    ]),
    # ------------------------------------------------------------------ 6
    ("Two Little Worlds", "MOTHER", [
        S("the pair of tiny baby shoes beside the crib in morning light, close view", "sunlight moves across the shoes",
          "morning birds", [N("Then came two little worlds of their own: my daughter and my son.")]),
        S("{MOTHER} cradling a newborn baby in a cosy sunlit room, a toddler girl in pink beside her, side view",
          "she rocks the baby gently", "baby cooing, soft room tone", [N("They changed the meaning of my life.")]),
        S("{MOTHER} feeding two toddlers at a small table, food on their cheeks, laughter, side view",
          "the children giggle and reach for the spoon", "children laughing, spoons on plates",
          [N("Their little hands, their endless questions, their laughter and their everyday adventures became my greatest happiness.")]),
        S("{DAUGHTER} at a small desk with a colouring book looking up, seen from the side", "she holds up her pencil",
          "pencil on paper", [L("DAUGHTER", "Mumma, can you help me?")], ref="CHILDREN"),
        S("{SON} running into the room holding up a paper boat craft", "he runs in excitedly", "running footsteps, paper rustle",
          [L("SON", "Mumma! Look what I made!")], ref="CHILDREN"),
        S("{MOTHER} kneeling between {DAUGHTER} and {SON}, laughing, seen from the side", "she opens her arms to both",
          "children giggling", [L("WOMAN", "One at a time! Let me see both.")]),
        S("{DAUGHTER} and {SON} hugging {MOTHER} together in the living room, seen from behind", "a big group hug",
          "children laughing",
          [L("CHILDREN", "Mumma!"), N("I watched them grow, helped them learn and celebrated their smallest achievements.")]),
        S("busy school morning: {MOTHER} packing two school bags and tiffins as {DAUGHTER} and {SON} wait at the door",
          "she zips the bags and hands them over", "zips, footsteps, morning birds",
          [N("I was their mother, their guide and their biggest cheerleader.")]),
        S("{MOTHER} reading a bedtime story to {DAUGHTER} and {SON} tucked in bed, warm lamp glow, side view",
          "she turns a page, the children's eyes close", "page turning, quiet night",
          [N("And while I was helping them discover the world,")]),
        S("{MOTHER} looking at an old classroom photograph and her teaching notebook while {DAUGHTER} and {SON} play "
          "on the floor nearby, seen over her shoulder", "she smiles at the notebook", "children playing softly, toy blocks",
          [N("I was quietly preparing to rediscover mine.")]),
    ]),
    # ------------------------------------------------------------------ 7
    ("The Classroom Door Opens Again", "TEACHER", [
        S("her teaching notebook on a table in morning light, close view", "the notebook pages flutter in a breeze",
          "morning birds, pages", [N("By 2015, life had taken another turn.")]),
        S("{TEACHER} walking calmly along a leafy lane with {DAUGHTER11} and {SON9} in school uniforms, seen from behind",
          "they walk together peacefully, morning light", "footsteps, birds, distant traffic",
          [N("After my separation, I made a decision that changed my professional journey.")]),
        S("{TEACHER} walking through a cheerful school gate with flower beds and a big tree, seen from behind",
          "she walks in with confidence", "school bell, children chatting",
          [N("I happily stepped into a classroom as a teacher.")]),
        S("{TEACHER} opening a classroom door, sunlight pouring in, seen from behind", "the door swings open into light",
          "door opening, children's voices", [N("It felt like opening a door I had left closed for years.")]),
        S("{TEACHER} teaching at a whiteboard to a bright classroom of students of different ages, side view",
          "she points at the board, students raise hands", "marker on whiteboard, classroom ambience",
          [N("I began teaching different grade levels, preparing lessons and helping students understand new ideas.")]),
        S("a schoolboy raising his hand at his desk, {TEACHER} walking towards him, seen from behind the boy",
          "the boy raises his hand", "classroom murmur", [L("STUDENT", "Ma'am, can you explain this once again?")]),
        S("{TEACHER} kneeling beside the student's desk explaining with colourful blocks, side view",
          "she arranges the blocks, he nods", "blocks clicking", [L("WOMAN", "Of course! Let's try it in a different way.")]),
        S("a sunny school staff room, {COLLEAGUE} handing {TEACHER} a cup of tea, side view", "they chat warmly",
          "tea cups, soft chatter",
          [L("COLLEAGUE", "How was your first day?"), L("WOMAN", "It felt wonderful. I think I'm right where I belong.")]),
        S("{TEACHER} walking through the school garden past a big tree, students playing nearby, seen from behind",
          "leaves fall, birds fly", "children playing, birds", [N("Slowly, I found my confidence again.")]),
        S("{TEACHER} at home arranging teaching materials and colourful flashcards beside a laptop, side view",
          "she opens the laptop, its glow lights her", "papers shuffling, laptop opening",
          [N("This time, I was ready to build something of my own.")]),
    ]),
    # ------------------------------------------------------------------ 8
    ("Beyond the Classroom", "TRAINER", [
        S("an open laptop beside neat teaching materials in morning light, close view", "the screen wakes up",
          "laptop chime, morning birds", [N("Then came 2020.")]),
        S("{TRAINER} at a beautiful home workspace with plants, bookshelves and a window onto a green garden, side view",
          "she adjusts her glasses and starts typing", "keyboard typing, birds outside",
          [N("The classroom was no longer the only place where I could teach.")]),
        S("{TRAINER} leading an online workshop, her laptop showing a grid of small video windows of educators, seen over her shoulder",
          "she waves to the participants", "online meeting chime, keyboard",
          [N("I began conducting online training workshops for people in the education field.")]),
        S("{TRAINER} preparing colourful presentation slides and notes at her desk, side view", "she arranges slides and writes notes",
          "mouse clicks, pen writing", [N("I was sharing ideas, explaining strategies and helping other educators grow.")]),
        S("a laptop screen showing a teacher on a video call raising his hand, {TRAINER} watching, seen over her shoulder",
          "the participant raises his hand", "video call ambience",
          [L("PARTICIPANT", "Could you show us a practical example?")]),
        S("{TRAINER} smiling and pointing to a whiteboard behind her during the video call, side view",
          "she turns to the whiteboard", "marker squeak", [L("WOMAN", "Absolutely. Let's work through it together.")]),
        S("the laptop screen showing educators nodding happily in their video windows", "participants nod and smile",
          "video call ambience", [L("PARTICIPANT2", "That makes it much clearer.")]),
        S("{TRAINER} at the window at dawn holding a cup of tea, birds flying over green trees, seen from behind",
          "birds fly past, light grows", "dawn birds, gentle breeze", [N("Technology opened new doors for me.")]),
        S("{TRAINER} in front of a large screen showing many educators from different cities in small windows, seen from behind",
          "more windows light up one by one", "soft notification sounds, keyboard",
          [N("I realised that teaching could reach people far beyond one classroom.")]),
        S("{TRAINER} working on curriculum documents, assessment sheets and digital learning materials spread across her desk, close side view",
          "she highlights a document", "pages turning, keyboard",
          [N("My journey was becoming bigger, and I was ready to learn even more.")]),
    ]),
    # ------------------------------------------------------------------ 9
    ("The Reinvention", "DESIGNER", [
        S("curriculum documents and colourful assessment sheets on a desk, {DESIGNER}'s hands arranging them, close view",
          "she stacks the documents", "papers shuffling", [N("From 2022, my journey entered a completely new phase.")]),
        S("{DESIGNER} walking into a bright modern office with plants and large windows, seen from behind",
          "she walks to her desk with a laptop bag", "office ambience, footsteps",
          [N("I moved into full-fledged instructional design and curriculum development.")]),
        S("{DESIGNER} at a large planning wall covered with colourful sticky notes and storyboard cards, side view",
          "she moves a sticky note and connects ideas", "sticky notes, marker",
          [N("I began working on curriculum mapping, assessment development, storyboarding and academic strategy.")]),
        S("{DESIGNER} at a desk with several screens showing colourful maths diagrams, reading materials and science "
          "illustrations, seen over her shoulder", "she switches between screens", "keyboard typing, mouse clicks",
          [N("My projects expanded across Mathematics, English Language Arts and Science.")]),
        S("{DESIGNER} leading a meeting around a table with {TEAM}, documents and laptops, side view",
          "she gestures as people discuss", "meeting murmur, pages",
          [N("I started leading and coordinating subject matter experts and contributing to College and Career Readiness projects.")]),
        S("a team member at the meeting table pointing at an assessment document, {DESIGNER} listening, side view",
          "he points at the document", "pages turning", [L("TEAM_MEMBER", "Should we map the assessment against the standards?")]),
        S("{DESIGNER} nodding and tapping the document thoughtfully, side view", "she taps the page",
          "pen tapping", [L("WOMAN", "Yes. Every question needs a clear learning purpose.")]),
        S("a colleague handing {DESIGNER} a printed document across the table, both smiling, side view",
          "she takes the document", "paper handed over",
          [L("COLLEAGUE2", "The revised version is ready."), L("WOMAN", "Wonderful. Let's review it together.")]),
        S("{DESIGNER} reviewing a storyboard on a tablet, warm afternoon light, side view", "she swipes through storyboard frames",
          "tablet taps, office ambience", [N("I was no longer just creating lessons.")]),
        S("{DESIGNER} working with a small team around a table, camera widening to reveal a collaborative academic workspace",
          "the camera slowly pulls back and widens", "office ambience, soft conversation",
          [N("I was helping design meaningful learning experiences.")]),
    ]),
    # ------------------------------------------------------------------ 10
    ("From One Classroom to Many", "FOUNDER", [
        S("a collaborative academic workspace, {FOUNDER} standing at the head of a table looking at her team, seen from behind",
          "she looks around warmly", "office ambience, typing",
          [N("Today, the little girl who once had big dreams leads academic projects of her own.")]),
        S("wide establishing shot of a lively, beautiful modern academic workspace with plants, sunlight and {TEAM} "
          "collaborating, {FOUNDER} walking through", "tracking shot following her", "typing, footsteps, soft conversation",
          [N("Through EduCrew, I work with a team that brings together curriculum development, instructional design, "
             "assessments and academic expertise.")]),
        S("shelves and desks full of colour-coded textbooks, binders and curriculum folders for different school boards, "
          "{FOUNDER} pulling out a folder, side view", "she flips through a binder", "pages turning, binder clicks",
          [N("From CBSE and ICSE to IB, US and UK curricula, our work reaches far beyond one classroom.")]),
        S("{FOUNDER} reviewing documents with two team members at a standing desk, side view", "they point and discuss",
          "pages, soft conversation", [N("My journey began with a dream.")]),
        S("{FOUNDER} looking at a large screen showing colourful digital learning materials, seen from behind",
          "materials scroll on the screen", "mouse clicks, keyboard",
          [N("Today, I am helping create learning opportunities for many.")]),
        S("a team member turning to {FOUNDER} with a laptop at the meeting table, side view", "he looks up eagerly",
          "office ambience", [L("TEAM_MEMBER", "Are we ready for the next project?")]),
        S("{FOUNDER} smiling and closing a folder confidently, side view", "she closes the folder and stands",
          "folder closing", [L("WOMAN", "We are. Let's build something meaningful together.")]),
        S("{FOUNDER} and her team gathering around the table, hands stacked together in the middle, seen from above",
          "hands come together in a team stack", "soft laughter",
          [L("TEAM_MEMBER", "EduCrew?"), L("WOMAN", "EduCrew.")]),
        S("{FOUNDER} at a large window looking out at green trees and the city beyond, birds flying, seen from behind",
          "birds fly past, light glows", "birds, soft office ambience", [N("And this is only the beginning.")]),
        S("{FOUNDER} and the whole team working together in the beautiful animated academic workspace, camera slowly moving "
          "back to reveal the entire team and environment", "slow pull-back crane shot", "office ambience, footsteps, typing",
          [N("EduCrew Academic Solutions. Building learning, one idea at a time.")]),
    ]),
]


def speech_seconds(lines):
    return sum(len(l["text"].split()) / 2.4 + 0.5 for l in lines)


def finish(shots, total=60.0):
    """Give every shot enough time for its words, then share the rest so the episode is exactly `total` seconds."""
    need = [max(4.5, speech_seconds(s["lines"]) + 1.2) for s in shots]
    if sum(need) > total:
        print(f"  ! speech needs {sum(need):.0f}s, more than {total:.0f}s")
    extra = max(0.0, total - sum(need)) / len(shots)
    durs = [round(n + extra, 1) for n in need]
    durs[-1] = round(total - sum(durs[:-1]), 1)
    for i, (s, d) in enumerate(zip(shots, durs), 1):
        s["id"], s["duration"] = i, d
        for line in s["lines"]:
            line["at"] = 0.6
    return shots


def main():
    os.makedirs(EP_DIR, exist_ok=True)
    common = {"width": 720, "height": 1280, "fps": 24, "logo": "logo/educrew_logo.png", "logo_width": 0.18, "style": STYLE,
              "negative": NEGATIVE, "characters": CHARACTERS, "voices": VOICES, "refs": REFS}
    sheet = dict(common, title="EduCrew Character Bible", episode=0,
                 shots=[{"id": i, "duration": 3, "image": img, "motion": "", "sfx": "", "lines": []}
                        for i, (_, img) in enumerate(SHEET, 1)])
    sheet.pop("refs")
    json.dump(sheet, open(os.path.join(EP_DIR, "EduCrew_Characters.json"), "w"), indent=1, ensure_ascii=False)

    for n, (title, main_ref, shots) in enumerate(EPISODES, 1):
        assert len(shots) == 10, title
        for s in shots:
            s["ref"] = s["ref"] or main_ref
        finish(shots)
        if n > 1:  # pick up exactly where the previous episode ended
            shots[0]["continue_from"] = f"work/EduCrew_Biography_Episode_{n - 1:02d}/keyframes/shot10.png"
            shots[0]["continue_strength"] = 0.65
        ep = dict(common, title=title, episode=n, shots=shots)
        if n == 10:
            ep["brand_reveal"] = {"seconds": 5, "width": 0.6}
        name = f"EduCrew_Biography_Episode_{n:02d}"
        json.dump(ep, open(os.path.join(EP_DIR, name + ".json"), "w"), indent=1, ensure_ascii=False)
        words = sum(len(l["text"].split()) for s in shots for l in s["lines"])
        print(f"{name}: {title} | {sum(s['duration'] for s in shots):.1f}s | {words} spoken words")


if __name__ == "__main__":
    main()
