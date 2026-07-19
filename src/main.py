"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Header showing the profile we're recommending for.
    print()
    print("=" * 44)
    print("  TOP RECOMMENDATIONS")
    print(
        f"  for genre={user_prefs['genre']}, "
        f"mood={user_prefs['mood']}, energy={user_prefs['energy']}"
    )
    print("=" * 44)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score: {score:.2f}")
        print("     Why:")
        # explanation is a "; "-joined string of reasons; show one per line.
        for reason in explanation.split("; "):
            print(f"       • {reason}")

    print()


if __name__ == "__main__":
    main()
