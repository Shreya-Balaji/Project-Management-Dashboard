import tkinter as tk
import pymysql
from tkinter import ttk
import matplotlib as plt
from PIL import ImageTk, Image
plt.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle
#import numpy as np
from datetime import datetime
from datetime import date
top=tk.Tk()
#Main Title Code
top.title("21BCE6167-Dashboard")
tk.Label(top, text="PROJECT DASHBOARD",bg='light green', fg='black', pady=10, padx=10,font=("Arial",40,'bold')).pack()
top.geometry("1745x775")
top.state('zoomed')
#Connect to Database
conn=pymysql.connect(host='localhost',user='root',password='give your password',db='project')
cur=conn.cursor()
#Display Project Title
cur.execute("select title from project1 where pid=1")
output=cur.fetchall()
for row in output:
    for i in row:
        tk.Label(top, text=i,fg='dark green',font=('Arial',30,'bold')).pack()
#Display Head of Project
cur.execute("select head from project1 where pid=1")
output=cur.fetchall()
for row in output:
    for i in row:
        tk.Label(top, text="Lead by "+i,fg='black',font=('Arial',18)).pack()
#Display Team Details- ID, NAME, ROLE as a Table
cur.execute("select eid,name,role from employee where pid=1")
output=cur.fetchall()
frame = ttk.Frame(top)
frame.pack(side="left", padx=0, pady=0,fill='both',expand=False)
style = ttk.Style()
tree = ttk.Treeview(frame,height=5,show='headings')
style.configure("Custom.Treeview",font=("Arial", 12, "bold"))
style.configure("Custom.Treeview.Heading",font=("Arial", 12, "bold"))
tree["style"] = "Custom.Treeview"
columns = ("EID", "Name", "Role")
tree["columns"] = columns
for col in columns:
    tree.heading(col, text=col, anchor="w")
    tree.column(col, anchor="w",width=140)
for row in output:
    tree.insert("","end", values=row[0:])
tree.pack(fill='both',expand=False)

#Display Budget Details
cur.execute("SELECT total, remaining, ideal  FROM budget where pid=1")
data = cur.fetchall()
values=['Total','Actual Remaining','Ideal Remaining']
for i in data:
    data=list(i)
fig = Figure(figsize=(4, 3))
ax = fig.add_subplot(111)
ax.bar(values, data, color='green', width=0.2)
ax.tick_params(axis='x',labelsize=5)
ax.set_xlabel("Total vs Actual vs Ideal",fontsize=8)
ax.set_ylabel("Amount in INR",fontsize=8)
ax.set_title("Project Budget")
fig_canvas = FigureCanvasTkAgg(fig, master=top)
fig_canvas.draw()
fig_canvas.get_tk_widget().place(x=0,y=320)
over=0
amount=0
if data[1]<data[2]:
    over= ((data[2] - data[1]) / data[0]) * 100
    amount=data[2]-data[1]
over="{:.2f}".format(over)
overs="Over Target = "+str(over)+"%"
amount="Amount = Rs. "+str(amount)
label=tk.Label(top,text=overs)
label.config(fg='red',font=("Arial",12,'bold'))
label.place(x=0,y=625)
label=tk.Label(top,text=amount)
label.config(fg='red',font=("Arial",12,'bold'))
label.place(x=0,y=650)

#place flag, launch_date, countdown
image = Image.open(r"give loaction of the image")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)
label = tk.Label(top, image=photo)
label.place(x=5,y=5)
cur.execute("Select start,end from project1 where pid=1")
data1=cur.fetchall()
data_from_mysql = data1
date1, date2 = data_from_mysql[0]
delta = date2 - date.today()
num_days = delta.days
formatted_date = date2.strftime("%d/%m/%Y")
label=tk.Label(top,text="Launch On")
label.config(fg='forestgreen',font=("Arial",26,'bold'))
label.place(x=150,y=5)
label=tk.Label(top,text=formatted_date)
label.config(fg='springgreen4',font=("Arial",20))
label.place(x=170,y=50)
text1=str(num_days)+" DAYS"
label=tk.Label(top,text=text1)
label.config(fg='dark green',font=("Arial",40))
label.place(x=130,y=80)

#Upcoming Deadline
cur.execute("select employee, task, deadline, workload from upcoming where pid=1")
data2=cur.fetchall()
frame1 = ttk.Frame(top)
frame1.pack(side="right", padx=0, pady=0,fill='both',expand=False)
tree1 = ttk.Treeview(frame1,height=3,show='headings')
style.configure("Custom.Treeview",font=("Arial", 10))
style.configure("Custom.Treeview.Heading",font=("Arial", 12, "bold"))
tree1["style"] = "Custom.Treeview"
columns1 = ("Employee", "Task", "Deadline","Workload in %")
tree1["columns"] = columns1
for col in columns1:
    tree1.heading(col, text=col, anchor="w")
    tree1.column(col, anchor="w",width=140)
for row in data2:
    tree1.insert("","end", values=row[0:])
tree1.pack()

#Workload graph
cur.execute("SELECT name,workload from workload where pid=1")
data = cur.fetchall()
#print(data)
xval=[]
yval=[]
for i in data:
    xval+=[i[0]]
    yval+=[i[1]]
