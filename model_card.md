# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodMatch 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This model suggests songs that match a person's taste. It takes a few simple preferences, like a favorite genre, a mood, and an energy level. It then returns a short list of top songs with reasons. It assumes the user can describe their taste with these labels. Since the provided data and scoring metrics are limited and simple, the program is intended for exploration and not real users.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The model looks at a few facts about each song. It uses the genre, the mood, and the energy level. It also checks if a song is acoustic. The user gives their favorite genre, mood, and target energy. The model then gives each song points for how well it matches. A genre match is worth the most, then mood, then how close the energy is. It adds up the points and shows the songs with the highest scores.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 18 songs. It covers many genres like pop, lofi, rock, jazz, edm, folk, and metal. It also covers many moods like happy, chill, intense, and nostalgic. Most genres and moods only appear once, so the data is small and uneven. Some parts of taste are missing too, since the songs lean high-energy and there are very few calm, low-energy options.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The model works well for clear, common tastes. A happy pop fan with medium-high energy gets sensible pop songs at the top. It is good at matching a genre and finding songs with a similar energy level. The reasons it shows also make sense and are easy to read. When the user's request is simple and matches the data, the results feel right.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The model only scores genre, mood, energy, and acoustic-ness, so features like tempo, danceability, and valence are ignored entirely, leaving listeners defined by those tastes unrepresented. The catalog is also thin and uneven — most genres and moods appear only once — and because genre and mood are matched by exact strings, a fan of a single-song genre sees that same song ranked first every time while near-identical labels like "pop" and "indie pop" earn no credit for each other. Genre's large weight (+2.0) means the system easily overfits to the one genre a user typed, and my experiment removing the mood check showed the reverse problem: mood is too weak to change the top-5 order at all. The scoring can also quietly favor some users over others, most clearly through the energy gap: because it is calculated as `1 - |song energy - target energy|`, an out-of-range target (e.g. `energy = 2.0`) turns negative and makes songs lose points, and since the catalog leans high-energy (8 of 18 songs above 0.7, only 4 below 0.4), a listener wanting calm, low-energy music can never score a close match and always gets weaker recommendations than a mid-energy listener — a bias that comes from the scoring and dataset rather than the user's taste.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I checked the recommender by running three profiles through it and reading: a high-energy pop fan with a "sad" mood, an EDM fan with an impossible energy value of 2.0, and a folk fan who wants both loud energy (0.95) and acoustic songs. For each one I looked at whether the songs at the top actually fit what the user asked for, whether the "Why" explanations made sense, and whether the scores stayed reasonable. The biggest surprise was that the EDM profile produced mostly negative scores because the out-of-range energy value broke the energy math, and that a calm 0.44-energy folk song still won the folk profile even though the user asked for high energy — which happens because a matching genre, mood, and acoustic bonus together outweigh the energy request. I also ran a before-and-after test where I switched the mood rule off, and the top-five order never changed, which confirmed mood barely matters compared to genre and energy. I also noticed differnces between the outputs of the users: the EDM profile prefers loud high-energy tracks while the folk profile shifts toward a quiet low-energy acoustic song.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would score more features, like danceability, tempo, and how upbeat a song is. I would also match similar genres, so "pop" and "indie pop" can help each other. I would fix the energy math so a bad value cannot make scores go negative. I would add more low-energy songs to balance the catalog. Finally, I would add a way to let users say what they dislike, not just what they like.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned that small scoring choices have a big effect on the results. The weights and the data quietly decide who gets good recommendations. The most surprising part was how one bad energy value could break the whole list. It also surprised me that mood barely mattered compared to genre. Now I see that music apps are full of hidden choices that shape what we hear.
