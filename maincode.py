import math
import scipy.stats as stat
from scipy.stats import poisson
from tkinter import *
import tkinter as tk

def QR_Solver_Normal(mean,variance,orcsot,holcost,zarcost,lead_time,c,b):
    holcost=float(holcost)
    standartdev = math.sqrt(variance*lead_time)
    talep = mean*lead_time
    QUA=math.sqrt(2*orcsot*mean/holcost)
    Q_ref = -1
    R_reff = -1
    R=0
    
    while ((QUA - Q_ref) > 0.01) or ((R - R_reff) > 0.01):
        Q_ref = QUA
        R_reff = R
        if b =='Backorder':
            FRR = 1 - ((QUA * holcost) / (zarcost * mean))
        else:
            FRR = 1 - ((QUA * holcost) / ((zarcost * mean) + (QUA*holcost)))
        R = talep + (standartdev * stat.norm.ppf(FRR))
        z = ((R - talep) / standartdev)
        NRR = standartdev*(stat.norm.pdf(z) - z*(1 - stat.norm.cdf(z)))  # Calculating loss function using z.
        QUA = math.sqrt((2 * mean*(orcsot + (zarcost*NRR))) / holcost)
    if b=='Backorder':
        G = orcsot*mean/QUA + c*mean + holcost*(QUA/2 + R - talep) + zarcost*mean*NRR/QUA
    else:
        G = orcsot*mean/QUA + c*mean+ holcost*(QUA/2 + R - talep + NRR) + zarcost*mean*NRR/QUA    
    QUA = round(QUA,2)
    R = round(R,2)   
    G = round(G,2)
    return R,QUA,G

#QR_Solver_Normal(40,80,4,50,0.0225,5)
#R_Solver_Normal(200,100,25,50,2,25)

def QR_Solver_Uniform(talep, min_demand, max_demand, orcsot, holcost, zarcost,c,b):
    holcost = float(holcost)
    QUA = math.sqrt(2 * orcsot * talep / holcost)
    mean = (max_demand + min_demand)/2
    Q_ref = -1
    R = 0
    R_reff = -1

    while((QUA - Q_ref) > 0.001) or ((R - R_reff) > 0.001):
        Q_ref = QUA
        R_reff = R
        if b =='Backorder':
           FRR = 1 - ((QUA * holcost) / (zarcost * talep))
        else:
            FRR = 1 - ((QUA * holcost) / (zarcost * talep + (QUA*holcost)))
        R = (max_demand - min_demand) * FRR
        NRR = ((R**2)/(max_demand*2))-R+max_demand/2
        QUA = math.sqrt((2 * talep * (orcsot + zarcost * NRR)) / holcost)
    if b=='Backorder':
        G = orcsot*mean/QUA + c*mean + holcost*(QUA/2 + R - talep) + zarcost*mean*NRR/QUA
    else:
        G = orcsot*mean/QUA + c*mean+ holcost*(QUA/2 + R - talep + NRR) + zarcost*mean*NRR/QUA
    QUA = round(QUA,2)
    R = round(R,2)
    G = round(G,2)

    return R,QUA,G

    


# Example call with uniform distribution parameters
#QR_Solver_Uniform(800, 0, 200, 10, 2, 5)



def qrPoisson(m, k, h, p, t,c, l):
    Q = round(math.sqrt(2*k*m/h))
    Q_ref = -1
    mt = m*t
    R = 0
    R_ref = -1
    while ((Q - Q_ref) > 0.001) or ((R - R_ref) > 0.001):
        Q_ref = Q
        R_ref = R
        if l=='Backorder':
            R = poisson.ppf(1-(Q*h)/(p*m), mu=mt)
        else:
            R = poisson.ppf(1-(Q*h)/(Q*h + p*m), mu=mt) #mu mean ıf poisson dist.
        nR = 0
        nR_ref = -1
        x = R
        while (nR - nR_ref) > 0.001:
            nR_ref = nR
            x = x + 1
            nR = nR + (x - R)*poisson.pmf(x, mu=mt)
        Q = round(math.sqrt((2*m*(k+p*nR))/h))
    if  l=='Backorder':
        G = k*m/Q + c*m + h*(Q/2 + R - mt) + p*m*nR/Q
    else:
        G = k*m/Q + c*m + h*(Q/2 + R - mt + nR) + p*m*nR/Q
    Q = round(Q,2)
    R = round(R,2)
    G = round(G,2)
    return R,Q,G
normal_veriler = ["Please enter the mean: ", "Please enter the variance: ",
            "Please enter the ordering cost: ", "Please enter the holding cost: ", "Please enter the penalty cost: ",
              "Please enter the lead time:",'Please enter unit cost:']
uniform_veriler = ['Rate/year','Min Demand','Max Demand',"Please enter the ordering cost: ", "Please enter the holding cost: ",
                   "Please enter the penalty cost: ",
                        'Please enter unit cost:']
poisson_veriler = ['Mean:',"Please enter the ordering cost: ", "Please enter the holding cost: ",
                   "Please enter the penalty cost: ",
              "Please enter the lead time:",'Please enter unit cost:']
değerlern = []
değerleru = []
değerlerp = []

#/////////////////////
#GUI
root = Tk()

root.geometry('800x500')


