# 🎵 Music Recommender Simulation

## Project Summary

This project allows users to define their own music preferences and tastes. Then, it loads songs from a predefined dataset and determines which ones most closely match the user preferences. The program then displays the top-k songs to the user with a brief explanation for each choice.

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

Every song starts at 0 points, and each rule below adds to its score. Songs are ranked by total score (highest first) and the top k are returned, each with a short reason built from the rules that fired.

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

====================================================================
  TOP RECOMMENDATIONS for {'genre': 'pop', 'mood': 'sad', 'energy': 0.9}
====================================================================
  1. Gym Hero — Max Pulse
     Score: +3.46  (genre=pop, mood=intense, energy=0.93)
     Why:
       • matches your favorite genre (pop)
       • energy 0.93 is close to your target 0.9

  2. Sunrise City — Neon Echo
     Score: +3.38  (genre=pop, mood=happy, energy=0.82)
     Why:
       • matches your favorite genre (pop)
       • energy 0.82 is close to your target 0.9

  3. Storm Runner — Voltline
     Score: +1.48  (genre=rock, mood=intense, energy=0.91)
     Why:
       • energy 0.91 is close to your target 0.9

  4. Voltage Rush — Pulse Theory
     Score: +1.43  (genre=edm, mood=energetic, energy=0.95)
     Why:
       • energy 0.95 is close to your target 0.9

  5. Iron Verdict — Ashfall
     Score: +1.38  (genre=metal, mood=angry, energy=0.98)
     Why:
       • energy 0.98 is close to your target 0.9

====================================================================
  TOP RECOMMENDATIONS for {'genre': 'edm', 'mood': 'energetic', 'energy': 2.0}
====================================================================
  1. Voltage Rush — Pulse Theory
     Score: +2.92  (genre=edm, mood=energetic, energy=0.95)
     Why:
       • matches your favorite genre (edm)
       • matches your mood (energetic)
       • energy 0.95 is close to your target 2.0

  2. Iron Verdict — Ashfall
     Score: -0.03  (genre=metal, mood=angry, energy=0.98)
     Why:
       • energy 0.98 is close to your target 2.0

  3. Gym Hero — Max Pulse
     Score: -0.10  (genre=pop, mood=intense, energy=0.93)
     Why:
       • energy 0.93 is close to your target 2.0

  4. Storm Runner — Voltline
     Score: -0.13  (genre=rock, mood=intense, energy=0.91)
     Why:
       • energy 0.91 is close to your target 2.0

  5. Sunrise City — Neon Echo
     Score: -0.27  (genre=pop, mood=happy, energy=0.82)
     Why:
       • energy 0.82 is close to your target 2.0

====================================================================
  TOP RECOMMENDATIONS for {'genre': 'folk', 'mood': 'nostalgic', 'energy': 0.95, 'likes_acoustic': True}
====================================================================
  1. Dust and Roads — Hollow Pine
     Score: +4.23  (genre=folk, mood=nostalgic, energy=0.44)
     Why:
       • matches your favorite genre (folk)
       • matches your mood (nostalgic)
       • energy 0.44 is close to your target 0.95
       • it's acoustic, which you like

  2. Voltage Rush — Pulse Theory
     Score: +1.50  (genre=edm, mood=energetic, energy=0.95)
     Why:
       • energy 0.95 is close to your target 0.95

  3. Gym Hero — Max Pulse
     Score: +1.47  (genre=pop, mood=intense, energy=0.93)
     Why:
       • energy 0.93 is close to your target 0.95

  4. Iron Verdict — Ashfall
     Score: +1.46  (genre=metal, mood=angry, energy=0.98)
     Why:
       • energy 0.98 is close to your target 0.95

  5. Storm Runner — Voltline
     Score: +1.44  (genre=rock, mood=intense, energy=0.91)
     Why:
       • energy 0.91 is close to your target 0.95
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran.

I ran an experiment where I switched off the mood metric, and found out that the top-five order did not change. This showed that mood has little effect on the score, although this can be explained by the very small size of the data.

---

## Limitations and Risks

Summarize some limitations of your recommender.

The model only scores genre, mood, energy, and acoustic-ness, so other features in the dataset are ignored entirely. The catalog is also thin and uneven — most genres and moods appear only once — and because genre and mood are matched by exact strings, a fan of a single-song genre sees that same song ranked first every time while near-identical labels like "pop" and "indie pop" earn no credit for each other.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

My biggest learning moment was seeing how one bad energy value could break the whole list and turn scores negative. It showed me how fragile scoring can be and how much small choices matter. AI tools helped me test tricky profiles quickly and spot patterns I might have missed. But I still had to double-check the outputs by hand, since the tool could explain a result without noticing it was actually unfair or wrong. What surprised me most was how a few simple points and rules could still "feel" like real recommendations, since the "Why" reasons made the results seem smart. If I extended this project, I would score more features like danceability and tempo, match similar genres, and add more low-energy songs to balance the data.



