import csv
import os.path
from os import listdir
from os.path import isfile, join
import pandas as pd
from tqdm import tqdm
my_path = os.path.abspath(os.path.dirname("potencias nega.ipynb"))
onlyfiles = [f for f in listdir('ejmpls5') if isfile(join('ejmpls5', f))]
#print(onlyfiles)
combined_csv_extend=pd.DataFrame()
combined_csv_reduc=pd.DataFrame()
for file in tqdm(onlyfiles):
    path = os.path.join(my_path,r"ejmpls5",file)
    #print(len(pd.read_csv(path).index))
    #print(file)
    pd0=pd.read_csv(path)
    if len(pd0.columns)==13:
        combined_csv_extend = pd.concat([pd0,combined_csv_extend])
    elif len(pd0.columns)==9:
        combined_csv_reduc = pd.concat([pd0,combined_csv_reduc])
    else:
        print(f"EXTENSION NO RECONOCIDA DEL ARCHIVO  {len(pd0.columns)}")

combined_csv_extend.to_csv("combined_extend.csv",index=False,sep=",")
combined_csv_reduc.to_csv("combined_reduc.csv",index=False,sep=",")

list=[] #segunda version
df=pd.read_excel(r"C:\Users\daniel.chacon\Desktop\ReporteEfetividadLecturas.xlsx")
df=df[["medidor","tipo_suministro","suministro"]]
#print(df)
re_list=df.values.tolist()
#print(re_list)
for par in re_list:
    if par[0].isnumeric():
        pass
    else:
        re_list.remove(par)
def tipo_medidor(medidor):
    respuesta=["sin valor","sin valor","sin valor"]
    for par in re_list:
        if int(par[0])==int(medidor) or abs(int(par[0])-int(medidor))==2873013:
            respuesta=par
            #print(par)
            break
    return respuesta
def sacar_extend():
    with open("combined_extend.csv",mode="r") as f:
        lines = f.readlines()
        header=lines[0]
        ncolumns=header.split(",")
        content =tuple(lines[1:])
    aux=""
    for line in tqdm(content):
        camps=line.split(",")
        problem=False
        errorvoltaje=False
        voltajeA=float(camps[4])
        voltajeC=float(camps[5])
        corrienteA=float(camps[6])
        corrienteC=float(camps[7])
        potA=float(camps[11])
        potC=float(camps[12])
        if aux!=camps[0]:
            aux=camps[0]
            valores=tipo_medidor(camps[0])
            tipo_med=valores[1]
            suministro=valores[2]
        voltajes=[voltajeA,voltajeC]
        (h, m) = camps[2].replace('"','').split(':')
        result = int(h)*60 + int(m)
        if result<360 or result==1440:
            horario="00-06H"
        elif result>=360 and result<720:
            horario="06-12H"
        elif result>=720 and result<1080:
            horario="12-18H"
        elif result>=1080 and result<1440:
            horario="18-24H"
        else:
            horario="ERROR DE HORARIO"
        
        if potA*potC<0 and (abs(potA)+abs(potC))>0:
            if max(abs(potA),abs(potC))>min(abs(potA),abs(potC))*1.3:
                caso=" DIF POT >30%"
                list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        if potA<0 and potC<0:
            caso=" POT NEG"
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        if corrienteA*corrienteC==0 and (abs(corrienteA)+abs(corrienteC))>0:
            caso=" CORR CERO"
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        if min(corrienteA,corrienteC)*5<max(corrienteA,corrienteC) and min(corrienteA,corrienteC)>0.6:
            caso=' CORR DESBAL >6i'
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        for volt in voltajes:
            if (volt>110*0.8 and tipo_med=="Maximetro Regulado MT") or (volt>220*0.8 and tipo_med!="Maximetro Regulado MT") :
                pass
            else:
                caso=" VOLT ERROR 110/220 -20%"
                errorvoltaje=True
        if errorvoltaje==True:
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        if voltajeA*voltajeC==0 and (abs(voltajeA)+abs(voltajeC))>0:
            caso=" VOLTAJE CEROS "
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
    df=pd.DataFrame(list)
    return df
def sacar_reduc():
    with open("combined_reduc.csv",mode="r") as f:
        lines = f.readlines()
        header=lines[0]
        ncolumns=header.split(",")
        content =tuple(lines[1:])
    aux=""
    for line in tqdm(content):
        camps=line.split(",")
        problem=False
        errorvoltaje=False
        voltajeA=float(camps[4])
        voltajeB=float(camps[5])
        voltajeC=float(camps[6])
        corrienteA=float(camps[7])
        corrienteC=float(camps[8])
        if aux!=camps[0]:
            aux=camps[0]
            valores=tipo_medidor(camps[0])
            tipo_med=valores[1]
            suministro=valores[2]
        voltajes=[voltajeA,voltajeB,voltajeC]
        (h, m) = camps[2].replace('"','').split(':')
        result = int(h)*60 + int(m)
        if result<360 or result==1440:
            horario="00-06H"
        elif result>=360 and result<720:
            horario="06-12H"
        elif result>=720 and result<1080:
            horario="12-18H"
        elif result>=1080 and result<1440:
            horario="18-24H"
        else:
            horario="ERROR DE HORARIO"

        if corrienteA*corrienteC==0 and (abs(corrienteA)+abs(corrienteC))>0:
            caso=" CORR CERO"
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        if min(corrienteA,corrienteC)*5<max(corrienteA,corrienteC) and min(corrienteA,corrienteC)>0.6:
            caso=' CORR DESBAL >6i'
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        for volt in voltajes:
            if (volt>110*0.8 and tipo_med=="Maximetro Regulado MT") or (volt>220*0.8 and tipo_med!="Maximetro Regulado MT") :
                pass
            else:
                caso=" VOLT ERROR 110/220 -20%"
                errorvoltaje=True
        if errorvoltaje==True:
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])
        if voltajeA*voltajeC==0 and (abs(voltajeA)+abs(voltajeC))>0:
            caso=" VOLTAJE CEROS "
            list.append([horario,camps[0],camps[1],camps[2],caso,camps[6],tipo_med,suministro])

    df=pd.DataFrame(list)
    return df

df_extend=sacar_extend()
df_reduc=sacar_reduc()

df=pd.concat([df_extend,df_reduc],ignore_index=True)
df.columns=["Horario","Medidor","Fecha","Hora","Caso","CORR","TIPO_MED","suministro"]
df2=df.pivot_table(values="CORR", index=["suministro","TIPO_MED","Medidor"], columns = ["Caso","Horario"],aggfunc='count')
df2.style.format({'NUM':'${0:,.0f}'})
writer=pd.ExcelWriter('AnalisisLp2.xlsx')
df2.to_excel(writer,'primerpivot')
writer.save()
print("finalizado")
