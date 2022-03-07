from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string
import csv


def recupere():
	filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
	fichier = open(filename, "r")
	obj = csv.reader(fichier)
	#for ligne in obj :
		#print(ligne)
	#content = fichier.read()
	fichier.close()

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

Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, padx=50, pady=50)

Frame2 = Frame(Frame1, borderwidth=2, relief=GROOVE)
Frame2.pack(side=TOP, padx=5, pady=5)

Label(Frame2, text="CSV").pack(side=TOP, padx=5, pady=5)

Frame3 = Frame(Frame1, borderwidth=2, relief=GROOVE)
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

Frame4 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame4.pack(side=RIGHT, padx=50, pady=50)

onglets = ttk.Notebook(Frame4)
tab1 = ttk.Frame(onglets)
tab2 = ttk.Frame(onglets)
tab3 = ttk.Frame(onglets)
tab4 = ttk.Frame(onglets)

onglets.add(tab1, text='Tronçon1')
onglets.add(tab2, text='Tronçon2')
onglets.add(tab3, text='Tronçon3')
onglets.add(tab4, text='Tronçon4')

onglets.pack(side=BOTTOM, expand=1, fill="both")

#Label(tab1, text="qjzghefgrekl").pack(side=TOP, padx=50, pady=50)

bouton10 = Button(tab1, text="Sauvegarder")
bouton10.pack(side=BOTTOM)

bouton11 = Button(tab2, text="Sauvegarder")
bouton11.pack()

bouton12 = Button(tab3, text="Sauvegarder")
bouton12.pack()

bouton13 = Button(tab4, text="Sauvegarder")
bouton13.pack()

bouton14 = Button(Frame4, text="Paramètres globaux")
bouton14.pack(side=TOP, padx=30, pady=30)

fig = Figure(figsize=(5,5),dpi=100)

#fonction pour le graphe a mettre ici
y = [i**2 for i in range(101)]
plot1 = fig.add_subplot(111)
plot1.plot(y)
###

canvas = FigureCanvasTkAgg(fig, master=tab1)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP)

fenetre.mainloop()