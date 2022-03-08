from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string
import pandas as pd


def recupere():
	filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
	fichier = open(filename, "r")
	obj = pd.read_csv(fichier)
	fichier.close()

#def save(figure) :
	#fig.savefig(figure)

fenetre = Tk()
fenetre.geometry("900x600")

#Canvas(fenetre, width=250, height=100, bg='white').pack(side=TOP, padx=5, pady=5)


#l = LabelFrame(fenetre, text="Documentation", bg='ivory', fg='black', padx=20, pady=20)
#l.pack(side=BOTTOM, fill="both", expand="yes")
#l2 = Label(l, text=content, bg='ivory', fg='black').pack(side=BOTTOM, padx=10, pady=10)

#scroll_bar = Scrollbar(l)
#scroll_bar.pack(side=RIGHT, fill=Y)

#text = Text(l, yscrollcommand=scroll_bar.set, bg='ivory', fg='black', height=10, width=10)
#text.insert(INSERT, content)
#text.pack()

#scroll_bar.config(command=text.yview)

Frame1 = Frame(fenetre, borderwidth=2)
Frame1.pack(side=LEFT, padx=50, pady=50)

Frame2 = Frame(Frame1, borderwidth=2)
Frame2.pack(side=TOP, padx=5, pady=5)

Label(Frame2, text="CSV").pack(side=TOP, padx=5, pady=5)

Frame3 = Frame(Frame1, borderwidth=2)
Frame3.pack(padx=5, pady=5)

Label(Frame3, text="Paramètres").pack(side=TOP, padx=5, pady=5)

bouton = Button(Frame2, text = "Csv dynamique", command=recupere)
bouton.pack(side=TOP, padx=5, pady=5)

bouton1 = Button(Frame2, text = "Csv défensif", command=recupere)
bouton1.pack(padx=5, pady=5)

bouton2 = Button(Frame2, text = "Csv à analyser", command=recupere)
bouton2.pack(padx=5, pady=5)

bouton3 = Checkbutton(Frame3, text="vitesse")
bouton3.pack()

bouton4 = Checkbutton(Frame3, text="accélération")
bouton4.pack()

bouton5 = Checkbutton(Frame3, text="_____")
bouton5.pack()

bouton6 = Checkbutton(Frame3, text="_____")
bouton6.pack()

bouton7 = Checkbutton(Frame3, text="_____")
bouton7.pack()

bouton8 = Checkbutton(Frame3, text="_____")
bouton8.pack()

bouton9 = Button(Frame1, text="Lancer l'analyse")
bouton9.pack()

Frame4 = Frame(fenetre, borderwidth=2)
Frame4.pack(side=RIGHT, padx=50, pady=50)

onglets = ttk.Notebook(Frame4)

#ici appeler fonction de Valentin pour récupérer liste de figures
liste = ["ee", "rr", "tt", "yy", "uu"]

longlets = []
lbuttons = []

for i in range(len(liste)) :

	#################A retirer quand liste de figures
	fig = Figure(figsize=(5,5),dpi=100)
	y = [i**2 for i in range(101)]
	#################
	#fig = liste[i]
	plot1 = fig.add_subplot(111)
	plot1.plot(y)
	###

	longlets.append(ttk.Frame(onglets))
	onglets.add(longlets[i], text="Tronçon" + str(i+1))
	lbuttons.append(Button(longlets[i], text="Sauvegarder"))
	lbuttons[i].pack(side=BOTTOM)

	canvas = FigureCanvasTkAgg(fig, master=longlets[i])
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP)

onglets.pack(side=BOTTOM, expand=1, fill="both")

#Label(tab1, text="qjzghefgrekl").pack(side=TOP, padx=50, pady=50)

bouton14 = Button(Frame4, text="Paramètres globaux")
bouton14.pack(side=TOP, padx=30, pady=30)



fenetre.mainloop()