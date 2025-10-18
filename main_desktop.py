import threading
import time
import webview
import subprocess

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "calc.py"])
    time.sleep(3)

if __name__ == "__main__":
    t = threading.Thread(target=run_streamlit)
    t.daemon = True
    t.start()
    webview.create_window("Calculadora de Medicamentos", "http://localhost:8501")
