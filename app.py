from flask import Flask, render_template_string, request, redirect, url_for
import json

app = Flask(__name__)

# Load data dari file JSON (jika ada)
try:
    with open("piket_data.json", "r") as f:
        piket_per_hari = json.load(f)
except FileNotFoundError:
    # Data awal kosong
    piket_per_hari = {
        "Selasa": [],
        "Rabu": [],
        "Kamis": [],
        "Jumat": []
    }

# Simpan ke file JSON
def save_data():
    with open("piket_data.json", "w") as f:
        json.dump(piket_per_hari, f)

# Halaman Utama
TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Jadwal Piket Interaktif</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; flex-direction: column; min-height: 100vh; margin: 0; background: linear-gradient(135deg, #d4bfff, #fbeaff); transition: background 0.5s ease; }
        h1 { color: #5c2a9d; margin-bottom: 30px; text-align: center; animation: fadeInDown 0.7s ease-out; }
        .btn { background-color: #b36bff; color: white; padding: 15px 25px; border: none; border-radius: 50px; cursor: pointer; margin: 5px; transition: background-color 0.3s ease, transform 0.2s; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); }
        .btn:hover { background-color: #9332b8; transform: translateY(-3px) scale(1.05); }
        .jadwal { margin-top: 30px; background: #fff; padding: 25px; border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); width: 320px; text-align: center; animation: fadeIn 0.5s ease-in-out; display: none; }
        ul { padding-left: 20px; text-align: left; }
        li { font-size: 16px; opacity: 0; transform: translateY(10px); animation: slideIn 0.5s forwards; animation-delay: var(--delay); margin-bottom: 5px; transition: all 0.3s ease; }
        li:hover { background-color: #f1f1ff; padding-left: 5px; border-left: 3px solid #b36bff; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideIn { 0% { transform: translateY(10px); opacity: 0; } 100% { transform: translateY(0); opacity: 1; } }
    </style>
</head>
<body>
    <h1>🌈 Jadwal Piket Kelas TI 3D 🌈</h1>

    <div id="button-container">
        {% for hari in piket_per_hari %}
            <button class="btn" onclick="showJadwal('{{ hari }}')">{{ hari }}</button>
        {% endfor %}
        <a href="{{ url_for('add') }}" class="btn">Tambah Jadwal</a>
    </div>

    {% for hari, siswa_list in piket_per_hari.items() %}
    <div id="jadwal-{{ hari }}" class="jadwal">
        <h3>📅 Jadwal Piket Hari {{ hari }}</h3>
        <ul>
            {% for nama in siswa_list %}
                <li style="--delay: {{ loop.index * 0.1 }}s;">👩‍🎓 {{ nama }} 
                    <a href="{{ url_for('edit', hari=hari, nama=nama) }}">Edit</a> | 
                    <a href="{{ url_for('delete', hari=hari, nama=nama) }}" style="color:red;">Delete</a>
                </li>
            {% endfor %}
        </ul>
        <a href="{{ url_for('index') }}" class="btn">⬅ Kembali</a>
    </div>
    {% endfor %}

    <script>
        function showJadwal(hari) {
            document.getElementById('button-container').style.display = 'none';
            document.querySelectorAll('.jadwal').forEach(el => {
                el.style.display = 'none';
            });
            const jadwalElement = document.getElementById('jadwal-' + hari);
            jadwalElement.style.display = 'block';
            setTimeout(() => {
                jadwalElement.querySelectorAll('li').forEach((item, index) => {
                    item.style.animationDelay = index * 0.1 + 's';
                });
            }, 0);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE, piket_per_hari=piket_per_hari)

# TAMBAH
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        hari = request.form['hari']
        siswa_name = request.form['nama']
        if siswa_name:
            piket_per_hari[hari].append(siswa_name)
            save_data()
        return redirect(url_for('index'))
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>Tambah Jadwal Piket</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #d4bfff, #fbeaff);
                animation: fadeIn 0.5s ease-in-out;
            }
            h3 { color: #5c2a9d; margin-bottom: 20px; animation: fadeInDown 0.6s ease-out; }
            .form {
                background: #fff;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
                width: 320px;
                text-align: center;
                animation: fadeInUp 0.6s ease-out;
            }
            .form input, .form button, .form select {
                padding: 10px;
                font-size: 16px;
                width: 90%;
                margin: 10px 0;
                border-radius: 8px;
                border: 1px solid #ccc;
                transition: all 0.3s ease;
            }
            .form input:focus, .form select:focus {
                outline: none;
                border-color: #b36bff;
                box-shadow: 0 0 5px #b36bff;
            }
            .form button {
                background-color: #5c2a9d;
                color: white;
                border: none;
                width: 100%;
                cursor: pointer;
                margin-top: 10px;
            }
            .form button:hover {
                background-color: #3c1a6d;
            }
            .btn-back {
                margin-top: 20px;
                background-color: #b36bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 50px;
                text-decoration: none;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.2s;
            }
            .btn-back:hover {
                background-color: #9332b8;
                transform: translateY(-3px) scale(1.05);
            }
            @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        </style>
    </head>
    <body>
        <h3>📝 Tambah Jadwal Piket</h3>
        <form method="POST" class="form">
            <label for="hari">Pilih Hari:</label><br>
            <select name="hari" id="hari" required>
                <option value="Selasa">Selasa</option>
                <option value="Rabu">Rabu</option>
                <option value="Kamis">Kamis</option>
                <option value="Jumat">Jumat</option>
            </select><br>
            <label for="nama">Nama Siswa:</label><br>
            <input type="text" name="nama" id="nama" required><br>
            <button type="submit">Tambah</button>
        </form>
        <a href="{{ url_for('index') }}" class="btn-back">⬅ Kembali</a>
    </body>
    </html>
    """)

# EDIT
@app.route('/edit/<hari>/<nama>', methods=['GET', 'POST'])
def edit(hari, nama):
    if request.method == 'POST':
        new_name = request.form['nama']
        if new_name:
            index = piket_per_hari[hari].index(nama)
            piket_per_hari[hari][index] = new_name
            save_data()
        return redirect(url_for('index'))

    return render_template_string("""
        <h3>Edit Jadwal Piket</h3>
        <form method="POST" class="form">
            <label for="nama">Nama Siswa:</label>
            <input type="text" name="nama" value="{{ nama }}" required><br><br>
            <button type="submit">Update</button>
        </form>
        <a href="{{ url_for('index') }}" class="btn-back">⬅ Kembali</a>
    """, nama=nama)

# DELETE
@app.route('/delete/<hari>/<nama>', methods=['GET'])
def delete(hari, nama):
    if nama in piket_per_hari[hari]:
        piket_per_hari[hari].remove(nama)
        save_data()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
