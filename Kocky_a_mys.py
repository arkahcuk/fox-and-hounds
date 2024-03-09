# -*- coding: utf8 -*-
""" 
Desková hra kočka a myš
Autor: Filip Hasoň
zápočtový program
zimní semestr 2022/23
Předmět: NPRG030 Programování 1
    
"""

def muzou_tahnout(K:list,M:list): # kočky
    """Vrátí bool hodnoty podle toho, zda jsou jednotlivé tahy jednotlivých koček možné"""
    R=4*[True]  #kočka daného indexu doprava (Right)
    L=4*[True]  #kočka daného indexu doleva (Left)
    for i in range(4):
        if (K[i][1]==0) or (K[i][0]==7) or ([K[i][0]+1,K[i][1]-1]==M) or ([K[i][0]+1,K[i][1]-1] in K):
            L[i]=False
        if (K[i][1]==7) or (K[i][0]==7) or ([K[i][0]+1,K[i][1]+1]==M) or ([K[i][0]+1,K[i][1]+1] in K):
            R[i]=False        
    return R,L
def muze_tahnout(K:list,M:list): # myš
    """Vrátí bool hodnoty podle toho, jestli je tahy myši možné provést"""
    LB,LF,RB,RF=True,True,True,True #left back, left forward, right back, right forward
    if M[1]==0 or [M[0]-1,M[1]-1] in K:
        LF = False
    if M[1]==0 or M[0]==7 or [M[0]+1,M[1]-1] in K:
        LB = False
    if M[1]==7 or [M[0]-1,M[1]+1] in K:
        RF = False
    if M[1]==7 or M[0]==7 or [M[0]+1,M[1]+1] in K:
        RB = False
    return LB,LF,RB,RF
#tahy koček
def vlevo(kocka: int):
    """Tah danou kočkou na pole vlevo dolů"""
    global K
    if ([K[kocka][0]+1,K[kocka][1]-1] in K) or [K[kocka][0]+1,K[kocka][1]-1] == M or K[kocka][0]==7 or K[kocka][1] == 0:
        lze_tahnout = False
    else:
        lze_tahnout=True
        K[kocka][1]-=1  #souřadnice sloupce
        K[kocka][0]+=1      #souřadnice řádku   
    return lze_tahnout
def vpravo(kocka: int):
    """Tah danou kočkou na pole vpravo dolů"""
    global K,M
    if ([K[kocka][0]+1,K[kocka][1]+1] in K) or [K[kocka][0]+1,K[kocka][1]+1] == M or K[kocka][0]==7 or K[kocka][1] == 7:
        lze_tahnout = False
    else:
        lze_tahnout=True
        K[kocka][1]+=1  #souřadnice sloupce
        K[kocka][0]+=1      #souřadnice řádku
    return lze_tahnout
#tahy myši
def vpred_vpravo():
    """Tah myši nahoru doprava"""
    global M,K 
    if ([M[0]-1,M[1]+1] in K) or M[0]==0 or M[1]==7:
        lze_tahnout = False
    else: 
        lze_tahnout = True
        M[1]+=1
        M[0]-=1  
    return lze_tahnout
def vpred_vlevo():
    """Tah myši nahoru doleva"""
    global M,K
    if ([M[0]-1,M[1]-1] in K) or M[0]==0 or M[1]==0:
        lze_tahnout = False
    else: 
        lze_tahnout = True
        M[1]-=1
        M[0]-=1
    return lze_tahnout
def vzad_vpravo():
    """Tah myši dolů doprava"""
    global M,K
    if ([M[0]+1,M[1]+1] in K) or M[0]==7 or M[1]==7:
        lze_tahnout = False
    else: 
        lze_tahnout = True
        M[1]+=1
        M[0]+=1
    return lze_tahnout
def vzad_vlevo():
    """Tah myši dolů doleva"""
    global M,K
    if ([M[0]+1,M[1]-1] in K) or M[0]==7 or M[1]==0:
        lze_tahnout = False
    else: 
        lze_tahnout = True
        M[1]-=1
        M[0]+=1
    return lze_tahnout

