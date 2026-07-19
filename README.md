# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

Real-world platforms like Spotify and YouTube maainly operate by blending two ideas: collaborative filtering (recommending what similar users liked) and content-based filtering (recommending songs whose attributes match your taste). They learn from huge amounts of behavioral data — likes, skips, replays, and listen time — and combine it with song features like tempo, energy, and mood. My version focuses on the content-based half, since it works from song attributes alone without needing a crowd of users. Each `Song` is scored against a `UserProfile` using a weighted rule that rewards matching genre and mood and gives more points to songs whose energy is close to the user's preference. Genre is weighted highest because it's the most reliable taste signal, with mood, energy, and acousticness refining the result. The scores then rank every song so the top few are returned as recommendations — with a short reason for each.

### Algorithm Recipe

Every song starts at **0 points**, and each rule below adds to its score. Songs are ranked by total score (highest first) and the top *k* are returned, each with a short reason built from the rules that fired.

- **+2.0** — genre matches the user's favorite genre
- **+1.0** — mood matches the user's favorite mood
- **up to +1.5** — energy closeness, scaled as `(1 - |song.energy - target_energy|) * 1.5`
- **+0.5** — song is acoustic (`acousticness >= 0.6`) and the user likes acoustic

Genre is weighted highest because it's the most stable taste signal; energy uses a sliding score rather than match/no-match because it's a number; mood refines the result; and the acoustic bonus acts as a small tie-breaker. The maximum possible score is 5.0. Because genre carries the most weight (+2.0), the system may over-prioritize genre and miss great songs that match the user's mood or energy but sit in a different genre.

**Data Flow**
songs.csv → load_songs (parse rows into song dicts) → recommend_songs → for each song → score_song (+2.0 genre, +1.0 mood, +1.5×energy closeness, +0.5 acoustic) → (score, reasons) → sort by score → top k → main.py prints title, score, and reason

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18

============================================
  TOP RECOMMENDATIONS
  for genre=pop, mood=happy, energy=0.8
============================================

  1. Sunrise City — Neon Echo
     Score: 4.47
     Why:
       • matches your favorite genre (pop)
       • matches your mood (happy)
       • energy 0.82 is close to your target 0.8

  2. Gym Hero — Max Pulse
     Score: 3.30
     Why:
       • matches your favorite genre (pop)
       • energy 0.93 is close to your target 0.8

  3. Rooftop Lights — Indigo Parade
     Score: 2.44
     Why:
       • matches your mood (happy)
       • energy 0.76 is close to your target 0.8

  4. Concrete Kingdom — Vibe Cartel
     Score: 1.50
     Why:
       • energy 0.8 is close to your target 0.8

  5. Night Drive Loop — Neon Echo
     Score: 1.42
     Why:
       • energy 0.75 is close to your target 0.8
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



