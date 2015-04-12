from flask import Flask,request,render_template


from flask import Flask,request,render_template,make_response
app=Flask(__name__)

import numpy.polynomial.polynomial as P
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import StringIO



@app.route('/')
def f():
    return render_template('Home.html',title="Home")
    

@app.route('/plot',methods=['GET','POST'])
def hello_world():

    if request.method=='GET':
        return render_template('get.html')

    elif request.method=='POST':
        points=request.form['points']
        return render_template('post.html',source='/plot/'+points,old_points=points)

    else:
        return 'Invalid Request'

@app.route('/plot/<points>')
def plot(points):

    s,X,F=points[:],[],[]
    while(s!=''):
        i=s.index('(')
        j=s.index(',',i)
        X.append(float(s[i+1:j]))
        k=s.index(')',j)
        F.append(float(s[j+1:k]))
        s=s[k+2:]

    fig=plt.figure()
    plt.clf()
    sub=fig.add_subplot(111)
    X1=np.arange(min(X)-2,max(X)+2,0.1)
    num_plots=len(X)
    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0.2, 0.9, num_plots)])
    x=[1.0]
    for i in range(len(X)):
        x=P.polymul(x,[-1*X[i],1])
    b=[0.0]
    for i in range(len(X)):
        a=P.polydiv(x,[-1*X[i],1])
        b=P.polyadd(P.polymul((P.polydiv(a[0],P.polyval(X[i],a[0])))[0],[F[i]]),b)
        Y=P.polyval(X1,P.polymul((P.polydiv(a[0],P.polyval(X[i],a[0])))[0],[F[i]]))
        sub.plot(X1,Y)

    Y=P.polyval(X1,b)
    Y1=P.polyval(np.arange(min(X),max(X)+0.1,0.1),b)
    interpol_obj=sub.plot(X1,Y,'k',linewidth=2)
    sub.plot(X,F,'ro',markersize=8)

    plt.grid(True)
    fig.legend(interpol_obj,['Interpolating Polynomial'],fancybox=True,shadow=True,loc='upper left')
    plt.axis([min(X)-3,max(X)+3,min(Y1)-2,max(Y1)+2])
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.title('Interpolate')
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response




@app.route('/average',methods=['GET','POST'])
def average():
    if request.method=='GET':
        return render_template("average.html",title='average',ans=" ")

    elif request.method=='POST':

        l=request.form['numbers']
##        newl=[]
##        a=[]
##        for i in l:
##                newl.append(i.split(',')[0])
##        for i in range(len(newl)):
##            if newl[i]:
##                a.apend(newl[i])
##        l=a[:]
           
        s=l[:]+','
        l=[]
        while(s!=''):
            i=s.index(',')
            l.append(float(s[:i]))
            s=s[i+1:]

        sum=0
        for item in l:
            sum=sum+item
            ans=float(sum)/len(l)
           
        return render_template("average.html",title='average',ans=ans)
    else:
        return "Invalid case"

@app.route('/team')
def team():
    return render_template('team_profile.html',title='team_profile')

@app.route('/contact')
def contacts():
    return render_template('contact.html',title='contact_page')



@app.route('/<name>')
def team_members(name):
    if name=='gaurav':
        return render_template('gaurav.html',title='Gaurav Gupta')
    if name=='arpit':
        return render_template('arpit.html',title='Arpit Choudhary')
    if name=='prakhar':
        return render_template('prakhar.html',title='Prakhar Gupta')


app.run()