###########      NOTE minimax      ###########
nalezené_pozice={}
obtížnost="ruthless"
def minimax(K:list,M:list,tah_mysi:bool, depth:int, bV:list):  
    global mys, kolo, nalezené_pozice, obtížnost
    if obtížnost == "ruthless":
        dno=40-kolo
    elif obtížnost == "hard":
        dno=15
    elif obtížnost=="easy":
        dno=7
    if M[0] == 0:
        return 0 # myš vyhrála
    nalezeno = False

    
    if tah_mysi:      
        if depth>dno:   # maximální povolená hloubka
            return bV[0]    #best value #TODO měla by se vracet pozice myši, ne bV, ale zřejmě to funguje aj tak ¯\_(ツ)_/¯
        if M[0]<bV[0]:
            bV=[M[0],depth]
        elif bV[0]==M[0]:
            if depth<bV[1]:
                bV=[M[0],depth]

        LB,LF,RB,RF = muze_tahnout(K,M) # myš
        if ((not LB) and (not LF) and (not RB) and (not RF)):
            return 10 # myš prohrála; vyhrály kočky
        
        x=[]
        for i,j in enumerate((LB,RB,LF,RF)):    #TODO DRY
            if j:   #na pozici lze táhnout
                
                if i == 0:  #LB tah myši (left back)
                    t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0]+1,M[1]-1),False)
                    if t not in nalezené_pozice:
                        f=minimax(K,[M[0]+1,M[1]-1],False,depth+1,bV)
                        if f!=None:
                            x.append(f) 
                            nalezené_pozice[t]=x[-1]
                            if x[-1]==0:
                                break
                        else: x.append(12)
                    else: x.append(nalezené_pozice[t])

                elif i == 1:    #RB tah myši (right back)
                    t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0]+1,M[1]+1),False)
                    if t not in nalezené_pozice:  
                        f=minimax(K,[M[0]+1,M[1]+1],False,depth+1,bV)
                        if f!=None:                      
                            x.append(f) 
                            nalezené_pozice[t]=x[-1]
                            if x[-1]==0:
                                break
                        else:x.append(12)
                    else: x.append(nalezené_pozice[t])

                elif i == 2:    #LF tah myši (left forward)
                    t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0]-1,M[1]-1),False)
                    if t not in nalezené_pozice:
                        f=minimax(K,[M[0]-1,M[1]-1],False,depth+1,bV)
                        if f!=None:
                            x.append(f) 
                            nalezené_pozice[t]=x[-1]
                            if x[-1]==0:
                                break
                        else: x.append(12)
                    else: x.append(nalezené_pozice[t])

                elif i == 3:    #RF tah myši (right forward)
                    t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0]-1,M[1]+1),False)
                    if t not in nalezené_pozice:
                        f=minimax(K,[M[0]-1,M[1]+1],False,depth+1,bV)
                        if f!=None:
                            x.append(f) 
                            nalezené_pozice[t]=x[-1]
                        else:x.append(12)
                    else:x.append(nalezené_pozice[t])
            else: x.append(12) # 12 pokud na pozic a) nejde táhnout nebo b) minimax na pozici vrátil None

        if depth>0:
            if x!=[] and x!=4*[12]:
                return(min(x))
            
            else: 
                a,b=muzou_tahnout(K,M)
                if (True not in a) and (True not in b) and (RF or LF or RB or LB):
                    return 0
                else:
                    return None
        else:   # konec
            nalezené_pozice={}
            print(x)
            for i in reversed(range(len(x))):
                if x[i]==min(x): return i
            #return x.index(min(x))
    

    else: # tah koček           #TODO DRY
        R,L = muzou_tahnout(K,M) # kočky
        HtL = round((K[0][0]+K[1][0]+K[2][0]+K[3][0])/4)+4    # hold the line
        x=[]     
        vystup=8*[False]
        if R[0] and K[0][0]+1<=HtL:                         ### NOTE první z možných tahů koček 
            vystup[0]=True
            t = (frozenset(((K[0][0]+1,K[0][1]+1),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0],M[1]),True)
            if t not in nalezené_pozice:
                f=minimax([[K[0][0]+1,K[0][1]+1],K[1],K[2],K[3]],M,True,depth+1,bV)
                if f!=None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                    if x[-1]==10:
                        nalezeno = True
                else: vystup[0]=False
            else: x.append(nalezené_pozice[t])
          
        if R[1] and (not nalezeno) and K[1][0]+1<=HtL:      ### NOTE třetí z možných tahů koček
            vystup[1]=True
            t= (frozenset(((K[0][0],K[0][1]),(K[1][0]+1,K[1][1]+1),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0],M[1]),True) 
            if t not in nalezené_pozice:
                f=minimax([K[0],[K[1][0]+1,K[1][1]+1],K[2],K[3]],M,True,depth+1,bV)
                if f !=None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                    if x[-1]==10:
                        nalezeno = True   
                else: vystup[1]=False
            else: x.append(nalezené_pozice[t])
        
        if R[2] and (not nalezeno) and K[2][0]+1<=HtL:      ### NOTE pátý z možných tahů koček
            vystup[2]=True
            t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0]+1,K[2][1]+1),(K[3][0],K[3][1]))),(M[0],M[1]),True)
            if t not in nalezené_pozice:
                f=minimax([K[0],K[1],[K[2][0]+1,K[2][1]+1],K[3]],M,True,depth+1,bV)
                if f!=None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                    if x[-1]==10:
                        nalezeno = True  
                else: vystup[2]=False
            else: x.append(nalezené_pozice[t])
        
        if R[3] and (not nalezeno) and K[3][0]+1<=HtL:      ### NOTE sedmý z možných tahů koček
            vystup[3]=True
            t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0]+1,K[3][1]+1))),(M[0],M[1]),True)
            if t not in nalezené_pozice:
                f=minimax([K[0],K[1],K[2],[K[3][0]+1,K[3][1]+1]],M,True,depth+1,bV)
                if f !=None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                    if x[-1]==10:
                        nalezeno = True 
                else: vystup[3]=False
            else: x.append(nalezené_pozice[t])           
    
        if L[0] and (not nalezeno) and K[0][0]+1<=HtL:      ### NOTE druhý z možných tahů koček
            vystup[4]=True
            t = (frozenset(((K[0][0]+1,K[0][1]-1),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0],M[1]),True)
            if t not in nalezené_pozice:
                f=minimax([[K[0][0]+1,K[0][1]-1],K[1],K[2],K[3]],M,True,depth+1,bV)
                if f != None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                    if x[-1]==10:
                        nalezeno = True 
                else: vystup[4]=None
            else: x.append(nalezené_pozice[t])   
                    
        if L[1] and (not nalezeno) and K[1][0]+1<=HtL:      ### NOTE čtvrtý z možných tahů koček
            vystup[5]=True
            t=(frozenset(((K[0][0],K[0][1]),(K[1][0]+1,K[1][1]-1),(K[2][0],K[2][1]),(K[3][0],K[3][1]))),(M[0],M[1]),True)
            if t not in nalezené_pozice:
                f=minimax([K[0],[K[1][0]+1,K[1][1]-1],K[2],K[3]],M,True,depth+1,bV)
                if f !=None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                    if x[-1]==10:
                        nalezeno = True    
                else: vystup[5]=False
            else: x.append(nalezené_pozice[t])  

        if L[2] and (not nalezeno) and K[2][0]+1<=HtL:      ### NOTE šestý z možných tahů koček
            vystup[6]=True
            t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0]+1,K[2][1]-1),(K[3][0],K[3][1]))),(M[0],M[1]),True)
            if t not in nalezené_pozice:
                f=minimax([K[0],K[1],[K[2][0]+1,K[2][1]-1],K[3]],M,True,depth+1,bV)
                if f != None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                    if x[-1]==10:
                        nalezeno = True  
                else: vystup[6]=False
            else: x.append(nalezené_pozice[t])

        if L[3] and (not nalezeno) and K[3][0]+1<=HtL:      ### NOTE osmý z možných tahů koček
            vystup[7]=True
            t=(frozenset(((K[0][0],K[0][1]),(K[1][0],K[1][1]),(K[2][0],K[2][1]),(K[3][0]+1,K[3][1]-1))),(M[0],M[1]),True)           
            if t not in nalezené_pozice:
                f=minimax([K[0],K[1],K[2],[K[3][0]+1,K[3][1]-1]],M,True,depth+1,bV)
                if f != None:
                    x.append(f)
                    nalezené_pozice[t]=x[-1]
                else: vystup[7]=False
            else: x.append(nalezené_pozice[t])

        if depth>0:
            if x!=[]:
                return(max(x))
            else: return None     
        else:   # konec
            x0=8*[]
            for i in range(8):
                if vystup[i]:
                    x0.append(x.pop(0))
                else: x0.append(-2)
            print(x0)
            nalezené_pozice={}
            if x0.count(max(x0))==1:
                return [x0.index(max(x0))]
            else: 
                vysl=[]
                for i in range(8):
                    if x0[i]==max(x0):
                        vysl.append(i)
                return vysl
