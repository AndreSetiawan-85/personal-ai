SEARCH_DOMAINS = {
    "news": [
        "berita",
        "terbaru",
        "hari ini",
        "update",
        "breaking",
        "news",
    ],
    "food": [
        "resep",
        "masak",
        "bahan",
        "menu",
        "makanan",
        "minuman",
    ],
    "travel": [
        "hotel",
        "pesawat",
        "wisata",
        "liburan",
        "travel",
        "tiket",
        "destinasi",
        "jalan-jalan",
    ],
    "shopping": [
        "harga",
        "beli",
        "produk",
        "rekomendasi",
        "murah",
        "terbaik",
        "review",
    ],
    "coding": [
        "python",
        "javascript",
        "error",
        "bug",
        "framework",
        "api",
        "program",
    ],
    "finance": [
        "saham",
        "crypto",
        "investasi",
        "harga dolar",
        "kurs",
    ],
    "health": [
        "obat",
        "gejala",
        "kesehatan",
        "dokter",
    ],
    "entertainment": [
        "film",
        "series",
        "anime",
        "game",
        "musik",
    ],
}


def detect_search_type(message: str):
    text = message.lower()
    scores = {}

    for domain, keywords in SEARCH_DOMAINS.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        scores[domain] = score

    best_domain = max(scores, key=scores.get)

    if scores[best_domain] > 0:
        return best_domain

    return "general"
