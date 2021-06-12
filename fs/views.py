from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import RegisterForm,UserForm,ForgetForm,OTPForm
from .models import Us,User,sug
import json
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
import plotly
import pandas as pd
from sqlalchemy import create_engine
import plotly.plotly as py
import plotly.graph_objs as go
import random
from django.http import FileResponse, Http404 ,HttpResponse
from reportlab.pdfgen import canvas
import os
from os import path
from datetime import datetime,timedelta
from datetime import date
from calendar import monthrange
import math 
from fusionexport import ExportManager, ExportConfig
from reportlab.lib.utils import ImageReader
from collections import OrderedDict
from fusioncharts import FusionCharts
import csv,ast

def home(request):
    return render(request, 'fs/home.html')

def y_pdf(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        k=vuser.username
        ye=date.today() - timedelta(days=1)
        ye=ye.strftime('%Y-%m-%d')
        d=str(ye)+".pdf"
        p=os.path.join("/home/me/final/media/media",k,d)
        if path.exists(p) == False:
            c = canvas.Canvas(p)
            gpdf(c,rt,ye,ye)
            os.remove('/home/me/final/media/media/'+k+'/export-1.png')
            os.remove('/home/me/final/media/media/'+k+'/export-2.png')
            os.remove('/home/me/final/media/media/'+k+'/export-3.png')
            os.remove('/home/me/final/media/media/'+k+'/export-4.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-1.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-2.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-3.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-4.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-5.png')
        try:
            return FileResponse(open(p,'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()
    
def m_pdf(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        k=vuser.username
        cm=datetime.now().month
        cy=datetime.now().year
        td=datetime.now().strftime('%Y-%m-%d')
        sd=str(cy)+"-"+"0"+str(cm)+"-"+"01"
        d=str(sd)+" to "+str(td)+".pdf"
        p=os.path.join("/home/me/final/media/media",k,d)
        if path.exists(p) == False:
            c = canvas.Canvas(p)
            gpdf(c,rt,sd,td)
            os.remove('/home/me/final/media/media/'+k+'/export-1.png')
            os.remove('/home/me/final/media/media/'+k+'/export-2.png')
            os.remove('/home/me/final/media/media/'+k+'/export-3.png')
            os.remove('/home/me/final/media/media/'+k+'/export-4.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-1.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-2.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-3.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-4.png')
            os.remove('/home/me/final/media/media/'+k+'/next/export-5.png')
        try:
            return FileResponse(open(p, 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()

def gpdf(c,k,sd,ld):
    vuser = get_object_or_404(Us,username=k)
    d=int(k[-4:])
    if d <= 5009 :
        un = int(k[-1:])
    else:
        un = int(k[-2:])
    s=int(vuser.pe)
    toc={}
    if s == 1 :
        toc[0]=2
        toc[1]=5
        toc[2]=3
    elif s == 2 :
        toc[0]=1
        toc[1]=6
        toc[2]=3
    elif s == 3 :
        toc[0]=1
        toc[1]=7
        toc[2]=2 
    elif s == 4 :
        toc[0]=1
        toc[1]=8
        toc[2]=1
    else:
        toc={}
    d=str(un)+".csv"
    b=str(un)+".db"
    p=os.path.join("/home/me/final/media/media",k,d)
    d1="sqlite:////home/me/final/media/media/"+k+"/"+str(un)+".db"
    disk_engine = create_engine(d1)
    m1 = pd.read_sql_query('SELECT count(DATE) as `c1` FROM set1 WHERE DATE BETWEEN (?) and (?) GROUP BY AUTHRESPONSE ORDER BY AUTHRESPONSE',disk_engine,params=(sd,ld,))
    m2 = pd.read_sql_query('SELECT count(DATE) as `c2` FROM set1 WHERE DATE BETWEEN (?) and (?) AND AUTHRESPONSE = 0 GROUP BY AGE ORDER BY AGE',disk_engine,params=(sd,ld,))
    m3 = pd.read_sql_query('SELECT count(DATE) as `c3` FROM set1 WHERE DATE BETWEEN (?) and (?) AND AUTHRESPONSE = 1 GROUP BY AGE ORDER BY AGE',disk_engine,params=(sd,ld,))
    m4 = pd.read_sql_query('SELECT count(DATE) as `c4` FROM set1 WHERE DATE BETWEEN (?) and (?)  AND AUTHRESPONSE = 0 GROUP BY STATE ORDER BY STATE',disk_engine,params=(sd,ld,))
    m5 = pd.read_sql_query('SELECT count(DATE) as `c5` FROM set1 WHERE DATE BETWEEN (?) and (?)  AND AUTHRESPONSE = 1 GROUP BY STATE ORDER BY STATE',disk_engine,params=(sd,ld,))
    m6 = pd.read_sql_query('SELECT count(DATE) as `c6` FROM set1 WHERE DATE BETWEEN (?) and (?)  AND AUTHRESPONSE = 0 GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(sd,ld,))
    m7 = pd.read_sql_query('SELECT count(DATE) as `c7` FROM set1 WHERE DATE BETWEEN (?) and (?)  AND AUTHRESPONSE = 1 GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(sd,ld,))
    m8 = pd.read_sql_query('SELECT count(DATE) as `c8` FROM set1 WHERE DATE BETWEEN (?) and (?) AND AUTHRESPONSE = 0 GROUP BY ERRORCODE ORDER BY ERRORCODE',disk_engine,params=(sd,ld,))
    k1 = pd.read_sql_query(' SELECT count(*) as cd1 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTHRESPONSE = 0 GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(sd,ld))
    k2= pd.read_sql_query(' SELECT count(*) as cd2 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTHRESPONSE = 1 GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(sd,ld))
    g=m1.c1.to_dict()
    g1=m2.c2.to_dict()
    g2=m3.c3.to_dict()
    g3=m4.c4.to_dict()
    g4=m5.c5.to_dict()
    g5=m6.c6.to_dict()
    g6=m7.c7.to_dict()
    g7=m8.c8.to_dict()
    g8=k1.cd1.to_dict()
    g9=k2.cd2.to_dict()
    q={0:'NUMBER OF FACEIMAGE DATA EXCEEDED BY 1',1:'MISSING PERSONAL INFORMATION',2:'MISSING PERSONAL ADDRESS',3:'INVALID DATE OF BIRTH',4:'TECHNICAL ERROR',5:'INVALID AADHAAR NUMBER',6:'OTP VALIDATION FAILED',
7:'BIOMETRIC DIDNOT MATCH',8:'BIOMETRIC LOCKED BY AADHAAR HOLDER',9:'INVALID BIOMETRICS DATA',10:'INVALID BIOMETRICS DATA IN CIDR SERVER',
        11:'DUPLICATE FINGER USED',12:'AADHAAR SUSPENDED BY AUTHORITY',13:'NUMBER of FINGER DATA SHOULD NOT EXCEEDED BY 10',14:'BEST FINGER DETECTION REQUIRED',
        15:'DEVICE KEY ROTATION POLICY',16:'AADHAAR CANCELLED'}
    p={0:'DEMOGRAPHIC AUTHENTICATION',1:'OTP BASED AUTHETICATION',2:'BIOMETRIC AUTHENTICATION'}
    x={0:'CHILDREN',1:'TEENAGER',2:'SENIOR-CITIZEN'}
    s={0:"Andhra Pradesh",1:"Arunachal Pradesh",2:"Assam",3:"Bihar",4:"Chandigarh",5:"Chhattisgarh",6:"Delhi",7:"Goa",8:"Gujarat",9:"Haryana",10:"Himachal Pradesh",11:"Jammu and Kashmir",
12:"Jharkhand",13:"Karnataka",14:"Kerala",15:"Madhya Pradesh",16:"Maharashtra",17:"Manipur",18:"Meghalaya",19:"Odisha",20:"Punjab",21:"Rajasthan",22:"Sikkim",23:"Tamil Nadu",
24:"Telangana",25:"Uttar Pradesh",26:"Uttarakhand",27:"West Bengal"}   
    aa=math.ceil((g[0]/(g[0]+g[1]))*100)
    dv=str(aa)+"%"
    ab=math.floor((g[1]/(g[0]+g[1]))*100)
    dv1=str(ab)+"%"
    js=[
    {
    "type": "angulargauge",
    "renderAt": "chart-container",
    "width": "1000",
    "height": "500",
    "dataFormat": "json",
    "dataSource": {
    "chart": {
        "lowerLimit": "0",
        "upperLimit": "100",
        "numberSuffix": "%",
        "theme": "fusion",
        "pivotFillColor":"#5599CC",
        "pivotFillAlpha":"100",
        "upperLimit":"100",
        "majorTMNumber":"9",
        "minorTMNumber":"4",
        "showValue":"1",
        "numberSuffix":"%"
    },
    "colorRange": {
        "color": [
            {
            "minValue": "0",
            "maxValue": "50",
            "code": "#F2726F"
            },
            {
            "minValue": "50",
            "maxValue": "75",
            "code": "#FFC533"
            },
            {
            "minValue": "75",
            "maxValue": "100",
            "code": "#62B58F"
            }
        ]
    },
    "dials": {
        "dial": [
            {
                "value": dv1
            }
        ]
    }
    }
    },
    {
    "type": "angulargauge",
    "renderAt": "chart-container",
    "width": "1000",
    "height": "500",
    "dataFormat": "json",
    "dataSource": {
    "chart": {
        "lowerLimit": "0",
        "upperLimit": "100",
        "numberSuffix": "%",
        "theme": "fusion",
        "pivotFillColor":"#5599CC",
        "pivotFillAlpha":"100",
        "upperLimit":"100",
        "majorTMNumber":"9",
        "minorTMNumber":"4",
        "showValue":"1",
        "numberSuffix":"%"
    },
    "colorRange": {
        "color": [
                    {
            "minValue": "75",
            "maxValue": "100",
            "code": "#F2726F"
            },
            {
            "minValue": "30",
            "maxValue": "75",
            "code": "#FFC533"
            },
            {
            "minValue": "0",
            "maxValue": "30",
            "code": "#62B58F"
            }
        ]
    },
    "dials": {
        "dial": [
            {
                "value": dv
            }
        ]
    }
    }
    },
    {
    "type": 'mscolumn2d',
    "renderAt": 'chart-container',
    "width": '500',
    "height": '500',
    "dataFormat": 'json',
    "dataSource": {
        "chart": {
            "theme": "fusion",
            "xAxisname": "AGE GROUP",
            "yAxisName": "Number Of Transaction",
            "plotFillAlpha": "80",
        },
        "categories": [{
            "category": [{
                "label": x[0]
            }, {
                "label": x[1]
            }, {
                "label": x[2]
            }]
        }],
        "dataset": [{
            "seriesname": "Negative Authentication",
            "data": [{
                "value": g1[0]
            }, {
                "value": g1[1]
            }, {
                "value": g1[2]
            }]
        }, {
            "seriesname": "Positive Authentication",
            "data": [{
                "value": g2[0]
            }, {
                "value": g2[1]
            }, {
                "value": g2[2]
            }]
        }],
    }
},
{
    "type": 'mscolumn2d',
    "renderAt": 'chart-container',
    "width": '800',
    "height": '500',
    "dataFormat": 'json',
    "dataSource": {
        "chart": {
            "theme": "fusion",
            "xAxisname": "STATE NAME",
            "yAxisName": "Number Of Transaction",
            "plotFillAlpha": "80",
        },
        "categories": [{
            "category": [{
                "label": s[0]
            }, {
                "label": s[1]
            }, {
                "label": s[2]
            }, {
                "label": s[3]
            }, {
                "label": s[4]
            }, {
                "label": s[5]
            }, {
                "label": s[6]
            }, {
                "label": s[7]
            }, {
                "label": s[8]
            }, {
                "label": s[9]
            }, {
                "label": s[10]
            }, {
                "label": s[11]
            }, {
                "label": s[12]
            }, {
                "label": s[13]
            }, {
                "label": s[14]
            }, {
                "label": s[15]
            }, {
                "label": s[16]
            }, {
                "label": s[17]
            }, {
                "label": s[18]
            }, {
                "label": s[19]
            }, {
                "label": s[20]
            }, {
                "label": s[21]
            }, {
                "label": s[22]
            }, {
                "label": s[23]
            }, {
                "label": s[24]
            }
            , {
                "label": s[25]
            }
            , {
                "label": s[26]
            }
            ,{
                "label": s[27]
            }]
        }],
        "dataset": [{
            "seriesname": "Positive Authentication",
            "data": [{
                "value": g4[0]
            }, {
                "value": g4[1]
            }, {
                "value": g4[2]
            }, {
                "value": g4[3]
            }, {
                "value": g4[4]
            },{
                "value": g4[5]
            }, 
            {
                "value": g4[6]
            }, {
                "value": g4[7]
            }, {
                "value": g4[8]
            }, {
                "value": g4[9]
            }, {
                "value": g4[10]
            }, {
                "value": g4[11]
            }, {
                "value": g4[12]
            }, {
                "value": g4[13]
            }, {
                "value": g4[14]
            }, {
                "value": g4[15]
            },{
                "value": g4[16]
            }, {
                "value": g4[17]
            }, {
                "value": g4[18]
            }, {
                "value": g4[19]
            }, {
                "value": g4[20]
            }, {
                "value": g4[21]
            }, {
                "value": g4[22]
            }, {
                "value": g4[23]
            }, {
                "value": g4[24]
            }, {
                "value": g4[25]
            }, {
                "value": g4[26]
            },
            {
                "value": g4[27]
            }]
        }, {
            "seriesname": "Negative Authentication",
            "data": [{
                "value": g3[0]
            }, {
                "value": g3[1]
            }, {
                "value": g3[2]
            }, {
                "value": g3[3]
            }, {
                "value": g3[4]
            }, {
                "value": g3[5]
            }, {
                "value": g3[6]
            }, {
                "value": g3[7]
            }, {
                "value": g3[8]
            }, {
                "value": g3[9]
            }, {
                "value": g3[10]
            }, {
                "value": g3[11]
            }, {
                "value": g3[12]
            }, {
                "value": g3[13]
            }, {
                "value": g3[14]
            }, {
                "value": g3[15]
            },{
                "value": g3[16]
            }, {
                "value": g3[17]
            }, {
                "value": g3[18]
            }, {
                "value": g3[19]
            }, {
                "value": g3[20]
            }, {
                "value": g3[21]
            }, {
                "value": g3[22]
            }, {
                "value": g3[23]
            }, {
                "value": g3[24]
            }, {
                "value": g3[25]
            }, {
                "value": g3[26]
            },
            {
                "value": g3[27]
            }]
        }],
    }
}]
    js2=[
{
    "type": "pie2d",
    "renderAt": "chart-container",
    "width": "1000",
    "height": "600",
    "dataFormat": "json",
    "dataSource": {
        "chart": {
            "showPercentInTooltip": "0",
            "decimals": "1",
            "useDataPlotColorForLabels": "1",
            "theme": "fusion"
        },
        "data": [{
                "label": p[0],
                "value": g6[0]
            },
            {
                "label": p[1],
                "value": g6[1]
            },
            {
                "label": p[2],
                "value": g6[2]
            }
        ]
    }
    },
    {
    "type": 'doughnut2d',
    "renderAt": 'chart-container',
    "width": '1000',
    "height": '600',
    "dataFormat": 'json',
    "dataSource": {
        "chart": {
            "bgColor": "#ffffff",
            "startingAngle": "310",
            "showLegend": "1",
            "defaultCenterLabel":str(g5[0]+g5[1]+g5[2]),
            "decimals": "0",
            "theme": "fusion"
        },
        "data": [{
            "label": p[0],
            "value": g5[0]
        }, {
            "label": p[1],
            "value": g5[1]
        }, {
            "label": p[2],
            "value": g5[2]
        }]
    }
},{
    "type": 'column2d',
    "renderAt": 'chart-container',
    "width": '500',
    "height": '800',
    "dataFormat": 'json',
    "dataSource": {
        "chart": {
            "theme": "fusion",
            "yAxisName": "NUmber Of Negative Transaction"
        },

        "data": [{
                "label": q[0],
                "value": g7[0]
            },
            {
                "label": q[1],
                "value": g7[1]
            },
            {
                "label": q[2],
                "value": g7[2]
            },
            {
                "label": q[3],
                "value": g7[3]
            },
            {
                "label": q[4],
                "value": g7[4]
            },
            {
                "label": q[5],
                "value": g7[5]
            }
            ,
            {
                "label": q[6],
                "value": g7[6]
            }
            ,
            {
                "label": q[7],
                "value": g7[7]
            }
            ,
            {
                "label": q[8],
                "value": g7[8]
            }
            ,
            {
                "label": q[9],
                "value": g7[9]
            }
            ,
            {
                "label": q[10],
                "value": g7[10]
            },
            {
                "label": q[11],
                "value": g7[11]
            },
            {
                "label": q[12],
                "value": g7[12]
            }
            ,
            {
                "label": q[13],
                "value": g7[13]
            },
            {
                "label": q[14],
                "value": g7[14]
            },
            {
                "label": q[15],
                "value": g7[15]
            }
            ,
            {
                "label": q[16],
                "value": g7[16]
            }
        ]
    }
},
 {
    "type": "mscolumnline3d",
    "renderAt": "chart-container",
    "width": "500",
    "height": "500",
    "dataFormat": "json",
    "dataSource": {
        "chart": {
            "theme": "fusion",
            "xAxisName": "AUTHENTICATION TYPE",
            "yAxisName": "PROFIT",
            "lineThickness": "2"
        },
        "categories": [
        {
            "category": [
                {
                    "label": p[0]
                },
                {
                    "label": p[1]
                },
                {
                    "label": p[2]
                }
            ]
        }],
        "dataset": [
        {
            "seriesname": "NUMBER OF POSITIVE AUTHENTICATION WIH AUTHETICATION TYPE",
            "data": [
                {
                    "value": g9[0]
                },
                {
                    "value": g9[1]
                },
                {
                    "value": g9[2]
                }
            ]
        },
        {
            "seriesname": "PROFIT",
            "renderas": "Line",
            "data": [
                {
                    "value": g9[0]*toc[0]
                },
                {
                    "value": g9[1]*toc[1]
                },
                {
                    "value": g9[2]*toc[2]
                }
            ]
        }
    ]
    }
    },
 {
    "type": "mscolumnline3d",
    "renderAt": "chart-container",
    "width": "500",
    "height": "500",
    "dataFormat": "json",
    "dataSource": {
        "chart": {
            "theme": "fusion",
            "xAxisName": "AUTHENTICATION TYPE",
            "yAxisName": "LOSS",
            "lineThickness": "2"
        },
        "categories": [
        {
            "category": [
                {
                    "label": p[0]
                },
                {
                    "label": p[1]
                },
                {
                    "label": p[2]
                }
            ]
        }],
        "dataset": [
        {
            "seriesname": "NUMBER OF NEGATIVE AUTHENTICATION WIH AUTHETICATION TYPE",
            "data": [
                {
                    "value": g8[0]
                },
                {
                    "value": g8[1]
                },
                {
                    "value": g8[2]
                }
            ]
        },
        {
            "seriesname": "LOSS",
            "renderas": "Line",
            "data": [
                {
                    "value": g8[0]*toc[0]
                },
                {
                    "value": g8[1]*toc[1]
                },
                {
                    "value": g8[2]*toc[2]
                }
            ]
        }
    ]
    }
    }]
    #Instantiate the ExportConfig class and add the required configurations
    export_config = ExportConfig()
    im=os.path.join("/home/me/final/media/media/",k)	im=os.path.join("/home/me/final/media/media/",k,”next”)
     # Provide path of the chart configuration which we have defined above.
    # You can also pass the same object as serialized JSON.
    export_config["chartConfig"] = js
    export_config["quality"] ="best"
    # Provide port and host of FusionExport Service
    export_server_host = "127.0.0.1"
    export_server_port = 1337

    # Instantiate the ExportManager class
    em = ExportManager(export_server_host, export_server_port)

    # Call the export() method with the export_config as an argument
    em.export(export_config,output_dir=im,unzip=True)
    logo = ImageReader('/home/me/final/fs/static/fs/images/logo.png')
    h1 = ImageReader('/home/me/final/media/media/'+k+'/export-1.png')
    h2 = ImageReader('/home/me/final/media/media/'+k+'/export-2.png')
    h3= ImageReader('/home/me/final/media/media/'+k+'/export-3.png')
    h4 = ImageReader('/home/me/final/media/media/'+k+'/export-4.png')
    c.setTitle("REPORT")

    c.setFont("Helvetica",25)


    c.drawImage(logo,0,730,width=150,height=100)

    c.drawCentredString(320,740,"REPORT(SUMMARY)")

    c.setFont("Helvetica",15)
    c.drawCentredString(520,740,ld)
    c.line(0,720,720,720)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,690,"POSITIVE AUTHENTICATION")
    c.drawImage(h1,40,400,width=500,height=250)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,360,"NEGATIVE AUTHENTICATION")
    c.drawImage(h2,40,50,width=500,height=250)



    c.showPage()

    c.setFont("Helvetica",25)


    c.drawImage(logo,0,730,width=150,height=100)

    c.drawCentredString(320,740,"REPORT(SUMMARY)")

    c.setFont("Helvetica",15)
    c.drawCentredString(520,740,ld)
    c.line(0,720,720,720)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,690,"AGE WISE RESPONSE")
    c.drawImage(h3,65,370,width=450,height=300)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,350,"STATE WISE RESPONSE")
    c.drawImage(h4,20,0,width=550,height=349)

    c.showPage()


    export_config["chartConfig"] = js2
    export_config["quality"] ="best"
    # Provide port and host of FusionExport Service
    export_server_host = "127.0.0.1"
    export_server_port = 1337

    # Instantiate the ExportManager class
    em = ExportManager(export_server_host, export_server_port)
    im=os.path.join("/home/me/final/media/media/",k,"next")
    # Call the export() method with the export_config as an argument
    em.export(export_config,output_dir=imn,unzip=True)
    h5 = ImageReader('/home/me/final/media/media/'+k+'/next/export-1.png')
    h6 = ImageReader('/home/me/final/media/media/'+k+'/next/export-2.png')
    h7= ImageReader('/home/me/final/media/media/'+k+'/next/export-3.png')
    h8 = ImageReader('/home/me/final/media/media/'+k+'/next/export-4.png')
    h9 = ImageReader('/home/me/final/media/media/'+k+'/next/export-5.png')
    #c.drawImage(self, image , x,y, width=None,height=None,mask=None)
    c.setFont("Helvetica",25)
    c.drawImage(logo,0,730,width=150,height=100)

    c.drawCentredString(320,740,"REPORT(SUMMARY)")

    c.setFont("Helvetica",15)
    c.drawCentredString(520,740,ld)
    c.line(0,720,720,720)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,690,"NEGATIVE RESPONSE")

    c.drawImage(h5,60,390,width=500,height=300)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,370,"LOSS")
    c.drawImage(h9,30,10,width=500,height=350)

    c.showPage()


    c.setFont("Helvetica",25)


    c.drawImage(logo,0,730,width=150,height=100)

    c.drawCentredString(320,740,"REPORT(SUMMARY)")

    c.setFont("Helvetica",15)
    c.drawCentredString(520,740,ld)
    c.line(0,720,720,720)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,690,"POSITIVE RESPONSE")

    c.drawImage(h6,60,390,width=500,height=300)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,370,"PROFIT")
    c.drawImage(h8,30,10,width=500,height=350)

    c.showPage()



    c.setFont("Helvetica",25)


    c.drawImage(logo,0,730,width=150,height=100)

    c.drawCentredString(320,740,"REPORT(SUMMARY)")

    c.setFont("Helvetica",15)
    c.drawCentredString(520,740,ld)
    c.line(0,720,720,720)

    c.setFont("Helvetica",20)
    c.drawCentredString(275,690,"ERROR CODE")
    c.drawImage(h7,0,10,width=550,height=600)
    c.showPage()
    c.save()
    return c

def al(request):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        data = Us.objects.all().order_by('is_act')
        u = { "pk": data }
        return render(request,'fs/adminlogin.html',u)

def ul(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = Us.objects.get(username=rt)
        s=int(vuser.pe)
        toc={}
        z={}
        k=vuser.username
        d=int(k[-4:])
        if d <= 5009 :
            un = int(k[-1:])
        else:
            un = int(k[-2:])
        pa="/home/me/final/media/media/"+k+"/l.csv"
        if os.path.exists(pa):
            with open(pa,'r') as f:
                w=csv.DictReader(f)
                for r in w:
                    z=dict(r)
            f.close()
            z={ int(k):str(v) for k,v in z.items() }
        else:
            if s == 1 :
                toc[0]=2
                toc[1]=5
                toc[2]=3
            elif s == 2 :
                toc[0]=1
                toc[1]=6
                toc[2]=3
            elif s == 3 :
                toc[0]=1
                toc[1]=7
                toc[2]=2 
            elif s == 4 :
                toc[0]=1
                toc[1]=8
                toc[2]=1
            else:
                toc={}
            d1="sqlite:////home/me/final/media/media/"+k+"/"+str(un)+".db"
            disk_engine = create_engine(d1)
            td=datetime.now().strftime('%Y-%m-%d')
            ye=date.today() - timedelta(days=1)
            ye=ye.strftime('%Y-%m-%d')
            cm=datetime.now().month
            cy=datetime.now().year
            sd=str(cy)+"-"+"0"+str(cm)+"-"+"01"
            yy = pd.read_sql_query(' SELECT count(DATE) as `c1` FROM set1 WHERE DATE = (?) ',disk_engine,params=(ye,))
            tt = pd.read_sql_query(' SELECT count(DATE) as `c2` FROM set1 WHERE DATE = (?) ',disk_engine,params=(td,))
            mm = pd.read_sql_query(' SELECT count(DATE) as `c3` FROM set1 WHERE DATE BETWEEN (?) and (?)',disk_engine,params=(sd,td,))
            h1 = pd.read_sql_query(' SELECT count(AUTHRESPONSE) as `c4` FROM set1 WHERE AUTHRESPONSE = 0 AND DATE BETWEEN (?) and (?)',disk_engine,params=(sd,td,))
            h2 = pd.read_sql_query(' SELECT count(AUTHRESPONSE) as `c5` FROM set1 WHERE AUTHRESPONSE = 1 AND DATE BETWEEN (?) and (?)',disk_engine,params=(sd,td,))
            z={1:int(tt.c2),2:int(yy.c1),3:int(mm.c3)}
            aa=math.floor((h2.c5/mm.c3)*100)
            dv=str(aa)+"%"
            dataSource = OrderedDict()
            widgetConfig = OrderedDict()
            widgetConfig["caption"] = "Positive-Authentication-Meter"
            widgetConfig["lowerLimit"] = "0"
            widgetConfig["pivotFillColor"]="#5599CC"
            widgetConfig["pivotFillAlpha"]="100"
            widgetConfig["upperLimit"] = "100"
            widgetConfig["majorTMNumber"]="9",
            widgetConfig["minorTMNumber"]="4"
            widgetConfig["showValue"] = "1"
            widgetConfig["numberSuffix"] = "%"
            widgetConfig["theme"] = "fusion"
            colorRangeData = OrderedDict()
            colorRangeData["color"] = [{
            "minValue": "0",
            "maxValue": "50",
            "code": "#F2726F"
            },
            {
            "minValue": "50",
            "maxValue": "75",
            "code": "#FFC533"
            },
            {
            "minValue": "75",
            "maxValue": "100",
            "code": "#62B58F"
            }
            ]
            dialData = OrderedDict()
            dialData["dial"] = []
            dataSource["chart"] = widgetConfig
            dataSource["colorRange"] = colorRangeData
            dataSource["dials"] = dialData
            dialData["dial"].append({"value":dv})
            angulargaugeWidget = FusionCharts("angulargauge", "myFirstWidget", "100%", "250", "positive-meter", "json", dataSource)
            z[4]=angulargaugeWidget.render()
            aa=math.ceil((h1.c4/mm.c3)*100)
            dv=str(aa)+"%"
            dataSource = OrderedDict()
            widgetConfig = OrderedDict()
            widgetConfig["caption"] = "Negative-Authentication-Meter"
            widgetConfig["lowerLimit"] = "0"
            widgetConfig["pivotFillColor"]="#5599CC"
            widgetConfig["pivotFillAlpha"]="100"
            widgetConfig["upperLimit"] = "100"
            widgetConfig["majorTMNumber"]="9",
            widgetConfig["minorTMNumber"]="4"
            widgetConfig["showValue"] = "1"
            widgetConfig["numberSuffix"] = "%"
            widgetConfig["theme"] = "fusion"
            colorRangeData = OrderedDict()
            colorRangeData["color"] = [{
            "minValue": "75",
            "maxValue": "100",
            "code": "#F2726F"
            },
            {
            "minValue": "30",
            "maxValue": "75",
            "code": "#FFC533"
            },
            {
            "minValue": "0",
            "maxValue": "30",
            "code": "#62B58F"
            }
            ]
            dialData = OrderedDict()
            dialData["dial"] = []
            dataSource["chart"] = widgetConfig
            dataSource["colorRange"] = colorRangeData
            dataSource["dials"] = dialData
            dialData["dial"].append({"value":dv})
            angulargaugeWidget = FusionCharts("angulargauge", "myFirstWidget1", "100%", "250", "negative-meter", "json", dataSource)
            z[5]=angulargaugeWidget.render()
            h3 = pd.read_sql_query(' SELECT AUTH_TYPE,COUNT(AUTH_TYPE) as `c6` FROM set1 WHERE DATE = (?)  GROUP BY AUTH_TYPE  ORDER BY AUTH_TYPE ',disk_engine,params=(td,))
            da=h3.AUTH_TYPE.to_dict()
            dt=h3.c6.to_dict()
            p={2:'DEMOGRAPHIC AUTHENTICATION',3:'BIOMETRIC AUTHENTICATION',4:'OTP BASED AUTHETICATION'}
            chartData = OrderedDict()
            for i in da:
                for j in p:
                    if da[i]==j:
                        chartData[p[j]]=dt[i]
            dataSource = OrderedDict()
            chartConfig = OrderedDict()
            chartConfig["caption"] = "AUTHENTICATION-TYPE"
            chartConfig["subCaption"] = "TODAY-RESPONSE"
            chartConfig["xAxisName"] = "TYPE OF AUTHENTICATION"
            chartConfig["yAxisName"] = "Number_Of_Transaction"
            chartConfig["theme"] = "fusion"
            dataSource["chart"] = chartConfig
            dataSource["data"] = []
            for key, value in chartData.items():
                data = {}
                data["label"] = key
                data["value"] = value
                dataSource["data"].append(data)
            pie2D = FusionCharts("pie2d", "myFirstChart1", "100%", "450", "auth-piechart", "json", dataSource)
            z[6]=pie2D.render()
            k1 = pd.read_sql_query(' SELECT DATE,count(*) as cd1 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTH_TYPE = 2 AND AUTHRESPONSE = 1 GROUP BY DATE ORDER BY DATE',disk_engine,params=(sd,td))
            k2 = pd.read_sql_query(' SELECT count(*) as cd2 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTH_TYPE = 3 AND AUTHRESPONSE = 1 GROUP BY DATE ORDER BY DATE',disk_engine,params=(sd,td))
            k3 = pd.read_sql_query(' SELECT count(*) as cd3 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTH_TYPE = 4 AND AUTHRESPONSE = 1 GROUP BY DATE ORDER BY DATE',disk_engine,params=(sd,td))
            trace1 = go.Bar(
                    x=k1.DATE,
                    y=k1.cd1,
                    name='DEMOGRAPHIC AUTHENTICATION'
                )
            trace2 = go.Bar(
                x=k1.DATE,
                y=k2.cd2,
                name='OTP AUTHENTICATION'
            )
            trace3= go.Bar(
                x=k1.DATE,
                y=k3.cd3,
                name='BIOMETRIC AUTHENTICATION'
            )
            trace4= go.Scatter(
                x=k1.DATE,
                y=(k1.cd1*toc[0]),
                name='DEMOGRAPHIC PROFIT AUTHENTICATION',
                yaxis='y2'
            )
            trace5= go.Scatter(
                x=k1.DATE,
                y=(k2.cd2*toc[1]),
                name='OTP PROFIT AUTHENTICATION',
                yaxis='y2'
            )
            trace6= go.Scatter(
                x=k1.DATE,
                y=(k3.cd3*toc[2]),
                name='BIOMETRIC PROFIT AUTHENTICATION',
                yaxis='y2'
            )
            data = [trace1,trace2,trace3,trace4,trace5,trace6]
            layout = go.Layout(
                legend=dict(x=-0.1,y=-0.5,orientation="h"),
                barmode='group',
                title='Transaction',
                yaxis=dict(
                    title='Number OF Transaction'
                ),
                yaxis2=dict(
                    title='Profit In Rs',
                    titlefont=dict(
                        color='rgb(148, 103, 189)'
                    ),
                    tickfont=dict(
                        color='rgb(148, 103, 189)'
                    ),
                    overlaying='y',
                    side='right'
                )
            )

            fig = go.Figure(data=data, layout=layout)
            z[7]=plotly.offline.plot(fig,auto_open=False,include_plotlyjs=False,output_type='div')
            df = pd.read_sql_query('SELECT COUNT(*) as `n1` FROM set1 WHERE AUTHRESPONSE = 0 AND DATE BETWEEN (?) AND (?) GROUP BY AGE ORDER BY AGE',disk_engine,params=(sd,td))
            dk = pd.read_sql_query('SELECT COUNT(*) as `n2` FROM set1 WHERE AUTHRESPONSE = 1 AND DATE BETWEEN (?) AND (?) GROUP BY AGE ORDER BY AGE',disk_engine,params=(sd,td))
            trace11 = go.Bar(
                                x=['CHILDREN','TEENAGER','SENIOR-CITIZEN'],
                                y=df.n1,
                                width=[0.3,0.3,0.3],
                                name='NEGATIVE_AUTH_RESPONSE',
                                textposition = 'auto',
                                marker=dict(
                                    color='red',
                                    line=dict(
                                    color='red',
                                    width=0.5),
                                ),
                                opacity=0.6
            )
            trace12 = go.Bar(    
                                x=['CHILDREN','TEENAGER','SENIOR-CITIZEN'],
                                y=dk.n2,
                                width=[0.3,0.3,0.3],
                                textposition = 'auto',
                                marker=dict(
                                    color='green',
                                    line=dict(
                                    color='green',
                                    width=0.5),
                                ),
                                opacity=0.6,
                                name='POSITIVE_AUTH_RESPONSE'
            )
            data1 = [trace11, trace12]
            layout1 = go.Layout(
                                xaxis={'title': 'AGE-GROUP'},
                                yaxis={'title': 'NO.OF TRANSACTION'},
                                barmode='group',
                                legend=dict(x=-0.1,y=-0.5,orientation="h"),
                                title='AGE-WISE-AUTHENTICATION(MONTHLY)'
            )
            fig1= go.Figure(data=data1, layout=layout1)
            z[8]=plotly.offline.plot(fig1,auto_open=False,include_plotlyjs=False,output_type='div')
            with open(pa,'w') as f:
                            fn=[1,2,3,4,5,6,7,8]
                            w=csv.DictWriter(f,fieldnames=fn)
                            w.writeheader()
                            w.writerow(z)
        return render(request, 'fs/userlogin.html',{'output':z})

def open_pdf(request,value):
    command = 'echo ' + value.strip() + '| clip'
    os.system(command)
    try:
        return FileResponse(open('/home/me/final/media/media/list.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def update_user(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        if request.method == "POST":
            e = request.POST['em']
            c = request.POST['cn']
            r = request.POST['rl']
        vuser = get_object_or_404(Us,username=rt)
        vuser.em = e 
        vuser.cn = c
        vuser.rl = r
        vuser.save()
        data = Us.objects.all().order_by('is_act')
        u = { "pk": data }
        return render(request,'fs/adminlogin.html',u)

def del_user(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        vuser.delete()
        main = User.objects.get(username=rt)
        main.delete()
        data = Us.objects.all().order_by('is_act')
        u = { "pk": data }
        return render(request,'fs/adminlogin.html',u)

def deactivate_user(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        vuser.is_act = False 
        vuser.save()
        data = Us.objects.all().order_by('is_act')
        u = { "pk": data }
        return render(request,'fs/adminlogin.html',u)



def send_ma(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        if request.method == "POST":
            p = request.POST['pe']
            vuser.pe = int(p) 
        vuser.is_act = True 
        vuser.save()
        content1 = "THANK YOU FOR REGISTERING WITH US !\n\n WELCOME TO OUR FAMILY AND EXPLORE YOUR BUSINESS !\n \nCREDENTIALS DETAILS ARE  \n USERID:  "
        content2="\nPASSWORD:  "
        send_mail('ACCOUNT VERIFIED',content1 + vuser.username + content2 + vuser.password, 'admin@analyticsking.com', [vuser.em])
        data = Us.objects.all().order_by('is_act')
        u = { "pk": data }
        return render(request,'fs/adminlogin.html',u)

def logout_user(request):
    logout(request)
    return render(request, 'fs/index.html',{'error_message': 'THANK YOU !! VISIT AGAIN'})

def register(request):
    form = RegisterForm(request.POST or None,request.FILES)
    
    if form.is_valid():
        user = form.save(commit=False)
        cn = form.cleaned_data['cn']
        em = form.cleaned_data['em']
        rl = form.cleaned_data['rl']
        ic = request.FILES['ic']
        k="PR5000"
        All_U = Us.objects.all().order_by('username')
        for i in All_U:
            if i.em == em :
                return render(request, 'fs/index.html',{'error_message': 'The Email ID Provided Is All Registered'})
            if i.cn == cn :
                return render(request, 'fs/index.html',{'error_message': 'Company Name Provided Is All Registered'})
            k=i.username
        d=int(k[-4:])
        if d <= 5009 :
            un = "PR"+str(d+1)
        else:
            un = "PR"+str(d+1)
        pwd = (User.objects.make_random_password())+str(random.randint(0,9))
        user.username=un
        user.password=pwd
        main = User.objects.create_user(un)
        main.save()
        u = User.objects.get(username=un)
        u.set_password(pwd)
        u.save()
        user.save()
        content1 = "USER REGISTERED WITH US \n USERID:  "
        content2="\nPASSWORD:  "
        #send_mail('URGENT: VERFICATION SOON',content1 + user.username + content2 + user.password, 'admin@analyticsking.com', ['vishalmali858@gmail.com','karaderahul05@gmail.com','manchekarsaurabh@gmail.com','krunalsarvaiya0804@gmail.com'])
        return render(request, 'fs/index.html',{'error_message': 'An Email With Userid And Password Will Be Send Once Verified By The Admin'})
    else:
        return render(request, 'fs/signup.html')

def rl(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        k=vuser.username
        s=int(vuser.pe)
        toc={}
        if s == 1 :
            toc[0]=2
            toc[1]=5
            toc[2]=3
        elif s == 2 :
            toc[0]=1
            toc[1]=6
            toc[2]=3
        elif s == 3 :
            toc[0]=1
            toc[1]=7
            toc[2]=2 
        elif s == 4 :
            toc[0]=1
            toc[1]=8
            toc[2]=1
        else:
            toc={}
        d=int(k[-4:])
        if d <= 5009 :
            un = int(k[-1:])
        else:
            un = int(k[-2:])
        d1="sqlite:////home/me/final/media/media/"+k+"/"+str(un)+".db"
        disk_engine = create_engine(d1)
        td=datetime.now().strftime('%Y-%m-%d')
        cm=datetime.now().month
        cy=datetime.now().year
        cs=monthrange(cy,cm)
        cs=cs[1]
        z={}
        last_hour_date_time = datetime.now() - timedelta(hours = 1)
        ct=last_hour_date_time.strftime('%H:%M:%S')
        lt=datetime.now().strftime('%H:%M:%S')
        k1 = pd.read_sql_query(' SELECT AUTH_TYPE,TIME,AUTHRESPONSE FROM set1 WHERE TIME BETWEEN (?) AND (?) AND DATE = (?)',disk_engine,params=(ct,lt,td))
        r10=k1.TIME.to_dict()
        r11=k1.AUTH_TYPE.to_dict()
        r12=k1.AUTHRESPONSE.to_dict() 
        js_data = json.dumps(r10)
        z[0]=js_data
        js_data1 = json.dumps(r11)      
        z[1]=js_data1
        js_data2 = json.dumps(r12)      
        z[2]=js_data2
        js_data3 = json.dumps(toc)
        z[3]=js_data3
        return render(request, 'fs/rl.html',{'data':z})

def mp(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        k=vuser.username
        s=int(vuser.pe)
        toc={}
        z={}
        e=0
        pa="/home/me/final/media/media/"+k+"/m.csv"
        if os.path.exists(pa):
            with open(pa,'r') as f:
                w=csv.DictReader(f)
                for r in w:
                    m=dict(r)
            f.close()
            for k,v in m.items():
                if int(k) >= 5 and int(k) <=66:
                    s=ast.literal_eval(v)
                    z[int(k)]=s 
                else:
                    z[int(k)]=str(v)
                e=e+1
        else:    
            if s == 1 :
                toc[0]=2
                toc[1]=5
                toc[2]=3
            elif s == 2 :
                toc[0]=1
                toc[1]=6
                toc[2]=3
            elif s == 3 :
                toc[0]=1
                toc[1]=7
                toc[2]=2 
            elif s == 4 :
                toc[0]=1
                toc[1]=8
                toc[2]=1
            else:
                toc={}
            d=int(k[-4:])
            if d <= 5009 :
                un = int(k[-1:])
            else:
                un = int(k[-2:])
            d1="sqlite:////home/me/final/media/media/"+k+"/"+str(un)+".db"
            disk_engine = create_engine(d1)
            td=datetime.now().strftime('%Y-%m-%d')
            cm=datetime.now().month
            cy=datetime.now().year
            sd=str(cy)+"-"+"0"+str(cm)+"-"+"01"
            z={}
            h4 = pd.read_sql_query(' SELECT COUNT(*) as `c7` FROM set1 WHERE DATE BETWEEN (?) and (?) AND AUTHRESPONSE = 0 GROUP BY STATE ORDER BY STATE ',disk_engine,params=(sd,td))
            k=h4.c7.to_dict()
            k[28]=0
            dataSource = OrderedDict()
            mapConfig = OrderedDict()
            mapConfig["caption"] = "Negative Authentication"
            mapConfig["subcaption"] = "MONTHLY NEGATIVE TRANSACTON"
            mapConfig["entitytooltext"]="$lname: <b> $dataValue </b> Monthly Negative Transaction"
            mapConfig["labelsepchar"] = ":"
            mapConfig["theme"] = "fusion"
            colorDataObj = {
                "minvalue": "5000",
                "startlabel": "Low",
                "endlabel": "High",
                "code": "#FF4411",
                "gradient": "1",
                "color": [{
                        "minValue": "5000",
                        "maxValue": "7000",
                        "code": "#00c0f9"
                    },
                    {
                        "minValue": "7000",
                        "maxValue": "15000",
                        "code": "#23f527"
                    },
                    {
                        "minValue": "15000",
                        "maxValue": "20000",
                        "code": "#00e3f7"
                    }
                ]
            }
            dataSource["colorrange"] = colorDataObj
            dataSource["chart"] = mapConfig
            dataSource["data"] = []
            mapDataArray = [
                ["002", k[0], "1"],
                ["003", k[1], "1"],
                ["004", k[2], "1"],
                ["005", k[3], "1"],
                ["006", k[4], "1"],
                ["007", k[5], "1"],
                ["010", k[6], "1"],
                ["011",k[7], "1"],
                ["012", k[8], "1"],
                ["013",k[9], "1"],
                ["014",k[10], "1"],
                ["015",5100, "1"],
                ["016",k[12], "1"],
                ["017",k[13], "1"],
                ["018",k[14], "1"],
                ["020",k[15], "1"],
                ["021",k[16], "1"],
                ["023",k[26], "1"],
                ["026",9500, "1"],
                ["028",k[18], "1"],
                ["029",k[19], "1"],
                ["030",k[20], "1"],
                ["031",k[21], "1"],
                ["033",k[22], "1"],
                ["034",k[23], "1"],
                ["035",k[24], "1"],
                ["036",k[25], "1"],
                ["027",k[27], "1"]
            ]
            for i in range(len(mapDataArray)):
                dataSource["data"].append({
                    "id": mapDataArray[i][0],
                    "value": mapDataArray[i][1],
                    "showLabel": mapDataArray[i][2]
                })
            fusionMap = FusionCharts("maps/india", "myFirstMap", "500", "640", "l1", "json", dataSource)
            z[2]=fusionMap.render()
            s={10:"Andhra Pradesh",11:"Arunachal Pradesh",12:"Assam",13:"Bihar",14:"Chandigarh",15:"Chhattisgarh",16:"Delhi",17:"Goa",18:"Gujarat",19:"Haryana",20:"Himachal Pradesh",21:"Jammu and Kashmir",
    22:"Jharkhand",23:"Karnataka",24:"Kerala",25:"Madhya Pradesh",26:"Maharashtra",27:"Manipur",28:"Meghalaya",29:"Odisha",30:"Punjab",31:"Rajasthan",32:"Sikkim",33:"Tamil Nadu",
    34:"Telangana",35:"Uttar Pradesh",36:"Uttarakhand",37:"West Bengal"}
            l=4
            for f in range(2,5):
                h5 = pd.read_sql_query(' SELECT COUNT(*) as `c8` FROM set1 WHERE DATE BETWEEN (?) and (?) AND AUTHRESPONSE = 0 AND AUTH_TYPE = (?) GROUP BY STATE ORDER BY STATE ',disk_engine,params=(sd,td,f))
                z[l]=h5.c8.to_dict()
                l=l+1 
            h4 = pd.read_sql_query(' SELECT COUNT(*) as `c7` FROM set1 WHERE DATE BETWEEN (?) and (?) AND AUTHRESPONSE = 1 GROUP BY STATE ORDER BY STATE ',disk_engine,params=(sd,td))
            l=7
            for f in range(2,5):
                h5 = pd.read_sql_query(' SELECT COUNT(*) as `c9` FROM set1 WHERE DATE BETWEEN (?) and (?) AND AUTHRESPONSE = 1 AND AUTH_TYPE = (?) GROUP BY STATE ORDER BY STATE ',disk_engine,params=(sd,td,f))
                z[l]=h5.c9.to_dict()
                l=l+1
            u=10
            for f in range(0,28):
                z[u]={0:s[u],1:z[7][f],2:z[8][f],3:z[9][f]}
                u=u+1
            u=38
            er=10
            for f in range(0,28):
                z[u]={0:s[er],1:z[4][f],2:z[5][f],3:z[6][f]}
                er=er+1
                u=u+1
            z[66]=toc
            k=h4.c7.to_dict()
            k[28]=0
            dataSource = OrderedDict()
            mapConfig = OrderedDict()
            mapConfig["caption"] = "Positive Authentication"
            mapConfig["subcaption"] = "MONTHLY Positive TRANSACTON"
            mapConfig["entitytooltext"]="$lname: <b> $dataValue </b> Monthly Positive Transaction"
            mapConfig["labelsepchar"] = ":"
            mapConfig["theme"] = "fusion"
            colorDataObj = {
                "minvalue": "20000",
                "startlabel": "Low",
                "endlabel": "High",
                "code": "#FF4411",
                "gradient": "1",
                "color": [{
                        "minValue": "20000",
                        "maxValue": "30000",
                        "code": "red"
                    },
                    {
                        "minValue": "30000",
                        "maxValue": "35000",
                        "code": "#23f527"
                    },
                    {
                        "minValue": "35000",
                        "maxValue": "40000",
                        "code": "#00e3f7"
                    }
                ]
            }
            dataSource["colorrange"] = colorDataObj
            dataSource["chart"] = mapConfig 
            dataSource["data"] = []
            mapDataArray = [
                ["002",k[0], "1"],
                ["003", k[1], "1"],
                ["004", k[2], "1"],
                ["005", k[3], "1"],
                ["006", k[4], "1"],
                ["007", k[5], "1"],
                ["010", k[6], "1"],
                ["011",k[7], "1"],
                ["012", k[8], "1"],
                ["013",k[9], "1"],
                ["014",k[10], "1"],
                ["015",25000, "1"],
                ["016",k[12], "1"],
                ["017",k[13], "1"],
                ["018",k[14], "1"],
                ["020",k[15], "1"],
                ["021",k[16], "1"],
                ["023",k[26], "1"],
                ["026",35000, "1"],
                ["028",k[18], "1"],
                ["029",k[19], "1"],
                ["030",k[20], "1"],
                ["031",k[21], "1"],
                ["033",k[22], "1"],
                ["034",k[23], "1"],
                ["035",k[24], "1"],
                ["036",k[25], "1"],
                ["027",k[27], "1"]
            ]
            for i in range(len(mapDataArray)):
                dataSource["data"].append({
                    "id": mapDataArray[i][0],
                    "value": mapDataArray[i][1],
                    "showLabel": mapDataArray[i][2]
                })
            fusionMap = FusionCharts("maps/india", "mySecondMap", "500", "640", "p1", "json", dataSource)
            z[0]=fusionMap.render()
            dataSource = OrderedDict()
            mapConfig = OrderedDict()
            mapConfig["caption"] = "PROFIT(Positive Authentication)"
            mapConfig["subcaption"] = "MONTHLY PROFIT"
            mapConfig["entitytooltext"]="$lname: <b> $dataValue </b> Monthly Profit"
            mapConfig["labelsepchar"] = "Rs"
            mapConfig["theme"] = "fusion"
            colorDataObj = {
                "minvalue": "50000",
                "startlabel": "Low",
                "endlabel": "High",
                "code": "#FF4411",
                "gradient": "1",
                "color": [{
                        "minValue": "50000",
                        "maxValue": "80000",
                        "code": "#00c0f9"
                    },
                    {
                        "minValue": "80000",
                        "maxValue": "100000",
                        "code": "#23f527"
                    },
                    {
                        "minValue": "100000",
                        "maxValue": "200000",
                        "code": "#00e3f7"
                    }
                ]
            }
            dataSource["colorrange"] = colorDataObj
            dataSource["chart"] = mapConfig
            dataSource["data"] = []
            mapDataArray = [
                ["002", ((z[7][0]*toc[0])+(z[8][0]*toc[1])+(z[9][0]*toc[2])), "1"],
                ["003", ((z[7][1]*toc[0])+(z[8][1]*toc[1])+(z[9][1]*toc[2])), "1"],
                ["004", ((z[7][2]*toc[0])+(z[8][2]*toc[1])+(z[9][2]*toc[2])), "1"],
                ["005", ((z[7][3]*toc[0])+(z[8][3]*toc[1])+(z[9][3]*toc[2])), "1"],
                ["006", ((z[7][4]*toc[0])+(z[8][4]*toc[1])+(z[9][4]*toc[2])), "1"],
                ["007",((z[7][5]*toc[0])+(z[8][5]*toc[1])+(z[9][5]*toc[2])), "1"],
                ["010",((z[7][6]*toc[0])+(z[8][6]*toc[1])+(z[9][6]*toc[2])), "1"],
                ["011",((z[7][7]*toc[0])+(z[8][7]*toc[1])+(z[9][7]*toc[2])), "1"],
                ["012", ((z[7][8]*toc[0])+(z[8][8]*toc[1])+(z[9][8]*toc[2])), "1"],
                ["013",((z[7][9]*toc[0])+(z[8][9]*toc[1])+(z[9][9]*toc[2])), "1"],
                ["014",((z[7][10]*toc[0])+(z[8][10]*toc[1])+(z[9][10]*toc[2])), "1"],
                ["015",79000, "1"],
                ["016",((z[7][12]*toc[0])+(z[8][12]*toc[1])+(z[9][12]*toc[2])), "1"],
                ["017",((z[7][13]*toc[0])+(z[8][13]*toc[1])+(z[9][13]*toc[2])), "1"],
                ["018",((z[7][14]*toc[0])+(z[8][14]*toc[1])+(z[9][14]*toc[2])), "1"],
                ["020",((z[7][15]*toc[0])+(z[8][15]*toc[1])+(z[9][15]*toc[2])), "1"],
                ["021",((z[7][16]*toc[0])+(z[8][16]*toc[1])+(z[9][16]*toc[2])), "1"],
                ["023",((z[7][26]*toc[0])+(z[8][26]*toc[1])+(z[9][26]*toc[2])), "1"],
                ["026",85000, "1"],
                ["028",((z[7][18]*toc[0])+(z[8][18]*toc[1])+(z[9][18]*toc[2])), "1"],
                ["029",((z[7][19]*toc[0])+(z[8][19]*toc[1])+(z[9][19]*toc[2])), "1"],
                ["030",((z[7][20]*toc[0])+(z[8][20]*toc[1])+(z[9][20]*toc[2])), "1"],
                ["031",((z[7][21]*toc[0])+(z[8][21]*toc[1])+(z[9][21]*toc[2])), "1"],
                ["033",((z[7][22]*toc[0])+(z[8][22]*toc[1])+(z[9][22]*toc[2])), "1"],
                ["034",((z[7][23]*toc[0])+(z[8][23]*toc[1])+(z[9][23]*toc[2])), "1"],
                ["035",((z[7][24]*toc[0])+(z[8][24]*toc[1])+(z[9][24]*toc[2])), "1"],
                ["036",((z[7][25]*toc[0])+(z[8][25]*toc[1])+(z[9][25]*toc[2])), "1"],
                ["027",((z[7][27]*toc[0])+(z[8][27]*toc[1])+(z[9][27]*toc[2])), "1"]
            ]
            for i in range(len(mapDataArray)):
                dataSource["data"].append({
                    "id": mapDataArray[i][0],
                    "value": mapDataArray[i][1],
                    "showLabel": mapDataArray[i][2]
                })
            fusionMap = FusionCharts("maps/india", "myThirdMap", "500", "640", "p2", "json", dataSource)
            z[1]=fusionMap.render()
            dataSource = OrderedDict()
            mapConfig = OrderedDict()
            mapConfig["caption"] = "LOSS(Negative Authentication)"
            mapConfig["subcaption"] = "MONTHLY LOSS"
            mapConfig["entitytooltext"]="$lname: <b> $dataValue </b> Monthly Loss"
            mapConfig["labelsepchar"] = "Rs"
            mapConfig["theme"] = "fusion"
            colorDataObj = {
                "minvalue": "20000",
                "startlabel": "Low",
                "endlabel": "High",
                "code": "#FF4411",
                "gradient": "1",
                "color": [{
                        "minValue": "20000",
                        "maxValue": "25000",
                        "code": "#00c0f9"
                    },
                    {
                        "minValue": "25000",
                        "maxValue": "40000",
                        "code": "#23f527"
                    },
                    {
                        "minValue": "40000",
                        "maxValue": "100000",
                        "code": "#00e3f7"
                    }
                ]
            }
            dataSource["colorrange"] = colorDataObj
            dataSource["chart"] = mapConfig
            dataSource["data"] = []
            mapDataArray = [
                ["002", ((z[4][0]*toc[0])+(z[5][0]*toc[1])+(z[6][0]*toc[2])), "1"],
                ["003", ((z[4][1]*toc[0])+(z[5][1]*toc[1])+(z[6][1]*toc[2])), "1"],
                ["004", ((z[4][2]*toc[0])+(z[5][2]*toc[1])+(z[6][2]*toc[2])), "1"],
                ["005", ((z[4][3]*toc[0])+(z[5][3]*toc[1])+(z[6][3]*toc[2])), "1"],
                ["006", ((z[4][4]*toc[0])+(z[5][4]*toc[1])+(z[6][4]*toc[2])), "1"],
                ["007",((z[4][5]*toc[0])+(z[5][5]*toc[1])+(z[6][5]*toc[2])), "1"],
                ["010",((z[4][6]*toc[0])+(z[5][6]*toc[1])+(z[6][6]*toc[2])), "1"],
                ["011",((z[4][7]*toc[0])+(z[5][7]*toc[1])+(z[6][7]*toc[2])), "1"],
                ["012", ((z[4][8]*toc[0])+(z[5][8]*toc[1])+(z[6][8]*toc[2])), "1"],
                ["013",((z[4][9]*toc[0])+(z[5][9]*toc[1])+(z[6][9]*toc[2])), "1"],
                ["014",((z[4][10]*toc[0])+(z[5][10]*toc[1])+(z[6][10]*toc[2])), "1"],
                ["015",23000, "1"],
                ["016",((z[4][12]*toc[0])+(z[5][12]*toc[1])+(z[6][12]*toc[2])), "1"],
                ["017",((z[4][13]*toc[0])+(z[5][13]*toc[1])+(z[6][13]*toc[2])), "1"],
                ["018",((z[4][14]*toc[0])+(z[5][14]*toc[1])+(z[6][14]*toc[2])), "1"],
                ["020",((z[4][15]*toc[0])+(z[5][15]*toc[1])+(z[6][15]*toc[2])), "1"],
                ["021",((z[4][16]*toc[0])+(z[5][16]*toc[1])+(z[6][16]*toc[2])), "1"],
                ["023",((z[4][26]*toc[0])+(z[5][26]*toc[1])+(z[6][26]*toc[2])), "1"],
                ["026",28000, "1"],
                ["028",((z[4][18]*toc[0])+(z[5][18]*toc[1])+(z[6][18]*toc[2])), "1"],
                ["029",((z[4][19]*toc[0])+(z[5][19]*toc[1])+(z[6][19]*toc[2])), "1"],
                ["030",((z[4][20]*toc[0])+(z[5][20]*toc[1])+(z[6][20]*toc[2])), "1"],
                ["031",((z[4][21]*toc[0])+(z[5][21]*toc[1])+(z[6][21]*toc[2])), "1"],
                ["033",((z[4][22]*toc[0])+(z[5][22]*toc[1])+(z[6][22]*toc[2])), "1"],
                ["034",((z[4][23]*toc[0])+(z[5][23]*toc[1])+(z[6][23]*toc[2])), "1"],
                ["035",((z[4][24]*toc[0])+(z[5][24]*toc[1])+(z[6][24]*toc[2])), "1"],
                ["036",((z[4][25]*toc[0])+(z[5][25]*toc[1])+(z[6][25]*toc[2])), "1"],
                ["027",((z[4][27]*toc[0])+(z[5][27]*toc[1])+(z[6][27]*toc[2])), "1"]
            ]
            for i in range(len(mapDataArray)):
                dataSource["data"].append({
                    "id": mapDataArray[i][0],
                    "value": mapDataArray[i][1],
                    "showLabel": mapDataArray[i][2]
                })
            fusionMap = FusionCharts("maps/india", "myForthMap", "500", "640", "l2", "json", dataSource)
            z[3]=fusionMap.render()
            with open(pa,'w') as f:
                                fn=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
                                41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66]
                                w=csv.DictWriter(f,fieldnames=fn)
                                w.writeheader()
                                w.writerow(z)
        return render(request, 'fs/mp.html',{'output':z})

def login1(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            vuser = Us.objects.get(username=username)
            if vuser.is_act == True:
                if vuser.is_ad == True:
                    request.session.set_expiry(3000)
                    login(request,user)
                    data = Us.objects.all().order_by('is_act')
                    u = { "pk": data }
                    return render(request,'fs/adminlogin.html',u)
                else:
                    request.session.set_expiry(3000)
                    login(request,user)
                    vuser = Us.objects.get(username=username)
                    s=int(vuser.pe)
                    toc={}
                    z={}
                    k=vuser.username
                    d=int(k[-4:])
                    if d <= 5009 :
                        un = int(k[-1:])
                    else:
                        un = int(k[-2:])
                    pa="/home/me/final/media/media/"+k+"/l.csv"
                    if os.path.exists(pa):
                        with open(pa,'r') as f:
                            w=csv.DictReader(f)
                            for r in w:
                                z=dict(r)
                        f.close()
                        z={ int(k):str(v) for k,v in z.items() }
                    else:
                        if s == 1 :
                            toc[0]=2
                            toc[1]=5
                            toc[2]=3
                        elif s == 2 :
                            toc[0]=1
                            toc[1]=6
                            toc[2]=3
                        elif s == 3 :
                            toc[0]=1
                            toc[1]=7
                            toc[2]=2 
                        elif s == 4 :
                            toc[0]=1
                            toc[1]=8
                            toc[2]=1
                        else:
                            toc={}
                        z[9]=toc[0]
                        z[10]=toc[1]
                        z[11]=toc[2]
                        d1="sqlite:////home/me/final/media/media/"+k+"/"+str(un)+".db"
                        disk_engine = create_engine(d1)
                        td=datetime.now().strftime('%Y-%m-%d')
                        ye=date.today() - timedelta(days=1)
                        ye=ye.strftime('%Y-%m-%d')
                        cm=datetime.now().month
                        cy=datetime.now().year
                        sd=str(cy)+"-"+"0"+str(cm)+"-"+"01"
                        yy = pd.read_sql_query(' SELECT count(DATE) as `c1` FROM set1 WHERE DATE = (?) ',disk_engine,params=(ye,))
                        tt = pd.read_sql_query(' SELECT count(DATE) as `c2` FROM set1 WHERE DATE = (?) ',disk_engine,params=(td,))
                        mm = pd.read_sql_query(' SELECT count(DATE) as `c3` FROM set1 WHERE DATE BETWEEN (?) and (?)',disk_engine,params=(sd,td,))
                        h1 = pd.read_sql_query(' SELECT count(AUTHRESPONSE) as `c4` FROM set1 WHERE AUTHRESPONSE = 0 AND DATE BETWEEN (?) and (?)',disk_engine,params=(sd,td,))
                        h2 = pd.read_sql_query(' SELECT count(AUTHRESPONSE) as `c5` FROM set1 WHERE AUTHRESPONSE = 1 AND DATE BETWEEN (?) and (?)',disk_engine,params=(sd,td,))
                        z={1:int(tt.c2),2:int(yy.c1),3:int(mm.c3)}
                        aa=math.floor((h2.c5/mm.c3)*100)
                        dv=str(aa)+"%"
                        dataSource = OrderedDict()
                        widgetConfig = OrderedDict()
                        widgetConfig["caption"] = "Positive-Authentication-Meter"
                        widgetConfig["lowerLimit"] = "0"
                        widgetConfig["pivotFillColor"]="#5599CC"
                        widgetConfig["pivotFillAlpha"]="100"
                        widgetConfig["upperLimit"] = "100"
                        widgetConfig["majorTMNumber"]="9",
                        widgetConfig["minorTMNumber"]="4"
                        widgetConfig["showValue"] = "1"
                        widgetConfig["numberSuffix"] = "%"
                        widgetConfig["theme"] = "fusion"
                        colorRangeData = OrderedDict()
                        colorRangeData["color"] = [{
                        "minValue": "0",
                        "maxValue": "50",
                        "code": "#F2726F"
                        },
                        {
                        "minValue": "50",
                        "maxValue": "75",
                        "code": "#FFC533"
                        },
                        {
                        "minValue": "75",
                        "maxValue": "100",
                        "code": "#62B58F"
                        }
                        ]
                        dialData = OrderedDict()
                        dialData["dial"] = []
                        dataSource["chart"] = widgetConfig
                        dataSource["colorRange"] = colorRangeData
                        dataSource["dials"] = dialData
                        dialData["dial"].append({"value":dv})
                        angulargaugeWidget = FusionCharts("angulargauge", "myFirstWidget", "100%", "250", "positive-meter", "json", dataSource)
                        z[4]=angulargaugeWidget.render()
                        aa=math.ceil((h1.c4/mm.c3)*100)
                        dv=str(aa)+"%"
                        dataSource = OrderedDict()
                        widgetConfig = OrderedDict()
                        widgetConfig["caption"] = "Negative-Authentication-Meter"
                        widgetConfig["lowerLimit"] = "0"
                        widgetConfig["pivotFillColor"]="#5599CC"
                        widgetConfig["pivotFillAlpha"]="100"
                        widgetConfig["upperLimit"] = "100"
                        widgetConfig["majorTMNumber"]="9",
                        widgetConfig["minorTMNumber"]="4"
                        widgetConfig["showValue"] = "1"
                        widgetConfig["numberSuffix"] = "%"
                        widgetConfig["theme"] = "fusion"
                        colorRangeData = OrderedDict()
                        colorRangeData["color"] = [{
                        "minValue": "75",
                        "maxValue": "100",
                        "code": "#F2726F"
                        },
                        {
                        "minValue": "30",
                        "maxValue": "75",
                        "code": "#FFC533"
                        },
                        {
                        "minValue": "0",
                        "maxValue": "30",
                        "code": "#62B58F"
                        }
                        ]
                        dialData = OrderedDict()
                        dialData["dial"] = []
                        dataSource["chart"] = widgetConfig
                        dataSource["colorRange"] = colorRangeData
                        dataSource["dials"] = dialData
                        dialData["dial"].append({"value":dv})
                        angulargaugeWidget = FusionCharts("angulargauge", "myFirstWidget1", "100%", "250", "negative-meter", "json", dataSource)
                        z[5]=angulargaugeWidget.render()
                        h3 = pd.read_sql_query(' SELECT AUTH_TYPE,COUNT(AUTH_TYPE) as `c6` FROM set1 WHERE DATE = (?)  GROUP BY AUTH_TYPE  ORDER BY AUTH_TYPE ',disk_engine,params=(td,))
                        da=h3.AUTH_TYPE.to_dict()
                        dt=h3.c6.to_dict()
                        p={2:'DEMOGRAPHIC AUTHENTICATION',3:'BIOMETRIC AUTHENTICATION',4:'OTP BASED AUTHETICATION'}
                        chartData = OrderedDict()
                        for i in da:
                            for j in p:
                                if da[i]==j:
                                    chartData[p[j]]=dt[i]
                        dataSource = OrderedDict()
                        chartConfig = OrderedDict()
                        chartConfig["caption"] = "AUTHENTICATION-TYPE"
                        chartConfig["subCaption"] = "TODAY-RESPONSE"
                        chartConfig["xAxisName"] = "TYPE OF AUTHENTICATION"
                        chartConfig["yAxisName"] = "Number_Of_Transaction"
                        chartConfig["theme"] = "fusion"
                        dataSource["chart"] = chartConfig
                        dataSource["data"] = []
                        for key, value in chartData.items():
                            data = {}
                            data["label"] = key
                            data["value"] = value
                            dataSource["data"].append(data)
                        pie2D = FusionCharts("pie2d", "myFirstChart1", "100%", "450", "auth-piechart", "json", dataSource)
                        z[6]=pie2D.render()
                        k1 = pd.read_sql_query(' SELECT DATE,count(*) as cd1 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTH_TYPE = 2 AND AUTHRESPONSE = 1 GROUP BY DATE ORDER BY DATE',disk_engine,params=(sd,td))
                        k2 = pd.read_sql_query(' SELECT count(*) as cd2 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTH_TYPE = 3 AND AUTHRESPONSE = 1 GROUP BY DATE ORDER BY DATE',disk_engine,params=(sd,td))
                        k3 = pd.read_sql_query(' SELECT count(*) as cd3 FROM set1 WHERE DATE BETWEEN (?) AND (?) AND AUTH_TYPE = 4 AND AUTHRESPONSE = 1 GROUP BY DATE ORDER BY DATE',disk_engine,params=(sd,td))
                        trace1 = go.Bar(
                                x=k1.DATE,
                                y=k1.cd1,
                                name='DEMOGRAPHIC AUTHENTICATION'
                            )
                        trace2 = go.Bar(
                            x=k1.DATE,
                            y=k2.cd2,
                            name='OTP AUTHENTICATION'
                        )
                        trace3= go.Bar(
                            x=k1.DATE,
                            y=k3.cd3,
                            name='BIOMETRIC AUTHENTICATION'
                        )
                        trace4= go.Scatter(
                            x=k1.DATE,
                            y=(k1.cd1*toc[0]),
                            name='DEMOGRAPHIC PROFIT AUTHENTICATION',
                            yaxis='y2'
                        )
                        trace5= go.Scatter(
                            x=k1.DATE,
                            y=(k2.cd2*toc[1]),
                            name='OTP PROFIT AUTHENTICATION',
                            yaxis='y2'
                        )
                        trace6= go.Scatter(
                            x=k1.DATE,
                            y=(k3.cd3*toc[2]),
                            name='BIOMETRIC PROFIT AUTHENTICATION',
                            yaxis='y2'
                        )
                        data = [trace1,trace2,trace3,trace4,trace5,trace6]
                        layout = go.Layout(
                            legend=dict(x=-0.1,y=-0.5,orientation="h"),
                            barmode='group',
                            title='Transaction',
                            yaxis=dict(
                                title='Number OF Transaction'
                            ),
                            yaxis2=dict(
                                title='Profit In Rs',
                                titlefont=dict(
                                    color='rgb(148, 103, 189)'
                                ),
                                tickfont=dict(
                                    color='rgb(148, 103, 189)'
                                ),
                                overlaying='y',
                                side='right'
                            )
                        )
                        fig = go.Figure(data=data, layout=layout)
                        z[7]=plotly.offline.plot(fig,auto_open=False,include_plotlyjs=False,output_type='div')
                        df = pd.read_sql_query('SELECT COUNT(*) as `n1` FROM set1 WHERE AUTHRESPONSE = 0 AND DATE BETWEEN (?) AND (?) GROUP BY AGE ORDER BY AGE',disk_engine,params=(sd,td))
                        dk = pd.read_sql_query('SELECT COUNT(*) as `n2` FROM set1 WHERE AUTHRESPONSE = 1 AND DATE BETWEEN (?) AND (?) GROUP BY AGE ORDER BY AGE',disk_engine,params=(sd,td))
                        trace11 = go.Bar(
                                            x=['CHILDREN','TEENAGER','SENIOR-CITIZEN'],
                                            y=df.n1,
                                            width=[0.3,0.3,0.3],
                                            name='NEGATIVE_AUTH_RESPONSE',
                                            textposition = 'auto',
                                            marker=dict(
                                                color='red',
                                                line=dict(
                                                color='red',
                                                width=0.5),
                                            ),
                                            opacity=0.6
                        )
                        trace12 = go.Bar(    
                                            x=['CHILDREN','TEENAGER','SENIOR-CITIZEN'],
                                            y=dk.n2,
                                            width=[0.3,0.3,0.3],
                                            textposition = 'auto',
                                            marker=dict(
                                                color='green',
                                                line=dict(
                                                color='green',
                                                width=0.5),
                                            ),
                                            opacity=0.6,
                                            name='POSITIVE_AUTH_RESPONSE'
                        )
                        data1 = [trace11, trace12]
                        layout1 = go.Layout(
                                            xaxis={'title': 'AGE-GROUP'},
                                            yaxis={'title': 'NO.OF TRANSACTION'},
                                            barmode='group',
                                            legend=dict(x=-0.1,y=-0.5,orientation="h"),
                                            title='AGE-WISE-AUTHENTICATION(MONTHLY)'
                        )
                        fig1= go.Figure(data=data1, layout=layout1)
                        z[8]=plotly.offline.plot(fig1,auto_open=False,include_plotlyjs=False,output_type='div')
                        with open(pa,'w') as f:
                            fn=[1,2,3,4,5,6,7,8]
                            w=csv.DictWriter(f,fieldnames=fn)
                            w.writeheader()
                            w.writerow(z)
                    return render(request, 'fs/userlogin.html',{'output':z})
            else:
                return render(request, 'fs/index.html', {'error_message': 'Your account has been disabled or not activated'})
        else:
            return render(request, 'fs/index.html', {'error_message': 'Invalid login ! Please Register !'})
    else:
         return render(request, 'fs/index.html')


def up(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        s=int(vuser.pe)
        toc={}
        z={}
        if s == 1 :
            toc[0]=2
            toc[1]=5
            toc[2]=3
        elif s == 2 :
            toc[0]=1
            toc[1]=6
            toc[2]=3
        elif s == 3 :
            toc[0]=1
            toc[1]=7
            toc[2]=2 
        elif s == 4 :
            toc[0]=1
            toc[1]=8
            toc[2]=1
        else:
            toc={}
        z[0]=toc[0]
        z[1]=toc[1]
        z[2]=toc[2]
        if request.method == "POST":
            f = request.POST['fn']
            l = request.POST['ln']
            vuser.fn=f
            vuser.ln=l
            vuser.save()
        if vuser.is_act == True:
            z[3]=vuser
            return render(request, 'fs/up.html',{'output':z})
        else:
            return render(request, 'fs/index.html', {'error_message': 'Your account has been disabled or not activated'})


def rp(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        if request.method == "POST":
            p = request.POST['pwd']
            rp = request.POST['rpwd']
            if p == rp:
                vuser = get_object_or_404(Us,username=rt)
                if vuser.is_act == True :
                    vuser.password=p
                    vuser.save()
                    main = User.objects.get(username=rt)
                    main.set_password(p)
                    main.save()
                    logout(request)
                    return render(request, 'fs/index.html',{'error_message': 'Your Password has been Changed ! Please Relogin !!!'})
                else:
                    return render(request, 'fs/index.html', {'error_message': 'Your account has been disabled or not activated'})
            else:
                return render(request,'fs/rp.html',{'error_message': 'PASSWORD AND REPEAT PASSWORD NOT SAME'})     
        return render(request,'fs/rp.html')


def ec(request,rt):
    if not request.user.is_authenticated:
        return render(request, 'fs/index.html')
    else:
        vuser = get_object_or_404(Us,username=rt)
        k=vuser.username
        z={}
        d=int(k[-4:])
        if d <= 5009 :
            un = int(k[-1:])
        else:
            un = int(k[-2:])
        db=sug.objects.all()
        l={}
        e=0
        pa="/home/me/final/media/media/"+k+"/e.csv"
        for i in db:
            l[e]=i
            e=e+1
        if os.path.exists(pa):
            with open(pa,'r') as f:
                w=csv.DictReader(f)
                for r in w:
                    m=dict(r)
            f.close()
            for k,v in m.items():
                if int(k) == 17:
                    z[int(k)]=str(v)
                elif int(k) == 6 :
                    v=v[0:10]+" 0 ,"+v[33:]
                    z[int(k)]=ast.literal_eval(v)
                elif int(k) >= 9 :
                    v=v[0:9]+" 0 ,"+v[33:]
                    z[int(k)]=ast.literal_eval(v)
                else:
                    v=v[0:9]+" 0 ,"+v[32:]
                    z[int(k)]=ast.literal_eval(v)
            for i in range(0,17):
                z[i][1]=l[i]
            print(z)
        else:
            d1="sqlite:////home/me/final/media/media/"+k+"/"+str(un)+".db"
            disk_engine = create_engine(d1)
            td=datetime.now().strftime('%Y-%m-%d')
            cm=datetime.now().month
            cy=datetime.now().year
            cs=monthrange(cy,cm)
            cs=cs[1]
            sd="1"+"/"+str(cm)+"/"+str(cy)
            ld=str(cs)+"/"+str(cm)+"/"+str(cy)
            z={}
            h11 = pd.read_sql_query(' SELECT AUTH_TYPE,count(*) as `c11` FROM set1 WHERE DATE = (?) GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(td,))
            h1 = pd.read_sql_query(' SELECT AUTH_TYPE,count(*) as `c1` FROM set1 WHERE AUTHRESPONSE = 0 AND DATE = (?) GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(td,))
            h2 = pd.read_sql_query(' SELECT AUTH_TYPE,count(*) as `c2` FROM set1 WHERE AUTHRESPONSE = 1 AND DATE = (?) GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(td,))
            h3 = pd.read_sql_query(' SELECT AUTH_TYPE,count(*) as `c3` FROM set1 WHERE AUTHRESPONSE = 0 AND DATE BETWEEN (?) and (?) GROUP BY AUTH_TYPE ORDER BY AUTH_TYPE',disk_engine,params=(sd,ld))
            q11=h11.c11.to_dict()
            q1=h1.c1.to_dict()
            q2=h3.c3.to_dict()
            h4 = pd.read_sql_query(' SELECT ERRORCODE,count(*) as `c4` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 2 AND DATE = (?) GROUP BY ERRORCODE ORDER BY ERRORCODE',disk_engine,params=(td,))
            h5 = pd.read_sql_query(' SELECT ERRORCODE,count(*) as `c5` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 2 AND DATE BETWEEN (?) and (?) GROUP BY ERRORCODE ORDER BY ERRORCODE',disk_engine,params=(sd,ld))
            t1=h4.ERRORCODE.to_dict()
            ntc1=h4.c4.to_dict()
            ntc4=h5.c5.to_dict()
            p1={101:'NUMBER OF FACEIMAGE DATA EXCEEDED BY 1',102:'MISSING PERSONAL INFORMATION',103:'MISSING PERSONAL ADDRESS',104:'INVALID DATE OF BIRTH',105:'TECHNICAL ERROR',106:'INVALID AADHAAR NUMBER'}
            chartData3 = OrderedDict()
            for i in t1:
                for j in p1:
                    if t1[i]==j:
                        chartData3[p1[j]]=ntc1[i]
            h6 = pd.read_sql_query(' SELECT ERRORCODE,count(*) as `c6` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 3 AND DATE = (?) GROUP BY ERRORCODE ORDER BY ERRORCODE',disk_engine,params=(td,))
            h7 = pd.read_sql_query(' SELECT ERRORCODE,count(*) as `c7` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 3 AND DATE BETWEEN (?) and (?) GROUP BY ERRORCODE ORDER BY ERRORCODE',disk_engine,params=(sd,ld))
            t2=h6.ERRORCODE.to_dict()
            ntc2=h6.c6.to_dict()
            ntc5=h7.c7.to_dict()
            p2={107:'OTP VALIDATION FAILED'}
            chartData4 = OrderedDict()
            for i in t2:
                for j in p2:
                    if t2[i]==j:
                        chartData4[p2[j]]=ntc2[i]
            h8 = pd.read_sql_query(' SELECT ERRORCODE,count(*) as `c8` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 4 AND DATE = (?) GROUP BY ERRORCODE ORDER BY ERRORCODE',disk_engine,params=(td,))
            h9 = pd.read_sql_query(' SELECT ERRORCODE,count(*) as `c9` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 4 AND DATE BETWEEN (?) and (?) GROUP BY ERRORCODE ORDER BY ERRORCODE',disk_engine,params=(sd,ld))
            h20 = pd.read_sql_query(' SELECT AGE,count(*) as `c20` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 4 AND DATE = (?) GROUP BY AGE',disk_engine,params=(td,))
            h21 = pd.read_sql_query(' SELECT AGE,count(*) as `c21` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 4 AND DATE BETWEEN (?) and (?) GROUP BY AGE',disk_engine,params=(sd,ld))
            h22 = pd.read_sql_query(' SELECT AGE,count(*) as `c22` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 3 AND DATE = (?) GROUP BY AGE',disk_engine,params=(td,))
            h23 = pd.read_sql_query(' SELECT AGE,count(*) as `c23` FROM set1 WHERE AUTHRESPONSE = 0 AND AUTH_TYPE = 2 AND DATE = (?) GROUP BY AGE',disk_engine,params=(td,))
            r1=h20.c20.to_dict()
            r2=h21.c21.to_dict()
            r3=h22.c22.to_dict()
            r4=h23.c23.to_dict()
            p3={108:'BIOMETRIC DIDNOT MATCH',109:'BIOMETRIC LOCKED BY AADHAAR HOLDER',110:'INVALID BIOMETRICS DATA',111:'INVALID BIOMETRICS DATA IN CIDR SERVER',
            112:'DUPLICATE FINGER USED',113:'AADHAAR SUSPENDED BY AUTHORITY',114:'NUMBER of FINGER DATA SHOULD NOT EXCEEDED BY 10',115:'BEST FINGER DETECTION REQUIRED',
            116:'DEVICE KEY ROTATION POLICY',117:'AADHAAR CANCELLED'}
            t3=h8.ERRORCODE.to_dict()
            ntc3=h8.c8.to_dict()
            ntc6=h9.c9.to_dict()
            chartData5 = OrderedDict()
            for i in t3:
                for j in p3:
                    if t3[i]==j:
                        chartData5[p3[j]]=ntc3[i]
            k=0
            db=sug.objects.all()
            k=0
            for i in db:
                z[k]=i
                k=k+1
            k=0
            d=101
            t={}
            for i in range(0,17):
                e = pd.read_sql_query(' SELECT AGE,count(*) as `e1` FROM set1 WHERE AUTHRESPONSE = 0 AND ERRORCODE = (?) AND DATE = (?) GROUP BY AGE',disk_engine,params=(d,td,))
                t = e.e1.to_dict()
                if i<=5:
                    if i==0:
                        z[i]=[("%.2f" % round((ntc1[i]/q1[0])*100,2)),(z[i]),("%.2f" % round((ntc4[i]/q2[0])*100,2)),t[0],t[1],t[2],q1[0],r1[0],("%.2f" % round((r2[0]/q2[2])*100,2)),r4[0],r4[1],r4[2]]
                    else:
                        z[i]=[("%.2f" % round((ntc1[i]/q1[0])*100,2)),(z[i]),("%.2f" % round((ntc4[i]/q2[0])*100,2)),t[0],t[1],t[2]]
                if i==6:
                    z[i]=[("%.2f" % round((ntc2[0]/q1[1])*100,2)),(z[i]),("%.2f" % round((ntc5[0]/q2[1])*100,2)),t[0],t[1],t[2],q1[1],r1[1],("%.2f" % round((r2[1]/q2[2])*100,2)),r3[0],r3[1],r3[2]]
                if i>=7:
                    if i==7:
                        z[i]=[("%.2f" % round((ntc3[k]/q1[2])*100,2)),(z[i]),("%.2f" % round((ntc6[i]/q2[2])*100,2)),t[0],t[1],t[2],q1[2],r1[2],("%.2f" % round((r2[2]/q2[2])*100,2)),r1[0],r1[1],r1[2]]
                    else:
                        z[i]=[("%.2f" % round((ntc3[k]/q1[2])*100,2)),(z[i]),("%.2f" % round((ntc6[k]/q2[2])*100,2)),t[0],t[1],t[2]]
                    k=k+1
                d=d+1
            t=h11.AUTH_TYPE.to_dict()
            ntc=h1.c1.to_dict()
            ptc=h2.c2.to_dict()
            p={2:'DEMOGRAPHIC AUTHENTICATION',3:'OTP BASED AUTHENTICATION',4:'BIOMETRIC AUTHETICATION'}
            chartData1 = OrderedDict()
            for i in t:
                for j in p:
                    if t[i]==j:
                        chartData1[p[j]]=ntc[i]
            chartData2 = OrderedDict()
            for i in t:
                for j in p:
                    if t[i]==j:
                        chartData2[p[j]]=ptc[i]
            chartConfig = OrderedDict()
            dataSource = {}
            chartConfig["caption"] = "AUTHENTICATION-TYPE"
            chartConfig["subCaption"] = "Today-AUthentication"
            chartConfig["xAxisName"] = "AUTHENTICATION_TYPE"
            chartConfig["yAxisName"] = "Number_Of_Transaction"
            chartConfig["theme"] = "fusion"
            chartConfig["numberPrefix"]= "%"
            chartConfig["plotFillAlpha"]= "80"
            chartConfig["plotToolText"]="<b>$dataValue</b> apps on $seriesName in $label"
            dataSource["chart"] = chartConfig
            dataSource['data'] = []
            dataSource['linkeddata'] = []
            v=1
            for key,value in chartData1.items():
                data = {}
                data['label'] = key
                data['value'] = value
                data['link'] = 'newchart-json-'+ str(v) 
                dataSource['data'].append(data)
                linkData = {}
                linkData['id'] = str(v)
                linkedchart = {}    
                linkedchart['data'] = []
                if v==1:
                    linkedchart['chart'] = {
                    "caption": "AUTHENTICATION - DEMOGRAPHIC AUTHENTICATION",
                    "subcaption": "TODAY",
                    "theme": "fusion",
                    "plottooltext": "$label, $dataValue,  $percentValue"
                    }
                    for key,value in chartData3.items():
                        arrDara = {}
                        arrDara['label'] = key
                        arrDara['value'] = value
                        linkedchart['data'].append(arrDara)
                if v==2:
                    linkedchart['chart'] = {
                    "caption": "AUTHENTICATION - OTP AUTHENTICATION",
                    "subcaption": "TODAY",
                    "theme": "fusion",
                    "plottooltext": "$label, $dataValue,  $percentValue"
                    }
                    for key,value in chartData4.items():
                        arrDara = {}
                        arrDara['label'] = key
                        arrDara['value'] = value
                        linkedchart['data'].append(arrDara)
                if v==3:
                    linkedchart['chart'] = {
                    "caption": "AUTHENTICATION -BIOMETRIC AUTHENTICATION",
                    "subcaption": "TODAY",
                    "numberSuffix": "k",
                    "theme": "fusion",
                    "plottooltext": "$label, $dataValue,  $percentValue"
                    }
                    for key,value in chartData5.items():
                        arrDara = {}
                        arrDara['label'] = key
                        arrDara['value'] = value
                        linkedchart['data'].append(arrDara)

                linkData['linkedchart'] = linkedchart
                dataSource['linkeddata'].append(linkData)
                v=v+1
            pie2D = FusionCharts("pie2d", "ex1" , "1000", "500", "error-co", "json", dataSource)	
            z[17]=pie2D.render()
            with open(pa,'w') as f:
                            fn=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
                            w=csv.DictWriter(f,fieldnames=fn)
                            w.writeheader()
                            w.writerow(z)
        return render(request, 'fs/error-re.html',{'output':z})

def forget(request):
    if request.method == "POST":
        username = request.POST['username']
        if Us.objects.filter(username=username).exists():
            vuser = Us.objects.get(username=username)
            if vuser is not None :
                if vuser.is_act == True:
                    if vuser.otp == 0 :
                        o = random.randint(1000,9999)
                        vuser.otp = o
                        content1 = "YOUR OTP REQUEST RECEIVED:\n OTP: "
                        send_mail('URGENT:OTP',content1 + str(o), 'admin@analyticsking.com', [vuser.em])
                        vuser.save()
                        return render(request,'fs/otp.html')
                    else:
                        return render(request, 'fs/otp.html', {'error_message': 'Your Previous OTP is Still Valid'})
                else:
                    return render(request, 'fs/index.html', {'error_message': 'Your account has been disabled or not activated'})
            else:
                return render(request, 'fs/index.html', {'error_message': 'Invalid UserID ! PLEASE REGISTER'})
        else:
            return render(request,'fs/index.html',{'error_message': 'Invalid UserID  ! PLEASE REGISTER' })
    else:
            return render(request,'fs/forget.html')


   
   
def otp(request):
    global c
    if request.method == "POST":
        otq = request.POST['otp']
        if Us.objects.filter(otp=otq).exists():
            vus = Us.objects.get(otp=otq)
            if vus.otp != 0:
                if vus.is_act == True:
                    if vus.otp == int(otq):
                        vus.otp=0
                        vus.save()
                        content1 = "YOUR FORGET PASSWORD REQUEST RECEIVED:\n USERID: "
                        content2="\nPASSWORD:  "
                        send_mail('FORGET PASSWORD',content1 + vus.username + content2 + vus.password, 'admin@analyticsking.com', [vus.em])
                        return render(request,'fs/index.html', {'error_message': 'An EMAIL With UserId And Password Is Sent To You'})
                    else :
                        vus.otp=0
                        vus.save()
                        c=int(c)+int(1)
                        if  c >= int(3) :
                            vus.otp=0
                            vus.is_act = False
                            vus.save()
                            return render(request,'fs/index.html', {'error_message': 'Too Many Attempts ! Please Try Again Later'})
                        return render(request,'fs/otp.html', {'error_message': 'OTP Didnot Match Try Again '})
                else:
                    c=int(c)+int(1)
                    return render(request, 'fs/index.html', {'error_message': 'Your account has been disabled or not activated'})
            else:
                c=int(c)+int(1)
                return render(request, 'fs/forget.html', {'error_message': 'OTP Didnot Generated'})
        else:
            c=int(c)+int(1)
            if  c >= int(3) :
                return render(request,'fs/index.html', {'error_message': 'Too Many Attempts ! Please Try Again Later'})
            return render(request,'fs/otp.html', {'error_message': 'OTP Didnot Match Try Again'})