####################    konec minimaxu      ######################


#NOTE grafické znázornění stavu hry: šachovnice

def show(board):
    print("\n0  0 1 2 3 4 5 6 7 y")
    for i in range(8):
        print(f"{i} ",end="")
        for j in range(8):
            print(board[i][j], end="")
        if i == 3:
            print(f"    K1:({K[0][0]},{K[0][1]}) K2:({K[1][0]},{K[1][1]}) K3:({K[2][0]},{K[2][1]}) K4:({K[3][0]},{K[3][1]})")
        elif i == 5:
            print(f"    M:({M[0]},{M[1]})")
        else: print("")
    print("x\n")

def aktualizuj(board):
    global K,M,B,C,Ž
    if C!=tuple(M):
        board[Ž[0]][Ž[1]],board[C[0]][C[1]],board[M[0]][M[1]]="⬜","🟨","🐭" 
        Ž,C=tuple(C),tuple(M)
    else:
        for i in range(4):
            if B[i]!=tuple(K[i]):
                board[Ž[0]][Ž[1]],board[B[i][0]][B[i][1]],board[K[i][0]][K[i][1]]="⬜","🟨","🐱"
                Ž,B[i]=tuple(B[i]),tuple(K[i])
                break

#######                      NOTE hra               #########

restart = True
while restart:
    board =[["🐱","⬛","🐱","⬛","🐱","⬛","🐱","⬛"],
            ["⬛","⬜","⬛","⬜","⬛","⬜","⬛","⬜"],
            ["⬜","⬛","⬜","⬛","⬜","⬛","⬜","⬛"],
            ["⬛","⬜","⬛","⬜","⬛","⬜","⬛","⬜"],
            ["⬜","⬛","⬜","⬛","⬜","⬛","⬜","⬛"],
            ["⬛","⬜","⬛","⬜","⬛","⬜","⬛","⬜"],
            ["⬜","⬛","⬜","⬛","⬜","⬛","⬜","⬛"],
            ["⬛","⬜","⬛","🐭","⬛","⬜","⬛","⬜"]]

    kolo=0
    vyhraly_kocky,vyhrala_mys = False,False
    valid = True

    x=0
    while (x!="1" and x!="2"):
        x = input("Vyber si, jestli chceš hrát za myš (napiš 1) nebo za kočky (napiš 2) a potvrď stisknutím klávesy enter\n")
    if x == "1":
        mys = True
        print("Hraješ za myš, pro zobrazení nápovědy napiš help")
    else:
        mys = False
        print("Hraješ za kočky, pro zobrazení nápovědy napiš help")

    #NOTE počáteční pozice
    M = [7,3] #pozice myši
    K = [[0,0],[0,2],[0,4],[0,6]] #pozice koček; K[0],K[1],K[2],K[3]
    B,C,Ž = [(0,0),(0,2),(0,4),(0,6)],(7,3),(4,6) #pomocné hodnoty pozic pro aktualizaci šachovnice

    if mys: #hráč hraje za myš, počítač za kočky
        while (not vyhraly_kocky) and (not vyhrala_mys):
            LB,LF,RB,RF=muze_tahnout(K,M)
            if LB or LF or RB or RF:
                valid = True
                show(board)
                while valid:
                    # NOTE tah hráče (myš)
                    tah = input(f"Kolo {kolo+1}, jsi na tahu, tahy: vpřed vlevo: 7, vpřed vpravo: 9, vzad vlevo: 1, vzad vpravo: 3 \n")
                    if tah=="help":
                        print("\nNapište \"restart\" pro ukončení partie, \"settings\" pro změnu obtížnosti,\n\nTah vpravo vpřed \"9\", tah vlevo vpřed \"7\", tah vlevo vzad \"1\", tah vpravo vzad \"3\"\n")
                    elif tah=="restart":
                        vyhrala_mys=True
                        valid=False
                    elif tah== "settings" or tah=="nastavení" or tah=="obtížnost":
                        z=input(f"Obtížnost je >{obtížnost}<, obtížnost změníš když nyní napíšeš příslušný příkaz (bez uvozovek): \"ruthless\", \"hard\", \"easy\"\n>>",
                              )
                        if z=="hard" or z=="normal" or z == "easy":
                            obtížnost=z
                    elif tah == "1":
                        if LB: 
                            vzad_vlevo()
                            valid=False
                        else: print("tam nelze táhnout")
                    elif tah == "7":
                        if LF:
                            vpred_vlevo()
                            valid=False
                        else: print("tam nelze táhnout")
                    elif tah == "3":
                        if RB: 
                            vzad_vpravo()
                            valid=False
                        else: print("tam nelze táhnout")
                    elif tah == "9":
                        if RF:
                            vpred_vpravo()
                            valid=False
                        else: print("tam nelze táhnout")
                    else: print("Neznámý příkaz")
                aktualizuj(board)
                show(board)
            else:
                vyhraly_kocky=True
                aktualizuj(board)
                show(board)
                break
            if M[0]==0: vyhrala_mys=True

            else:           # NOTE tah počítače (kočky)               
                print(f"Kolo {kolo+1}, protihráč je na tahu, přemýšlí... ")   
                if kolo<4:
                    vpravo(kolo)
                else:
                    x=minimax(K,M,False,0,[M[0],0])
                    for i in x:
                        if i>=4:
                            if vlevo(i-4): break
                        else: 
                            if vpravo(i): break
                aktualizuj(board)
                kolo+=1

    else: # hráč hraje za kočky, počítač za myš
        while (not vyhraly_kocky) and (not vyhrala_mys):    # NOTE tah počítače (myš)
            print(f"Kolo {kolo+1}, protihráč je na tahu, přemýšlí...")
            LB,LF,RB,RF=muze_tahnout(K,M)
            if LB or LF or RB or RF:        # myš může táhnout
                if kolo<2:
                    if RF: vpred_vpravo()
                    elif LF: vpred_vlevo()
                    else: vzad_vlevo()
                elif kolo<4:
                    if RF: vpred_vlevo()
                    elif LF: vpred_vpravo()
                    else: vzad_vlevo()
                elif min(K[0][0],K[1][0],K[2][0],K[3][0])>= M[0]:
                    if RF: vpred_vpravo()
                    else: vpred_vlevo()
                else:
                    x=minimax(K,M,True,0,[M[0],0])
                    if x==0: vzad_vlevo()
                    elif x==1: vzad_vpravo()
                    elif x==2: vpred_vlevo()
                    elif x==3: vpred_vpravo()
                    else: print("chyba")
                aktualizuj(board)
                show(board)
                if M[0]==0:
                    vyhrala_mys = True
                    break
                
                valid = True    # NOTE tah hráče (kočky)
                while valid:
                    tah = input(f"Kolo {kolo+1}, jsi na tahu, (číslo kočky(1 až 4) a 1 pro tah vlevo, 2 vpravo: např. pokyn 41 je pro tah kočky 4 vlevo)\n")
                    if tah.isnumeric() and (tah[1]=="2") and int(tah[0])<5 and int(tah[0])>=0:
                        if not vpravo(int(tah[0])-1):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah.isnumeric() and (tah[1]=="1") and int(tah[0])<5 and int(tah[0])>=0:
                        if not vlevo(int(tah[0])-1):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="restart":
                        vyhrala_mys=True
                        valid=False
                    elif tah == "help":
                        print("\nNapište \"restart\" pro ukončení partie, \"settings\" pro změnu obtížnosti,\n\nTah kočkou 1 vlevo \"11\", tah kočkou 1 vpravo \"12\",tah kočkou 2 vlevo \"21\", tah kočkou 2 vpravo \"22\",\nTah kočkou 3 vlevo \"31\", tah kočkou 3 vpravo \"32\", tah kočkou 4 vlevo \"41\", tah kočkou 4 vpravo \"42\"\n")
                    elif tah== "settings" or tah=="nastavení" or tah=="obtížnost":
                        z=input(f"Obtížnost je >{obtížnost}<, obtížnost změníš když nyní napíšeš příslušný příkaz (bez uvozovek): \"ruthless\", \"hard\", \"easy\"\n>>",
                              )
                        if z=="hard" or z=="normal" or z == "easy":
                            obtížnost=z
                    elif tah=="a": 
                        if not vlevo(0):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="s": 
                        if not vpravo(0):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="d": 
                        if not vlevo(1):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="f": 
                        if not vpravo(1):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="j": 
                        if not vlevo(2):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="k": 
                        if not vpravo(2):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="l": 
                        if not vlevo(3):
                            print("Tam táhnout nelze")
                        else: valid=False
                    elif tah=="ů" or tah ==";": 
                        if not vpravo(3):
                            print("Tam táhnout nelze")
                        else: valid=False
                    else: print("Neznámý příkaz")
                aktualizuj(board)
                show(board)
                kolo+=1

            else:           # myš nemůže táhnout
                vyhraly_kocky = True 
                aktualizuj(board)
                show(board)     



    if (vyhraly_kocky and not mys) or (vyhrala_mys and mys):
        print("Vyhrál jsi!",end="\n\n")
    elif (vyhraly_kocky and mys) or (vyhrala_mys and not mys):
        print("Prohrál jsi",end="\n\n")
    else: pass
    rst=input("Chceš hrát znovu? Pokud ano, napiš 1 a stiskni enter. Jinak hra skončí.")
    if rst=="1":
        pass
    else: restart=False
