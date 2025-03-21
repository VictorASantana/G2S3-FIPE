@echo off
cd "C:\Users\Thais\OneDrive\Área de Trabalho\G2S3-FIPE"
call venv\Scripts\activate
python scheduled_task.py >> "C:\Users\Thais\OneDrive\Área de Trabalho\G2S3-FIPE\log.txt" 2>&1