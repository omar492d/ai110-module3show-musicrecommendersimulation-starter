import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read the CSV at csv_path into a list of song dicts with numeric fields converted."""
    # Columns that hold numbers, so we can do math on them later.
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user_prefs, returning (score, list of reasons that fired)."""
    # Algorithm Recipe (see README): every song starts at 0 and each rule adds points.
    score = 0.0
    reasons: List[str] = []

    # +2.0 — genre matches the user's favorite genre
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"matches your favorite genre ({song['genre']})")

    # +1.0 — mood matches the user's favorite mood
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"matches your mood ({song['mood']})")

    # up to +1.5 — energy closeness, scaled by how near the song is to the target
    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        closeness = 1 - abs(song["energy"] - target_energy)
        energy_points = closeness * 1.5
        score += energy_points
        reasons.append(f"energy {song['energy']} is close to your target {target_energy}")

    # +0.5 — song is acoustic and the user likes acoustic
    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) >= 0.6:
        score += 0.5
        reasons.append("it's acoustic, which you like")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), highest first."""
    # Score every song, building an (song, score, explanation) tuple for each.
    scored = [
        (song, *_score_with_explanation(user_prefs, song))
        for song in songs
    ]

    # Sort highest score first, then keep the top k.
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]


def _score_with_explanation(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Run score_song and turn its list of reasons into one explanation string."""
    score, reasons = score_song(user_prefs, song)
    explanation = "; ".join(reasons) if reasons else "no strong matches"
    return score, explanation
