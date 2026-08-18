# Personal AI Memory Engine - Project Context

## Vision

Membangun personal AI assistant lokal yang mampu memahami user secara berkelanjutan.

Tujuan utama bukan membuat chatbot dengan fitur "memory", tetapi membuat AI yang memiliki pemahaman tentang user melalui pengalaman percakapan.

AI harus mampu:

* mengenali fakta tentang user
* memahami pola dan kebiasaan user
* mengingat konteks penting
* menghubungkan informasi lama dan baru
* memperbarui pemahamannya ketika user berubah

---

# Prinsip Desain Utama

## Memory bukan kategori

Sistem tidak menggunakan kategori fixed sebagai fondasi.

Hindari desain seperti:

* profile memory
* preference memory
* relationship memory
* project memory

karena dunia nyata tidak memiliki batas kategori yang jelas.

Memory disimpan sebagai fakta bermakna.

Contoh:

Benar:

```
Andre lebih produktif ketika bekerja malam hari.
```

Tidak:

```
category: habit
value: night
```

---

# Current Stack

## Backend

* Python
* FastAPI

## Local AI Model

* Ollama
* Qwen3:8B

## Storage

Saat ini:

* SQLite

Target:

* SQLite + embedding/vector storage

---

# Current Architecture

Flow saat ini:

```
User Message
      |
      v
FastAPI Chat Endpoint
      |
      v
Agent Service
      |
      +----------------+
      |                |
      v                v
Memory Extractor    Tool System
      |
      v
Memory Storage
      |
      v
Context Builder
      |
      v
Qwen3:8B
      |
      v
Response
```

---

# Completed Features

## Chat System

Status:
DONE

Sudah berjalan:

* FastAPI endpoint `/chat`
* Ollama integration
* Qwen3:8B response generation

## Memory Extraction

Status:
DONE

Sebelumnya menggunakan regex:

Contoh:

```
if "nama saya":
    save name
```

Sudah diganti menjadi:

```
User Message
      |
      v
Qwen3:8B
      |
      v
Memory JSON
```

Contoh input:

```
Saya sedang membuat personal AI menggunakan FastAPI
```

Output:

```json
[
 {
  "memory": "Andre sedang membuat personal AI menggunakan FastAPI",
  "importance": 8
 }
]
```

---

## Memory Storage

Status:
BERJALAN

Saat ini:

SQLite table:

```
memories

id
memory
importance
created_at
```

---

## Basic Retrieval

Status:
BERJALAN

AI sudah bisa:

Input:

```
Siapa nama saya?
```

Output:

```
Nama kamu adalah Andre.
```

Input:

```
Apa proyek saya?
```

Output:

```
Kamu sedang membuat personal AI menggunakan FastAPI.
```

---

# Current Limitations

## 1. Memory masih seperti database catatan

Saat ini:

```
save memory
      |
retrieve memory
      |
inject prompt
```

Belum ada:

* pemahaman hubungan antar memory
* penggabungan memory
* perubahan memory
* forgetting

---

## 2. Retrieval belum semantic

Masalah:

Memory:

```
Andre punya perasaan kepada Ahi Max.
```

Pertanyaan:

```
Siapa orang yang membuat saya bahagia?
```

Keyword search bisa gagal.

Target:

```
Query
 |
Embedding
 |
Semantic Search
 |
Relevant Memory
```

---

## 3. Belum ada Memory Consolidation

Saat ini:

```
Memory baru
     |
     v
Save
```

Target:

```
Memory baru
      |
      v
Bandingkan memory lama
      |
      v
Gabungkan / update / pertahankan
```

Contoh:

Memory lama:

```
Andre menggunakan Python.
```

Memory baru:

```
Andre sekarang sering menggunakan Rust.
```

AI harus memahami perkembangan, bukan hanya menyimpan dua fakta terpisah.

---

# Target Architecture

```
                 User Message
                      |
                      v
              Understanding Layer
                      |
          +-----------+-----------+
          |                       |
          v                       v
 Memory Extraction        Intent Understanding
          |
          v
     Memory Store
          |
          v
 Memory Consolidation
          |
          v
 Semantic Retrieval
          |
          v
 Context Builder
          |
          v
       Qwen3:8B
          |
          v
       Response
```

---

# Next Development Steps

## Phase 1 - Upgrade Memory Storage

Tambahkan:

```
confidence
last_accessed
access_count
status
superseded_id
```

Tujuan:

Memory memiliki lifecycle.

---

## Phase 2 - Hybrid Retrieval

Ganti keyword-only retrieval menjadi:

```
Semantic Search
+
Keyword Search
+
Recency
+
Importance
```

Skor:

```
final_score =
semantic_similarity
+
importance
+
recency
+
usage_frequency
```

---

## Phase 3 - Memory Consolidation

Background process:

* cari memory yang mirip
* deteksi konflik
* gabungkan fakta
* update pemahaman

---

## Phase 4 - Memory Lifecycle

Tambahkan:

```
active
superseded
archived
```

Memory lama tidak langsung dihapus.

---

# Important Decisions

## Decision 1

Tidak menggunakan fixed memory category.

Alasan:

Kategori membuat sistem sulit berkembang.

Memory harus berdasarkan makna, bukan label.

---

## Decision 2

LLM digunakan untuk memahami memory.

Bukan membuat banyak rule:

```
if nama:
if suka:
if proyek:
```

---

## Decision 3

AI harus belajar tentang user, bukan hanya mengambil data user.

---

# Current Project State

Milestone:

```
Chatbot
        |
        v
Chatbot + Memory
        |
        v
Personal AI Foundation   <-- CURRENT
        |
        v
Cognitive Memory System
```

Fokus pengembangan berikutnya:

**Mengubah memory dari penyimpanan fakta menjadi sistem pemahaman user.**
