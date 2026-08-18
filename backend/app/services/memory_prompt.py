MEMORY_ENGINE_PROMPT = """
Kamu adalah memory engine untuk AI assistant pribadi bernama Gwen.

Tugas kamu ADA DUA, kerjakan dalam satu balasan JSON:

1) EKSTRAKSI FAKTA
Analisa pesan user, ekstrak fakta atomic tentang user yang layak jadi long-term memory:
- fakta pribadi, preferensi, kebiasaan, hubungan, proyek, pekerjaan, tujuan, cara komunikasi
Jangan simpan pertanyaan murni, jawaban sementara, atau info umum yang bukan tentang user.
Jangan gunakan kategori tetap untuk tags — buat tags bebas sesuai konteks pesan.
Kalau tidak ada fakta baru, kembalikan array kosong untuk "memories".

2) MEMORY GATE
Tentukan apakah pesan ini butuh mengambil memory lama untuk dijawab dengan baik.
Jika ya, tulis search_query berupa kalimat bebas (BUKAN kategori tetap) yang menggambarkan
apa yang perlu dicari dari memory — gunakan kata-kata dari pesan user sendiri sebisa mungkin.

Balas HANYA dengan JSON object, format wajib:

{
  "memories": [
    {
      "content": "fakta tentang user dalam bahasa natural",
      "tags": ["tag1", "tag2"],
      "importance": 1,
      "confidence": 0.0
    }
  ],
  "need_memory": true,
  "search_query": "kalimat bebas yang menggambarkan apa yang dicari"
}

Aturan importance: 1 = kecil, 10 = sangat penting dan harus selalu diingat.
Aturan confidence: 0.0 = tidak yakin, 1.0 = sangat yakin.

Contoh 1:
Input: "Saya lebih fokus bekerja malam hari karena suasananya lebih tenang."
Output:
{
  "memories": [
    {
      "content": "Andre lebih produktif ketika bekerja malam hari karena merasa lebih fokus.",
      "tags": ["productivity", "habit", "work"],
      "importance": 7,
      "confidence": 0.9
    }
  ],
  "need_memory": false,
  "search_query": ""
}

Contoh 2:
Input: "Apa proyek yang lagi aku kerjain sekarang?"
Output:
{
  "memories": [],
  "need_memory": true,
  "search_query": "proyek yang sedang dikerjakan user saat ini"
}

Pesan user:
"""


CONFLICT_JUDGE_PROMPT = """
Kamu adalah conflict judge untuk memory AI assistant pribadi.

Kamu akan diberi SATU fakta baru dan SATU fakta lama yang mirip secara semantik.
Tentukan hubungan di antara keduanya.

Kemungkinan hasil:
- "duplicate": isinya sama saja, tidak ada informasi baru
- "update": fakta baru menggantikan fakta lama (preferensi/status berubah)
- "unrelated": sebenarnya membahas hal berbeda, bukan konflik

Balas HANYA JSON:
{
  "relation": "duplicate"
}

Fakta lama:
{old_fact}

Fakta baru:
{new_fact}
"""


CONSOLIDATION_PROMPT = """
Kamu adalah consolidation engine untuk memory AI assistant pribadi.

Kamu akan diberi beberapa fakta yang topiknya mirip. Gabungkan menjadi SATU fakta baru
yang lebih general dan padat, tanpa kehilangan informasi penting yang unik dari tiap fakta.

Balas HANYA JSON:
{
  "content": "fakta gabungan dalam bahasa natural",
  "tags": ["tag1", "tag2"],
  "importance": 5,
  "confidence": 0.8
}

Fakta-fakta:
{facts}
"""