#print(xval,yval)
fig = Figure(figsize=(4, 4))
ax = fig.add_subplot(111)
ax.bar(xval, yval, color='limegreen', width=0.3)
ax.set_xlabel("Employee Name",fontsize=8)
ax.set_ylabel("Workload in %",fontsize=8)
ax.set_title("Project Workload")
fig_canvas = FigureCanvasTkAgg(fig, master=top)
fig_canvas.draw()
fig_canvas.get_tk_widget().place(x=1050,y=270)

#Overdue Tasks
cur.execute("select employee, task, ideal from overdue where pid=1")
data3=cur.fetchall()
#print(data3)
data4=[]
current_datetime = datetime.now()
current_date = current_datetime.date()
for i in data3:
    if i[2]<current_date:
        val=(current_date-i[2]).days
        j=i+(val,)
        data4.append(j)
    else:
        j=i+(0,)
        data4.append(j)
#print(data4)
frame2 = ttk.Frame(top)
frame2.pack(side="bottom",anchor='ne', padx=0, pady=0,fill='both',expand=False)
tree2 = ttk.Treeview(frame2,height=3,show='headings')
style.configure("Custom.Treeview",font=("Arial", 10))
style.configure("Custom.Treeview.Heading",font=("Arial", 12, "bold"))
tree2["style"] = "Custom.Treeview"
columns2 = ("Employee", "Task", "Deadline","Overdue (in days)")
tree2["columns"] = columns2
w=[100,170,100,170]
for col,wi in zip(columns2,w):
    tree2.heading(col, text=col, anchor="w")
    tree2.column(col, anchor="w",width=wi)
for row in data4:
    tree2.insert("","end", values=row[0:])
tree2.pack(fill='both',expand=False)

#Phases Doughnut Chart
cur.execute('select planning, design, deployment, testing from phases where pid=1')
data5=cur.fetchall()
#print(data5)
plan=[]
design=[]
deploy=[]
test=[]
for i in data5:
    plan.append(i[0])
    plan.append(100-i[0])
    design.append(i[1])
    design.append(100-i[1])
    deploy.append(i[2])
    deploy.append(100-i[2])
    test.append(i[3])
    test.append(100-i[3])
#print(plan,design,deploy,test)
#Plan
key = ['Completed','Pending']
colors = ['green', 'greenyellow']
explode = (0.05, 0.05)
fig = Figure(figsize=(2, 2), dpi=100)
ax = fig.add_subplot(111)
_, _, autotexts = ax.pie(plan, colors=colors, labels=None,
                         autopct='%1.1f%%', pctdistance=0.85,
                         explode=explode)
for autotext in autotexts:
    autotext.set_fontsize(8)
ax.set_title('Planning Phase')
centre_circle = Circle((0, 0), 0.50, fc='white')
fig.gca().add_artist(centre_circle)
canvas = FigureCanvasTkAgg(fig, master=top)
canvas.draw()
canvas.get_tk_widget().place(x=450,y=200)
ax.legend(labels=key, loc='best')
#Design
key = ['Completed','Pending']
colors = ['green', 'greenyellow']
explode = (0.05, 0.05)
fig = Figure(figsize=(2, 2), dpi=100)
ax = fig.add_subplot(111)
_, _, autotexts = ax.pie(design, colors=colors, labels=None,
                         autopct='%1.1f%%', pctdistance=0.85,
                         explode=explode)
for autotext in autotexts:
    autotext.set_fontsize(8)
ax.set_title('Design Phase')
centre_circle = Circle((0, 0), 0.50, fc='white')
fig.gca().add_artist(centre_circle)
canvas = FigureCanvasTkAgg(fig, master=top)
canvas.draw()
canvas.get_tk_widget().place(x=750,y=200)
ax.legend(labels=key, loc='best')

#Deployment
key = ['Completed','Pending']
colors = ['green', 'greenyellow']
explode = (0.05, 0.05)
fig = Figure(figsize=(2, 2), dpi=100)
ax = fig.add_subplot(111)
_, _, autotexts = ax.pie(deploy, colors=colors, labels=None,
                         autopct='%1.1f%%', pctdistance=0.85,
                         explode=explode)
for autotext in autotexts:
    autotext.set_fontsize(8)
ax.set_title('Deployment Phase')
centre_circle = Circle((0, 0), 0.50, fc='white')
fig.gca().add_artist(centre_circle)
canvas = FigureCanvasTkAgg(fig, master=top)
canvas.draw()
canvas.get_tk_widget().place(x=450,y=450)
ax.legend(labels=key, loc='best')

#Testing
#Deployment
key = ['Completed','Pending']
colors = ['green', 'greenyellow']
explode = (0.05, 0.05)
fig = Figure(figsize=(2, 2), dpi=100)
ax = fig.add_subplot(111)
_, _, autotexts = ax.pie(test, colors=colors, labels=None,
                         autopct='%1.1f%%', pctdistance=0.85,
                         explode=explode)
for autotext in autotexts:
    autotext.set_fontsize(8)
ax.set_title('Testing Phase')
centre_circle = Circle((0, 0), 0.50, fc='white')
fig.gca().add_artist(centre_circle)
canvas = FigureCanvasTkAgg(fig, master=top)
canvas.draw()
canvas.get_tk_widget().place(x=750,y=450)
ax.legend(labels=key, loc='best')

top.mainloop()
cur.close()
conn.close()

