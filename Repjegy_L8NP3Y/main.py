import tkinter as tk
import csv

# Járatok beolvasása
def beolvas_jaratokat(fajlnev):
    try:
        with open(fajlnev, newline='', encoding='utf-8') as csvfile:
            olvaso = csv.reader(csvfile)
            fejlec = next(olvaso)
            jaratok = list(olvaso)
            return fejlec, jaratok
    except FileNotFoundError:
        return [], []

def foglalas_kattintas(jarat):
    popup = tk.Toplevel()
    popup.title("Járat részletei")
    popup.geometry("450x550")
    popup.resizable(False, False)

    tk.Label(popup, text="Járat részletei", font=("Arial", 14, "bold"), pady=10).pack()

    adatok_frame = tk.Frame(popup)
    adatok_frame.pack(pady=10)

    mezok = ["Járatszám", "Légitársaság", "Kiindulás", "Célállomás", "Indulás", "Időtartam", "Ár", "Típus"]
    for i, (mezo, ertek) in enumerate(zip(mezok, jarat)):
        tk.Label(adatok_frame, text=mezo + ":", font=("Arial", 11, "bold"), anchor='e', width=12).grid(row=i, column=0, padx=10, pady=4, sticky='e')
        tk.Label(adatok_frame, text=ertek, font=("Arial", 11), anchor='w').grid(row=i, column=1, padx=10, pady=4, sticky='w')

    input_frame = tk.Frame(popup)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Vezetéknév:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
    vezeteknev_entry = tk.Entry(input_frame, font=("Arial", 11), width=25)
    vezeteknev_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(input_frame, text="Keresztnév:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
    keresztnev_entry = tk.Entry(input_frame, font=("Arial", 11), width=25)
    keresztnev_entry.grid(row=1, column=1, padx=10, pady=5)

    gomb_frame = tk.Frame(popup)
    gomb_frame.pack(pady=20)

    vasarlas_gomb = tk.Button(
        gomb_frame,
        text="Vásárlás",
        font=("Arial", 11, "bold"),
        bg="green",
        fg="white",
        state="disabled",
        width=12
    )
    vasarlas_gomb.grid(row=0, column=1, padx=10)

    def frissit_gomb_allapot(*args):
        if vezeteknev_entry.get().strip() and keresztnev_entry.get().strip():
            vasarlas_gomb.config(state="normal")
        else:
            vasarlas_gomb.config(state="disabled")

    vezeteknev_entry.bind("<KeyRelease>", frissit_gomb_allapot)
    keresztnev_entry.bind("<KeyRelease>", frissit_gomb_allapot)

    def vasarlas():
        vezeteknev = vezeteknev_entry.get().strip()
        keresztnev = keresztnev_entry.get().strip()
        if not (vezeteknev and keresztnev):
            return

        fajlnev = "foglalasok.csv"
        adatsor = [vezeteknev, keresztnev] + jarat

        with open(fajlnev, mode='a', newline='', encoding='utf-8') as file:
            iras = csv.writer(file)
            iras.writerow(adatsor)

        print(f"Mentve: {vezeteknev} {keresztnev} – {jarat[0]}")
        popup.destroy()

    vasarlas_gomb.config(command=vasarlas)

    megse_gomb = tk.Button(gomb_frame, text="Mégse", font=("Arial", 11), command=popup.destroy, width=12)
    megse_gomb.grid(row=0, column=0, padx=10)

# Táblázat
def jegy_foglalasa():
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    fejlec, jaratok = beolvas_jaratokat("jaratok.csv")
    if not jaratok:
        tk.Label(canvas_frame, text="Nincs betölthető járat.", font=("Arial", 12)).grid(row=0, column=0, sticky='w')
        return

    oszlopok = {
        "Légitársaság": 1,
        "Kiindulás": 2,
        "Célállomás": 3,
        "Indulás": 4,
        "Ár (Ft)": 6
    }

    for i, felirat in enumerate(list(oszlopok.keys()) + [""]):
        tk.Label(
            canvas_frame,
            text=felirat,
            font=("Arial", 11, "bold"),
            padx=10, pady=6,
            anchor='center'
        ).grid(row=0, column=i, sticky='nsew', padx=5)

    for sor_index, sor in enumerate(jaratok, start=1):
        for i, index in enumerate(oszlopok.values()):
            tk.Label(
                canvas_frame,
                text=sor[index],
                font=("Arial", 11),
                padx=10, pady=4,
                anchor='center'
            ).grid(row=sor_index, column=i, sticky='nsew', padx=5)

        link = tk.Label(
            canvas_frame,
            text="Foglalás",
            font=("Arial", 11, "underline"),
            fg="blue",
            cursor="hand2"
        )
        link.grid(row=sor_index, column=len(oszlopok), sticky='nsew', padx=5)
        link.bind("<Button-1>", lambda e, jarat=sor: foglalas_kattintas(jarat))

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def foglalasok_listazasa():
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    try:
        with open("foglalasok.csv", newline='', encoding='utf-8') as file:
            olvaso = csv.reader(file)
            sorok = list(olvaso)
    except FileNotFoundError:
        tk.Label(canvas_frame, text="A foglalasok.csv fájl nem található.", font=("Arial", 11)).grid(row=0, column=0, sticky='w')
        return
    except Exception as e:
        tk.Label(canvas_frame, text=f"Hiba a fájl olvasásakor: {e}", font=("Arial", 11)).grid(row=0, column=0, sticky='w')
        return

    if len(sorok) < 2:
        tk.Label(canvas_frame, text="Még nincsen foglalásod :(", font=("Arial", 11)).grid(row=0, column=0, sticky='w')
        return

    fejlec = ["Utas neve", "Légitársaság", "Kiindulás", "Célállomás", "Indulás", ""]  # utolsó: Lemondás gomb
    for col_index, mezo in enumerate(fejlec):
        tk.Label(
            canvas_frame,
            text=mezo,
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            anchor='center'
        ).grid(row=0, column=col_index, sticky='nsew')

    # Lemondás
    for row_index, sor in enumerate(sorok[1:], start=1):
        teljes_nev = f"{sor[0]} {sor[1]}"
        adatok = [teljes_nev, sor[3], sor[4], sor[5], sor[6]]
        for col_index, ertek in enumerate(adatok):
            tk.Label(
                canvas_frame,
                text=ertek,
                font=("Arial", 11),
                padx=10,
                pady=4,
                anchor='center'
            ).grid(row=row_index, column=col_index, sticky='nsew')

        # Lemondás gomb
        link = tk.Label(
            canvas_frame,
            text="Lemondás",
            font=("Arial", 11, "underline"),
            fg="red",
            cursor="hand2"
        )
        link.grid(row=row_index, column=len(adatok), sticky='nsew', padx=5)

        eredeti_sor = sor.copy()

        # felugro
        def lemondas_popup(foglalas_sor):
            popup = tk.Toplevel()
            popup.title("Foglalás lemondása")
            popup.geometry("450x500")
            popup.resizable(False, False)

            tk.Label(popup, text="Foglalás lemondása", font=("Arial", 14, "bold"), pady=10).pack()

            # Foglalás adatai
            mezok = ["Vezetéknév", "Keresztnév", "Járatszám", "Légitársaság", "Kiindulás", "Célállomás", "Indulás",
                     "Időtartam", "Ár", "Típus"]

            adatok_frame = tk.Frame(popup)
            adatok_frame.pack(pady=10)

            for i, (mezo, ertek) in enumerate(zip(mezok, foglalas_sor)):
                tk.Label(adatok_frame, text=mezo + ":", font=("Arial", 11, "bold"), anchor='e', width=12).grid(row=i,
                                                                                                               column=0,
                                                                                                               padx=10,
                                                                                                               pady=4,
                                                                                                               sticky='e')
                tk.Label(adatok_frame, text=ertek, font=("Arial", 11), anchor='w').grid(row=i, column=1, padx=10,
                                                                                        pady=4, sticky='w')

            # Gombok
            gomb_frame = tk.Frame(popup)
            gomb_frame.pack(pady=20)

            def vegleges_lemondas():
                with open("foglalasok.csv", newline='', encoding='utf-8') as f:
                    reader = list(csv.reader(f))
                uj_sorok = [reader[0]] + [s for s in reader[1:] if s != foglalas_sor]
                with open("foglalasok.csv", mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(uj_sorok)
                popup.destroy()
                foglalasok_listazasa()

            megse_btn = tk.Button(gomb_frame, text="Mégse", font=("Arial", 11), width=12, command=popup.destroy)
            megse_btn.grid(row=0, column=0, padx=10)

            lemond_btn = tk.Button(gomb_frame, text="Lemondás", font=("Arial", 11, "bold"), width=12, bg="red",
                                   fg="white", command=vegleges_lemondas)
            lemond_btn.grid(row=0, column=1, padx=10)

        link.bind("<Button-1>", lambda e, s=eredeti_sor: lemondas_popup(s))

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# GUI
ablak = tk.Tk()
ablak.title("Repülőjegy Foglalási Rendszer")
ablak.geometry("1000x600")

cimke = tk.Label(ablak, text="Repülőjegy Foglalási Rendszer", font=("Arial", 18, "bold"), pady=10)
cimke.pack()

gombok_keret = tk.Frame(ablak)
gombok_keret.pack(pady=8)

foglalas_gomb = tk.Button(gombok_keret, text="Jegy foglalása", font=("Arial", 13), command=jegy_foglalasa)
foglalas_gomb.grid(row=0, column=0, padx=10)

listazas_gomb = tk.Button(gombok_keret, text="Foglalásaim", font=("Arial", 13), command=foglalasok_listazasa)
listazas_gomb.grid(row=0, column=1, padx=10)

keret = tk.Frame(ablak)
keret.pack(expand=True, fill='both', padx=20, pady=10)

canvas = tk.Canvas(keret, bd=0, highlightthickness=0)
scrollbar = tk.Scrollbar(keret, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

canvas_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=canvas_frame, anchor="n")

def kozepre_igazitas(event):
    canvas_width = event.width
    canvas.coords(canvas_window, canvas_width // 2, 0)

canvas.bind("<Configure>", kozepre_igazitas)

ablak.mainloop()
