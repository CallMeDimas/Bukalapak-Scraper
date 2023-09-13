@echo off
echo =======================================================
echo Versi: 1.1.0
echo Judul: Bot Scraper Toko Bukalapak
echo Tentang: Bot Scraping Data Dari Bukalapak.com
echo Author : https://github.com/CallMeDimas/
echo Website: https://CallMeDimas.github.io 
echo =======================================================
echo Q: Apa Yang Bot Ini Bisa Dapatkan?...
echo A: (Nama Toko, Rating Toko, Total Feedback, Tanggal Bergabung, Nama Barang, Harga Barang, Link Barang)
echo =======================================================
echo Versi Custom/Lengkap nya Bisa Email ke CallMeDimas@proton.me
echo =======================================================
pause
echo INSTALLING LIBRARY...
pip install -r requirements.txt
python3 bukalapak.py
