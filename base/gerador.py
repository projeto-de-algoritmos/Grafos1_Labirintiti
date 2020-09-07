from random import *
import sys
print("Digite o tamanho do labirinto: ",end='')
size = int(input())

print("Digite o ponto de entrada e saida do labirinto separados por 1 espaço: ",end='')
ini,fim = input().split(" ")

ini = int(ini)

fim = int(fim)

if( ini< 0 or fim < 0 or ini>=size or fim>=size):
    print("Dados de entrada incoerentes")
    sys.exit()
maze = []

x = 0

y = 1

for i in range(size):
    maze.append(('0 '*size).strip(" ").split(" "))

maze[ini][0] = '1'

ponto = [ini,0]

while ponto!=[fim,size-1]:
    moeda = randrange(0,2)
    if(ponto[x]>fim and moeda==1):# tem que subir ent.
        ponto[x]-=1
    elif(ponto[x]<fim and moeda==1):#tem que descer.
        ponto[x]+=1
    else:#Tem que ir para frente.
        ponto[y] += 1
    
    if(ponto[x]<0):#Restringindo a possibilidade de ele tentar sair da matriz.
        ponto[x]+=1
    elif(ponto[y]<0):
        ponto[y]+=1
    elif(ponto[x]>=size):
        ponto[x]-=1
    elif(ponto[y]>=size):
        ponto[y]-=1
    
    maze[ponto[x]][ponto[y]] = '1'

text = ''
for i in range(size): #printa o caminho correto.
    text +=' '.join(maze[i]) + '\n'
#resp = open('ans.txt','w')
#resp.write(text)
#resp.close()
#gerando subcaminhos.
def olharLados(x,y):
    dx = [0, 0, 1, -1]
    dy = [1,-1, 0,  0]
    vizinhos = 0
    for k in range(4):
        sumX = x+dx[k]
        sumY = y+dy[k]
        if( sumX< 0 or sumY < 0 or sumX>=size or sumY >=size):
            continue
        if maze[sumX][sumY]=='1':
            vizinhos+=1
    return vizinhos

i = j = 0
while i < size:
    j = 0
    while j < size:
        if maze[i][j] == '1':
            j+=1    
            continue
        elif olharLados(i,j)==1:
            maze[i][j] = '1'
            i = i - 2
            j = 0
            break
        j+=1
    i+=1
    if i<0:
        i+=1

text = '{}\n{} {}\n'.format(size,ini,fim)
for i in range(size): #printa o labirinto.
    text +=' '.join(maze[i]) + '\n'
resp = open('tmp/maze.txt','w')
resp.write(text)
resp.close()
