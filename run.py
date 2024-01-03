from dashboard import app, VALORE, path


import subprocess


def elimina_il_file___dotenv():
    subprocess.call("del C:\\Users\\Utente\\Desktop\\info\\variabili\\.env", shell=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) if VALORE else app.run(debug=True)

    elimina_il_file___dotenv()
    with open(path+"\\check.txt", "w") as f: count = f.write("True")
