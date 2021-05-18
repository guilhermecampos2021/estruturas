import PySimpleGUI as sg
from decimal import Decimal
sg.theme('SandyBeach')

layout = [
    [sg.Text('Dados de Entrada')],
    [sg.Text('bw(cm)', size=(17,1)), sg.InputText(size=(10,1))],
    [sg.Text('h(cm)', size=(17,1)), sg.InputText(size=(10,1))],
    [sg.Text('fck(Mpa)', size=(17,1)), sg.InputText(size=(10,1))],
    [sg.Text('Momento (kgfm)', size=(17,1)), sg.InputText(size=(10,1))],
    [sg.Submit(),sg.Cancel()]
]


window = sg.Window('Tela de Entrada',layout)
event,values = window.read()
window.close()
print(event,values[0],values[1],values[2],values[3])


bw = int(values[0])
h = int(values[1])
dl = 5
d = h-dl
fck = float(values[2])
fc = 0.85*fck/1.4
md = float(values[3]) # Em kgfm


def aco(bw, d, fck, md):
    fyd = 43.45  #KN/cm2
    fc = 0.85*(fck/10)/1.4 #KN/cm2
    k = md/(fc*bw*d**2)

    if fck <= 35:
        kl = 0.32
    else:
        kl = 0.269

    if k< 0.32:
        klinha = k
    else:
        klinha = kl

    As1 = fc*bw*d/(fyd)*(1-(1-2*klinha)**0.5)
    As2 = fc*bw*d/(fyd)*(k-klinha)/(1-5/d)

    Asprincipal = As1+As2
    AsCompressao = As2
    wmin = 0.035 # Apenas para seção retangular
    romin = ((fck/14)/fyd)*wmin
    Asmin = romin * bw * (d+5)

    return (Asprincipal,AsCompressao,Asmin)


# Processamento
asviga,ascom, asmin = aco(bw,d,fck,md)

if asviga>asmin:
    asadot = asviga
else:
    asadot = asmin

diam = [5,6.3,8,10,12.5,16,20,25]
area = list(range(8))
numbarraprincipal =list(range(8))
numbarracompressao =list(range(8))

for i in  range(0,8):
    area[i] = 3.14*(diam[i]/10)**2/4
    numbarraprincipal[i] = int(asadot/area[i]) +1
    numbarracompressao[i]= int(ascom/area[i]) +1

#SAIDA
print(f'####################################################\n')
print(f'Seção {bw}x{h} - fck {fck} - Md(kgfm) = {md}\n')
print(f'####################################################\n')
print(f'As inferior = {asadot:_.2f}cm2\n')
print(f'####################################################\n')

for i in  range(0,8):
    if numbarraprincipal[i]>1:
        print(f'{numbarraprincipal[i]} diam {diam[i]}')

print(f'\n As Minimo = {asmin:_.2f}cm2\n')
print(f'####################################################\n')

print(f'As superior = {ascom:_.2f}cm2')

print(f'\n ####################################################\n')

for i in  range(0,8):
    if numbarracompressao[i]>1:
        print(f'{numbarracompressao[i]} diam {diam[i]}')

print(f'####################################################')
print(f'Elaborado por Guilherme Campos em 25/03/2021')
print(f'####################################################')