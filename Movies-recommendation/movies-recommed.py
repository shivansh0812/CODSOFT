import json
from rapidfuzz import process, fuzz

# ---------- LOAD MOVIES ----------

with open("movies.json", "r", encoding="utf-8") as f:
    MOVIES = json.load(f)

ALL_GENRES = sorted({g for m in MOVIES for g in m["genres"]})


# ---------- HELPERS ----------

def fuzzy_match(text, choices):
    match, score, _ = process.extractOne(
        text,
        choices,
        scorer=fuzz.WRatio
    )
    return match if score >= 60 else None


# ---------- RECOMMEND BY MOVIE ----------

def recommend_by_movie(user_movie):
    titles = [m["title"] for m in MOVIES]
    matched_title = fuzzy_match(user_movie, titles)

    if not matched_title:
        print("Kimu: I couldn’t find that movie 😕")
        return

    movie = next(m for m in MOVIES if m["title"] == matched_title)

    print(f"\nKimu: Because you liked {movie['title']}")
    print(f"Kimu: Genres → {', '.join(movie['genres'])}\n")

    scored = []

    for m in MOVIES:
        if m["title"] == movie["title"]:
            continue

        score = len(set(movie["genres"]) & set(m["genres"]))
        if score > 0:
            scored.append((score, m))

    scored.sort(reverse=True, key=lambda x: x[0])

    print("Kimu: You might also enjoy:")
    for i, (_, rec) in enumerate(scored[:5], 1):
        print(f"{i}. {rec['title']} ({', '.join(rec['genres'])})")


# ---------- RECOMMEND BY GENRE ----------

def recommend_by_genre(user_genre):
    matched_genre = fuzzy_match(user_genre, ALL_GENRES)

    if not matched_genre:
        print("Kimu: Hmm, I don’t recognize that genre.")
        print("Kimu: Available genres are:")
        print(", ".join(ALL_GENRES))
        return

    print(f"\nKimu: Got it! Interpreting genre as {matched_genre}\n")

    results = [m for m in MOVIES if matched_genre in m["genres"]]

    print("Kimu: Here are some recommendations:")
    for i, m in enumerate(results[:5], 1):
        print(f"{i}. {m['title']} ({', '.join(m['genres'])})")


# ---------- CHAT LOOP ----------

def show_menu():
    print("""
Kimu: Here’s what I can do 🎬

1️⃣  Recommend movies by movie name  
    (Type: movie or 1)

2️⃣  Recommend movies by genre  
    (Type: genre or 2)

Type 'help' to see this menu again  
Type 'exit' to quit
""")


def main():
    print("Kimu: Hi! I’m Kimu, your movie recommendation assistant 🍿")
    show_menu()

    while True:
        user = input("\nYou: ").lower().strip()

        if user in ["exit", "quit", "bye"]:
            print("Kimu: Enjoy your movies! See you next time 👋")
            break

        elif user in ["1", "movie"]:
            movie = input("Kimu: Tell me a movie you liked: ").strip()
            recommend_by_movie(movie)

        elif user in ["2", "genre"]:
            genre = input("Kimu: Which genre are you in the mood for? ").strip()
            recommend_by_genre(genre)

        elif user in ["help", "menu"]:
            show_menu()

        else:
            print("Kimu: Please choose 1 / 2 or type movie / genre.")
            print("Kimu: Type 'help' to see options again.")


if __name__ == "__main__":
    main()