def main():
    frame = Frame(root, width=800,height=500,bg='white')
    frame.place(x=0,y=0)
    for i in range(len(normal_veriler)):
        back_lablel = tk.Label(frame, text=normal_veriler[i])
        back_lablel.place(x=175,y=50+i*30)
        e = tk.Entry(frame)
        e.place(x=350,y=50+i*30)
        değerlern.append(e)
    l = tk.StringVar()
    backor = ['Backorder','Exccess Demand Lost']
    l.set(backor[0])
    backorder_kutusu = tk.OptionMenu(frame, l,*backor )
    backorder_kutusu.place(x=350,y=250)
    def hesaplan():
        x = float(değerlern[0].get())
        y = float(değerlern[1].get())
        z = float(değerlern[2].get())
        w = float(değerlern[3].get())
        u = float(değerlern[4].get())
        v = float(değerlern[5].get())
        f = float(değerlern[6].get())
        if l.get() == 'Backorder':
            o = 'Backorder'
            result = QR_Solver_Normal(x, y, z, w, u, v,f, o)
        else:
            o = 'Not Backordered'
            result = QR_Solver_Normal(x, y, z, w, u, v,f, o)
        #değerlern.clear()
        label = tk.Label(frame, text="R,Q,Cost:"+str(result))
        label.place(x=235, y=295) 
    calculation_button_n = tk.Button(frame, text="Calculate", command=hesaplan)
    calculation_button_n.place(x=235, y=265)
    btn1 = Button(frame,text="QR_Normal_Distribution",command=main)
    btn1.place(x=10,y=10)
    btn2 = Button(frame,text= "QR_Uniform_Distribution",command=screen1)
    btn2.place(x=10,y=50)
    btn3 = Button(frame,text="QR_Poisson_Distirubtion",command=screen2)
    btn3.place(x=10,y=80)

    lab = Label(frame,text="QR_Normal_Distribution")
    lab.place(x=300,y=10)

def screen1():
    frame1 = Frame(root, width=880,height=500,bg='white')
    frame1.place(x=0,y=0)
    for i in range(len(uniform_veriler)):
        back_lablel = tk.Label(frame1, text=uniform_veriler[i])
        back_lablel.place(x=175,y=50+i*30)
        e = tk.Entry(frame1)
        e.place(x=350,y=50+i*30)
        değerleru.append(e)
    l = tk.StringVar()
    backor = ['Backorder','Exccess Demand Lost']
    l.set(backor[0])
    backorder_kutusu = tk.OptionMenu(frame1, l,*backor )
    backorder_kutusu.place(x=350,y=250)
    def hesaplau():
        x = float(değerleru[0].get())
        y = float(değerleru[1].get())
        z = float(değerleru[2].get())
        w = float(değerleru[3].get())
        u = float(değerleru[4].get())
        v = float(değerleru[5].get())
        f = float(değerleru[6].get())
        if l.get() == 'Backorder':
            o = 'Backorder'
            result = QR_Solver_Uniform(x, y, z, w, u, v,f, o)
        else:
            o = 'Not Backordered'
            result = QR_Solver_Uniform(x, y, z, w, u, v,f, o)
        label = tk.Label(frame1, text="R,Q,Cost:"+str(result))
        label.place(x=235, y=275) 
    calculation_button_u = tk.Button(frame1, text="Calculate", command=hesaplau)
    calculation_button_u.place(x=235, y=295)

    btn1 = Button(frame1,text="QR_Normal_Distribution",command=main)
    btn1.place(x=10,y=10)
    btn2 = Button(frame1,text='QR_Uniform_Distribution',command=screen1)
    btn2.place(x=10,y=50)
    btn3 = Button(frame1,text="QR_Poisson_Distirubtion",command=screen2)
    btn3.place(x=10,y=80)
    
    lab = Label(frame1,text="QR_Uniform_Distribution")
    lab.place(x=300,y=10)

def screen2():
    frame2 = Frame(root, width=800,height=500,bg='white')
    frame2.place(x=0,y=0)
    for i in range(len(poisson_veriler)):
        back_lablel = tk.Label(frame2, text=poisson_veriler[i])
        back_lablel.place(x=175,y=50+i*30)
        e = tk.Entry(frame2)
        e.place(x=350,y=50+i*30)
        değerlerp.append(e)
    l = tk.StringVar()
    backor = ['Backorder','Exccess Demand Lost']
    l.set(backor[0])
    backorder_kutusu = tk.OptionMenu(frame2, l,*backor )
    backorder_kutusu.place(x=350,y=250)
    def hesaplap():
        x = float(değerlerp[0].get())
        y = float(değerlerp[1].get())
        z = float(değerlerp[2].get())
        w = float(değerlerp[3].get())
        u = float(değerlerp[4].get())
        v = float(değerlerp[5].get())
        if l.get() == 'Backorder':
            o = 'Backorder'
            result = qrPoisson(x, y, z, w, u,v,o)
        else:
            o = 'Not Backordered'
            result = qrPoisson(x, y, z, w, u,v, o)
        label = tk.Label(frame2, text="R,Q,Cost:"+str(result))
        label.place(x=235, y=275) 
    calculation_button_p = tk.Button(frame2, text="Calculate", command=hesaplap)
    calculation_button_p.place(x=235, y=295)

    btn1 = Button(frame2,text="QR_Normal_Distribution",command=main)
    btn1.place(x=10,y=10)
    btn2 = Button(frame2,text='QR_Uniform_Distribution',command=screen1)
    btn2.place(x=10,y=50)
    btn3 = Button(frame2,text="QR_Poisson_Distirubtion",command=screen2)
    btn3.place(x=10,y=80)

    lab = Label(frame2,text="QR_Poisson_Distirubtion")
    lab.place(x=300,y=10)

main()


root.mainloop()