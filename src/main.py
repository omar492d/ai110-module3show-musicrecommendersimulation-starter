"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# Profiles to run through the recommender, including adversarial / edge cases
# designed to try to "trick" the scoring logic.
PROFILES = [
    {"genre": "pop", "mood": "sad", "energy": 0.9},
    {"genre": "edm", "mood": "energetic", "energy": 2.0},
    {"genre": "folk", "mood": "nostalgic", "energy": 0.95, "likes_acoustic": True}
]


def print_recommendations(user_prefs: dict, songs: list) -> None:
    """Run the recommender for one profile and print its top 5 with explanations."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 68)
    print(f"  TOP RECOMMENDATIONS for {user_prefs}")
    print("=" * 68)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score: {score:+.2f}  "
              f"(genre={song['genre']}, mood={song['mood']}, energy={song['energy']})")
        print("     Why:")
        # explanation is a "; "-joined string of reasons; show one per line.
        for reason in explanation.split("; "):
            print(f"       • {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for user_prefs in PROFILES:
        print_recommendations(user_prefs, songs)


if __name__ == "__main__":
    main()
