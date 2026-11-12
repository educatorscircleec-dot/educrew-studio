# EduCrew: From a Little Dream to a Bigger World. Series bible

The single source of truth is `series/educrew_biography.py`. It defines the characters, voices and style once and writes all 10 episode files from them.
Edit it there, then run `python series/educrew_biography.py`. Don't edit the episode files by hand.

## Look
- High-quality 3D animated storybook film with charming stylized characters and soft, simplified faces. Side views, rear views and expressive body language.
- Rich Indian environments: a traditional home with glowing windows, a mango tree, bougainvillea, a duck pond and stream, birds and butterflies.
- Vertical 9:16, 60 seconds per episode, no music, no subtitles, EduCrew logo bottom-right throughout. Episode 10 ends with a large logo reveal.

## The family: an ordinary, happy, middle-class Indian Muslim family
Modest clothing, salaam, halal family meals, a prayer mat and a Quran respectfully placed in her childhood room. No other religious symbols.

## Her signature at every age
Slim build, warm medium-brown skin, thick black hair, **teal clothes with a mustard-yellow dupatta**.

| Age | Key | Look |
|---|---|---|
| 6 (1990s) | GIRL6 | Two plaits with red ribbons, teal flowered frock, mustard cardigan |
| 11 | GIRL11 | Two long plaits with red ribbons, white uniform with teal dupatta |
| 19 (2001) | WOMAN19 | Side plait, teal salwar kameez, mustard dupatta over head |
| 22 | WOMAN22 | Same as 19, slightly older |
| Wedding | BRIDE | Deep red and gold gharara, dupatta over head |
| 25 | WIFE | Low bun, teal salwar kameez, mustard dupatta |
| 30 | MOTHER | Same, now a mother |
| 2015 | TEACHER | Teal kurta, mustard dupatta, steel watch, handbag |
| 2020 | TRAINER | Adds round reading glasses |
| 2022 | DESIGNER | Adds navy long jacket and ID lanyard |
| Today | FOUNDER | Elegant teal kurta, navy jacket, mustard dupatta, glasses |

Family: AMMI (maroon salwar kameez, mustard dupatta, green bangles; AMMI_OLDER in Episode 4), ABBU (pale blue shirt, trimmed beard, steel watch), DADI, BHAI.
Her children: DAUGHTER (curly ponytail, yellow clip, pink frock) and SON (green t-shirt), shown older in Episode 7.

## Voices
One narrator (`Mary`, Indian English) in all 10 episodes. The adult woman's own lines use the same voice.
Hindi lines (Ammi, Abbu, little girl) are spoken by Hindi voices; they're spelt in Devanagari for pronunciation only, and the words are unchanged.

## How continuity works
1. `EduCrew_Characters.json` makes the reference image for each character and age. Every shot uses its character's reference through IP-Adapter.
2. Shot 1 of each episode starts from the previous episode's last image.
3. Fixed seeds: the same settings give the same result.
