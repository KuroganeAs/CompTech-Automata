## State Machine Kombinasi Tombol

Implementasi pada `combos.py` membangun finite state machine (FSM) berbasis trie untuk mendeteksi 10 kombo fighting game dengan batas waktu 1 detik antar input. Kombo hanya valid jika seluruh tombol ditekan berurutan tanpa jeda >1s; jika lewat, FSM reset ke akar.

### Cara Pakai (Python)
- Input yang diterima hanya panah `→ ← ↑ ↓` dan spasi (space bar).
- Buat `InputEvent(button, timestamp, action="press")`, lalu panggil `ComboStateMachine.handle_event(event)` untuk tiap event (press atau release) dari `combos.py`.
- Hasil deteksi: dict `{"combo": <nama>, "charged": <bool>, "hold_duration": <opsional>}` atau None.
- Deteksi kombo terjadi saat spasi DILEPAS. Tekan spasi terakhir, tahan 2–3 detik, lalu rilis untuk `charged=True`. Jika spasi dilepas tanpa kombo lengkap, akan mengembalikan error `incomplete_combo`.

Contoh singkat:
```
from combos import ComboStateMachine, InputEvent
import time

fsm = ComboStateMachine()
now = time.monotonic()
events = [
    InputEvent("→", now + 0.0),
    InputEvent("→", now + 0.2),
    InputEvent("→", now + 0.4),
    InputEvent(" ", now + 0.5, action="press"),
    InputEvent(" ", now + 2.7, action="release"),  # hold 2.2s -> charged
]

for e in events:
    detected = fsm.handle_event(e)
    if detected:
        print(detected)
```

### Aturan yang Diimplementasikan
- 10 kombo sesuai tabel tugas (seluruh berakhiran Space).
- Timeout 1s antar tombol (press); jika terlewati, state kembali ke akar sebelum memproses input berikutnya.
- Efek khusus: jika Space terakhir ditahan 2–3s lalu dilepas, hasil deteksi berlabel `charged=True` dengan `hold_duration`.

### Mode Interaktif (terminal, real-time, tanpa prompt)
```
cd "C:\Users\kevin\OneDrive\Documents\Comptech_Kuro"
pip install keyboard
python interactive.py
```
- Tekan langsung di keyboard: panah `→ ← ↑ ↓` atau spasi. `q` atau `Esc` untuk keluar.
- Spasi cukup sekali (real press/release); tahan 2–3 detik untuk efek charge.
- Idle lebih dari 1 detik akan mereset state machine (sesuai aturan timeout), tapi saat spasi sedang ditekan untuk charge tidak di-reset.
- Jika spasi dilepas tetapi rangkaian kombo belum lengkap, akan muncul pesan "Combo tidak lengkap".

### Tes Semua Kombo
```
cd "C:\Users\kevin\OneDrive\Documents\Comptech_Kuro"
python test_all_combos.py
```
Script ini memutar semua kombo di `COMBO_DEFINITIONS` dan melaporkan OK/FAIL, plus satu tes charge pada kombo pertama.

### Diagram Automata
Representasi high-level automata berbasis trie. Simbol R/L/U/D/Spc = Right/Left/Up/Down/Space. State `S0` adalah akar; state terminal ditandai dengan nama kombo.

```
stateDiagram-v2
    [*] --> S0
    S0 --> R1: R
    S0 --> L1: L
    S0 --> U1: U
    S0 --> D1: D

    R1 --> R2: R
    R2 --> R3: R
    R3 --> Hadoken: Spc

    R2 --> D1b: D
    D1b --> R3b: R
    R3b --> Hurricane: R
    Hurricane --> HurricaneSpc: Spc
    HurricaneSpc --> [*]

    R2 --> U1b: U
    U1b --> D1c: D
    D1c --> R4: R
    R4 --> UltraShoryuPrep: D
    UltraShoryuPrep --> R5: R
    R5 --> UltraShoryu: Spc

    R3 --> D2: D
    D2 --> U2: U
    U2 --> R4: R
    R4 --> GigaHadoken: Spc

    L1 --> R1b: R
    R1b --> L2: L
    L2 --> R2b: R
    R2b --> Tatsumaki: Spc

    U1 --> U2b: U
    U2b --> D3: D
    D3 --> R6: R
    R6 --> DragonPunch: Spc

    U1 --> D4: D
    D4 --> U3: U
    U3 --> R7: R
    R7 --> Shoryuken: Spc

    U2b --> D5: D
    D5 --> R8: R
    R8 --> R9: R
    R9 --> R10: R
    R10 --> MegaTatsu: Spc

    L1 --> U4: U
    U4 --> R11: R
    R11 --> R12: R
    R12 --> D6: D
    D6 --> U5: U
    U5 --> R13: R
    R13 --> FinalDP: Spc

    R2 --> U6: U
    U6 --> D7: D
    D7 --> R14: R
    R14 --> U7: U
    U7 --> R15: R
    R15 --> R16: R
    R16 --> UltimateHK: Spc
```

Catatan: Diagram memperlihatkan jalur utama. Untuk keterbacaan, beberapa state intermediate (mis. untuk variasi fallback) tidak ditampilkan; implementasi kode tetap mencakup seluruh transisi dan reset saat mismatch/timeout.

