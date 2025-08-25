from math import*
import numpy as np 
import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import font

###########################################################################################################################################

# Sn : le salaire mensuel imposable 
# n : le nombre d'année du crédit souhiaté
# tc : taux du crédit immobilier

def emprunt (Sn, n, t, p ):
    tc = t/12
    x = (p * Sn * n * 12) / ( ( (tc*n*12) / (1-((1 + tc)**(-n*12))) ) + 0.07) # Calcul de la valeur de la maison
    N = 0.07 * x # frais de notaire ( 0.07 en moyenne )
    i = (p * Sn * n * 12) - 0.07 * x - x
    c = p * Sn * n * 12
    return x,N,i,c

def resultat_emprunt(Sn,n,t,p,App):
   
   Sn_val = float(Sn.get())
   n_val = int(n.get())
   t_val = float(t.get())
   p_val = float(p.get())
   App_val = float(App.get())

   maison,notaire,interets,capital = emprunt(Sn_val,n_val,t_val,p_val)
   reponse_label.config(text=f" Capital : {capital:,.2f} €\n Emprunt {(1-App_val)*100}% : {maison:,.2f} € \n Apports {maison*App_val/(1-App_val):,.2f} € \n Maison {maison/(1-App_val):,.2f} €")
   reponse_label_4.config(text=f"  Intérêts : {interets:,.2f}€,\n Frais notaire: {notaire:,.2f} € ")
###########################################################################################################################################

# P0 : apport dans le portefeuille
# n : nombre d'année d'investissement
# mensualité : ( oui ou non )
# m : montant des mensualités ( x si oui , 0 si non )
# R : rendement du portefeuille ( ex : 0.03 qui correspond à 3% )

def portefeuille (P0, n , mensualite , m , R): 
  t = np.linspace(1,n,n)
  capital = []
  liquidite = []
  impot = []

  if mensualite == "oui":
    for i in range(1,len(t)+1):

      tot = P0*(1+R)**i + 12*m*(((1+R)**i)-1)/R
      ecart = tot - P0 - m*i*12
      impots= 0.3*ecart # 30% du benefice (total avec intérêts - total sans intérêts )

      capital.append(tot) # Calcul arithmético-géometrique avec mensualité
      liquidite.append(tot - impots)
      impot.append(impots)

  else : 
    for i in range(1,len(t)+1):  # Calcul géométrique sans mensualité
      tot = P0*(1+R)**i
      ecart = tot-P0
      impots= 0.3*ecart
      capital.append(tot)
      liquidite.append (tot-impots)
      impot.append(impots)
  return capital[-1], liquidite[-1]
    
def resultat_portefeuille(P0, n , mensualite , m , r):
   
   P0_val = float(P0.get())
   n_val = int(n.get())
   mensualite_val = mensualite.get()
   m_val = float(m.get())
   r_val = float(r.get())

   capital,liquidite = portefeuille(P0_val,n_val,mensualite_val,m_val,r_val)
   reponse_label_2.config(text=f"Avant impôts : {capital:,.2f} € \n  Après impôts : {liquidite:,.2f} €")

###########################################################################################################################################

# adult_parts : nombre d'adulte = 1 part 
# E : nombre d'etudiant
# e : nombre d'enfant
# R : Revenus net imposable annuel
# Pension : Pension annuel versée à/aux l'étudiant/étudiants

def impots(adult_parts, E, e, R, Pension, verbose=True):

  def fiscalité(quotient):
      if quotient < 11497:
          return 0
      elif 11498 <= quotient < 29315:
          return 0.11 * (quotient - 11498)
      elif 29316 <= quotient < 83823:
          return 0.11 * 17817 + 0.3 * (quotient - 29316)
      elif 83824 <= quotient < 180293:
          return 0.11 * 17817 + 0.3 * 54507 + 0.4 * (quotient - 83824)
      else:
          return 0.11 * 17817 + 0.3 * 54507 + 0.4 * 96469 + 0.45 * (quotient - 180294)

    # Calcul des parts fiscales
  if e < 3:
      Parts = adult_parts + 0.5 * e
  else:
      Parts = adult_parts + 0.5 * (e - 1) + 1

    # Vérification des pensions
  if E > 0:
      if Pension > 6674 * E:
          raise ValueError("Pension trop élevée : maximum autorisé = 6 674 € par étudiant.")
      R_fiscal = R - Pension
  else:
      R_fiscal = R

    # Calculs de l'impôt avec et sans quotient familial
  quotient_f = R_fiscal / Parts
  impots_avec_qf = fiscalité(quotient_f) * Parts

  quotient_sans_qf = R / adult_parts
  impots_sans_qf = fiscalité(quotient_sans_qf) * adult_parts

    # Calcul du plafonnement du quotient familial
  nb_demi_parts_sup = max(0, Parts - adult_parts) * 2
  reduction_max = nb_demi_parts_sup * 1759  
  gain_qf = impots_sans_qf - impots_avec_qf

  if gain_qf > reduction_max:
      impots_final = impots_sans_qf - reduction_max
      msg = f"Réduction QF plafonnée à {reduction_max:.2f} €."
  else:
      impots_final = impots_avec_qf
      if e == 0:
          msg = "Pas de réduction liée au quotient familial : aucun enfant à charge."
      else:
          msg = f"Réduction QF appliquée : {gain_qf:.2f} €."

  revenu_net = R - impots_final
  revenu_mensuel = revenu_net / 12


  return impots_final, revenu_net,revenu_mensuel

