from flask import Flask, render_template_string

app = Flask(__name__)

piket_per_hari = {
    "Selasa": [
        "Nurul Agustina", "NORA SYUHADA", "Muhammad Alfitrah", "Muhammad Abil",
        "ZACHRA ALMIRA APRILLA", "Muhammad Rizki", "Taufik Muhaimin"
    ],
    "Rabu": [
        "TRI KUMALA SARI", "Nurul Afiqah Simbolon", "Sunil Hukmi", "Andrian Fakhruza",
        "Mulyani", "Rizki Ananda", "AFIIFA LHOKSEUM DWI PUTRI"
    ],
    "Kamis": [
        "Vidya Ayu Ningtyas", "Muhammad Rafli Aulia", "AURA SYASKIA", "ZAMHUR",
        "CUT EVANA SALSABILA", "CUT SITI SARAH AZKIANI", "Muhammad Rafli"
    ],
    "Jumat": [
        "Teuku Aldie Aulia", "CUT RAYSHA", "Dimas Kurniawan", "Fachrul Rozi Rangkuti",
        "Febri Fanisa", "Sultan Juanda Al Muttaqin"
    ]
}

TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Jadwal Piket Interaktif</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #ffe0f0, #d3cce3);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.2);
            overflow-x: hidden;
        }
        h1 {
            color: #5c2a9d;
            margin-bottom: 30px;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.2);
            animation: fadeSlide 1s ease-out;
        }
        .btn {
            background-color: #b36bff;
            color: white;
            padding: 15px 25px;
            margin: 10px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 18px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            animation: bounceIn 0.6s ease forwards;
            position: relative;
            overflow: hidden;
        }
        .btn:hover {
            animation: pulse 0.6s;
            transform: translateY(-3px) scale(1.08);
            box-shadow: 0 8px 16px rgba(0,0,0,0.25);
        }
        .btn:active::after {
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 50%;
            animation: bubble 0.5s ease-out;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 0;
        }
        .btn span {
            position: relative;
            z-index: 1;
        }
        .jadwal {
            display: none;
            opacity: 0;
            transform: scale(0.95);
            margin-top: 30px;
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
            animation: fadeZoom 0.6s ease forwards;
        }
        .jadwal h3 {
            margin-top: 0;
            color: #5c2a9d;
            text-align: center;
        }
        ul {
            padding-left: 20px;
            text-align: left;
        }
        li {
            margin: 5px 0;
            font-size: 16px;
        }

        .back-btn {
            margin-top: 20px;
            background-color: #ff85b3;
        }

        @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeZoom {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes bounceIn {
            0% { transform: scale(0.9); opacity: 0; }
            60% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); }
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        @keyframes bubble {
            from {
                transform: translate(-50%, -50%) scale(0);
                opacity: 0.8;
            }
            to {
                transform: translate(-50%, -50%) scale(1.5);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <h1>🌈 Jadwal Piket Kelas TI 3D 🌈</h1>

    <div id="button-container">
        {% for hari in piket_per_hari %}
            <button class="btn" onclick="showJadwal('{{ hari }}')"><span>{{ hari }}</span></button>
        {% endfor %}
    </div>

    {% for hari, siswa_list in piket_per_hari.items() %}
    <div id="jadwal-{{ hari }}" class="jadwal">
        <h3>📅 Jadwal Piket Hari {{ hari }}</h3>
        <ul>
            {% for nama in siswa_list %}
                <li>👩‍🎓 {{ nama }}</li>
            {% endfor %}
        </ul>
        <button class="btn back-btn" onclick="kembali()"><span>⬅️ Kembali</span></button>
    </div>
    {% endfor %}

    <script>
        function showJadwal(hari) {
            document.getElementById('button-container').style.display = 'none';

            document.querySelectorAll('.jadwal').forEach(el => {
                el.style.display = 'none';
                el.style.opacity = 0;
                el.style.transform = 'scale(0.95)';
            });

            const elemen = document.getElementById('jadwal-' + hari);
            if (elemen) {
                elemen.style.display = 'block';
                setTimeout(() => {
                    elemen.style.opacity = 1;
                    elemen.style.transform = 'scale(1)';
                }, 50);
            }
        }

        function kembali() {
            document.querySelectorAll('.jadwal').forEach(el => {
                el.style.display = 'none';
            });
            document.getElementById('button-container').style.display = 'flex';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE, piket_per_hari=piket_per_hari)

if __name__ == '__main__':
    app.run(debug=True)
