# Penggunaan Dashboard
1. Pilih tahun pada *select box* tahunan yang tertera pada app untuk mengganti plot dari tahun ke tahun
2. Pilih gas polutan pada *select box* polutan untuk mengganti variable
3. Untuk app Pertanyaan, *tombol radio* akan secara otomatis mengurutkan data dari terbesar ke terkecil atau sebaliknya

# Setup
mkdir proyek_analisis_air_quality
cd proyek_analisis_air_quality
pipenv install
pipenv shell
pip install -r requirements.txt

streamlit run dashboard.py