def resultat_impot(a,E,e,R,P,verbose=True):
  a_val = float(a.get())
  E_val = float(E.get())
  e_val = float(e.get())
  R_val = float(R.get())
  P_val = float(P.get())
  impots_final, revenu_net,revenu_mensuel = impots(a_val,E_val,e_val,R_val,P_val)
  reponse_label_3.config(text=f"Montant des impôts : {impots_final:,.2f}€ \n et revenus : {revenu_net:,.2f}€")

###########################################################################################################################################

root = tk.Tk()
root.title("Logiciel Bancaire")
root.configure(bg="darkgreen") #Fond d'écran ( hors texte )

titre_font = font.Font(family='Arial', size=14, weight='bold')

tk.Label(root, text="Calcul valeur maison", font=titre_font,fg="gold", bg="darkgreen").grid(row=1, column=0, sticky='w', padx=5, pady=5,)

tk.Label(root,text="Salaire net après impots (mensuel)", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=2, column=0, sticky = 'w', padx=5, pady=5)
Sn = tk.Entry(root)
Sn.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root,text="Durée en année du prêt (années)", font=('Arial', 12),fg="gold", bg="darkgreen").grid(row=3, column=0, sticky = 'w', padx=5, pady=5)
n = tk.Entry(root)
n.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root,text="Taux du crédit (ex: 0.03 = 3%)", font=('Arial', 12),fg="gold", bg="darkgreen").grid(row=4, column=0, sticky = 'w', padx=5, pady=5)
t = tk.Entry(root)
t.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root,text="Part du crédit immobilier dans salaire (0.2 = 20%)", font=('Arial', 12),fg="gold", bg="darkgreen").grid(row=5, column=0, sticky = 'w', padx=5, pady=5)
p = tk.Entry(root)
p.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root,text="Pourcentage de l'apport nécessaire", font=('Arial', 12),fg="gold", bg="darkgreen").grid(row=6, column=0, sticky = 'w', padx=5, pady=5)
App = tk.Entry(root)
App.grid(row=6, column=1, padx=5, pady=5)


button = tk.Button(root, text="Simuler", font=('Arial', 12),fg="gold", bg="darkgreen", command=lambda: resultat_emprunt(Sn, n, t, p,App))
button.grid(row=7, column=0, padx=5, pady=5)

# Label pour afficher le résultat
reponse_label = tk.Label(root, text="", font=('Arial', 12),fg="gold", bg="darkgreen")
reponse_label.grid(row=9, column=0, padx=5, pady=5)

reponse_label_4 = tk.Label(root,text="",font=('Arial',12), fg="gold", bg ="darkgreen")
reponse_label_4.grid(row=9, column = 1, padx = 5 , pady = 5 )

#tk.Label(root, text="-------------", font=titre_font,fg="gold", bg="darkgreen").grid(row=1, column=2, sticky='w', padx=5, pady=5,)


###############################################################################################################################

tk.Label(root, text="Calcul valeur Capital", font=titre_font,fg="gold", bg="darkgreen").grid(row=1, column=3, sticky='w', padx=5, pady=5,)

tk.Label(root,text="Apport ( 0 si aucun )", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=2, column=3, sticky = 'w', padx=5, pady=5)
P0 = tk.Entry(root)
P0.grid(row=2, column=4, padx=5, pady=5)

tk.Label(root,text="Durée en année de l'investissement", font=('Arial', 12),fg="gold", bg="darkgreen").grid(row=3, column=3, sticky = 'w', padx=5, pady=5)
n_p = tk.Entry(root)
n_p.grid(row=3, column=4, padx=5, pady=5)

tk.Label(root,text="Mensualités (oui ou non)", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=4, column=3, sticky = 'w', padx=5, pady=5)
mensualite = tk.Entry(root)
mensualite.grid(row=4, column=4, padx=5, pady=5)

tk.Label(root,text="Montant des mensualités ( 0 si non )", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=5, column=3, sticky = 'w', padx=5, pady=5)
m = tk.Entry(root)
m.grid(row=5, column=4, padx=5, pady=5)

tk.Label(root,text="Rendement du portefeuille ( ex : 0.07 )", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=6, column=3, sticky = 'w', padx=5, pady=5)
r = tk.Entry(root)
r.grid(row=6, column=4, padx=5, pady=5)


