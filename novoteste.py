from datetime import datetime
import re, os

data_atual_BR= datetime.now() #.strftime("%d-%m-%Y")
datanome=str(data_atual_BR).replace(':','_').replace(' ','_')
datanome=re.sub(r'\.[0-9]*$', '', datanome)
print(datanome)

if os.path.exists(f'relatorios'):
    print("O arquivo existe")
else:
    os.mkdir(f'relatorios')
    print("O arquivo nao existe")