button = tk.Button(root, text="Simuler", font=('Arial', 12), fg="gold", bg="darkgreen", command=lambda: resultat_portefeuille(P0, n_p , mensualite , m , r))
button.grid(row=7, column=3, padx=5, pady=5)

# Label pour afficher le résultat
reponse_label_2 = tk.Label(root, text="", font=('Arial', 12), fg="gold", bg="darkgreen")
reponse_label_2.grid(row=9, column=4, padx=5, pady=5)

##################################################################################################################################
#tk.Label(root, text="---------------------------------------------", font=titre_font,fg="gold", bg="darkgreen").grid(row=11, column=0, sticky='w', padx=5, pady=5,)
#tk.Label(root, text="-----------------------", font=titre_font,fg="gold", bg="darkgreen").grid(row=11, column=1, sticky='w', padx=5, pady=5,)
#tk.Label(root, text="-----------------------", font=titre_font,fg="gold", bg="darkgreen").grid(row=11, column=2, sticky='w', padx=5, pady=5,)
#tk.Label(root, text="-----------------------", font=titre_font,fg="gold", bg="darkgreen").grid(row=11, column=3, sticky='w', padx=5, pady=5,)
#tk.Label(root, text="----------------------------------", font=titre_font,fg="gold", bg="darkgreen").grid(row=11, column=4, sticky='w', padx=5, pady=5,)
#tk.Label(root, text="---------------------------", font=titre_font,fg="gold", bg="darkgreen").grid(row=11, column=5, sticky='w', padx=5, pady=5,)
##################################################################################################################################

tk.Label(root, text="Calcul d'impôts", font=titre_font,fg="gold", bg="darkgreen").grid(row=12, column=0, sticky='w', padx=5, pady=5,)

tk.Label(root,text="Nombre d'adulte dans le foyer fiscal", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=13, column=0, sticky = 'w', padx=5, pady=5)
a = tk.Entry(root)
a.grid(row=13, column=1, padx=5, pady=5)

tk.Label(root,text="Nombre d'étudiant", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=14, column=0, sticky = 'w', padx=5, pady=5)
E = tk.Entry(root)
E.grid(row=14, column=1, padx=5, pady=5)

tk.Label(root,text="Nombre d'enfant", font=('Arial', 12),fg="gold", bg="darkgreen").grid(row=15, column=0, sticky = 'w', padx=5, pady=5)
e = tk.Entry(root)
e.grid(row=15, column=1, padx=5, pady=5)

tk.Label(root,text="Revenus net imposable annuel", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=16, column=0, sticky = 'w', padx=5, pady=5)
R = tk.Entry(root)
R.grid(row=16, column=1, padx=5, pady=5)

tk.Label(root,text="Pension versée à l'étudiant annuellement", font=('Arial', 12), fg="gold", bg="darkgreen").grid(row=17, column=0, sticky = 'w', padx=5, pady=5)
P = tk.Entry(root)
P.grid(row=17, column=1, padx=5, pady=5)


button = tk.Button(root, text="Simuler", font=('Arial', 12), fg="gold", bg="darkgreen", command=lambda: resultat_impot(a, E , e ,R , P))
button.grid(row=18, column=0, padx=5, pady=5)


reponse_label_3 = tk.Label(root, text="", font=('Arial', 12), fg="gold", bg="darkgreen")
reponse_label_3.grid(row=18, column=1, padx=5, pady=5)

###################################################################################################################################

zone_texte_frame = tk.Frame(root, bg="darkgreen")
zone_texte_frame.grid(row=13, column=3, columnspan=2,rowspan=5, sticky="w", padx=5, pady=5) 
# Columnspan et rowspan == permet de creer une zone autour du texte sans modifier environnement du logiciel

tk.Label(
    zone_texte_frame,
    text=(
        "Ce logiciel bancaire, développé en Python avec l’interface graphique Tkinter,\n"
        "est un outil complet de simulation financière. Il permet à l’utilisateur d’estimer\n"
        "la valeur d’un bien immobilier en fonction de son salaire, de la durée de l’emprunt,\n"
        "du taux d’intérêt et de son apport personnel, tout en intégrant les frais de notaire\n"
        "et le coût total du crédit.\n\n"
        "Il inclut également un module de calcul de capital investi, avec ou sans versements\n"
        "mensuels, tenant compte du rendement attendu et de la fiscalité sur les gains.\n\n"
        "Enfin, une section dédiée au calcul des impôts permet d’estimer rapidement la charge\n"
        "fiscale annuelle d’un foyer, en fonction de sa composition et de ses revenus, avec\n"
        "gestion des pensions versées aux étudiants.\n\n"
        "L’ensemble offre une vision claire et chiffrée de différents scénarios financiers,\n"
        "facilitant la prise de décision pour des projets immobiliers ou d’investissement."
    ),
    bg="darkgreen",
    fg="gold",
    justify="left",
    wraplength=700,  # limite la largeur pour un meilleur rendu
    font = ('Arial', 11, 'bold'),
).pack(anchor="w")





root.mainloop()