import json,os,urllib.request
def post(u,p,b):return json.load(urllib.request.urlopen(urllib.request.Request(u+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})))
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0}
I=10**9
KN=(8,12,19,21,-8,-12,-19,-21);BD=(9,11,-9,-11);RD=(1,10,-1,-10);KG=BD+RD
D={'N':KN,'K':KG,'B':BD,'R':RD,'Q':KG}
def P(fen):
 f=fen.split();b=list("##########"+"#........#"*8+"##########"*3)
 for i,row in enumerate(f[0].split("/")):
  x=0
  for c in row:
   if c.isdigit():x+=int(c)
   else:b[(i+1)*10+x+1]=c;x+=1
 ep=-1
 if f[3]!="-":ep=(9-int(f[3][1]))*10+"abcdefgh".index(f[3][0])+1
 return "".join(b),f[1]=="w",ep
def A(b,sq,byw):
 for ds,ps,sl in (((9,11) if byw else (-9,-11),'P' if byw else 'p',0),(KN,'N' if byw else 'n',0),(KG,'K' if byw else 'k',0),(BD,'BQ' if byw else 'bq',1),(RD,'RQ' if byw else 'rq',1)):
  for d in ds:
   t=sq+d
   if sl:
    while b[t]=='.':t+=d
   if b[t] in ps:return True
 return False
def G(b,w,ep,caps=False):
 ms=[]
 for i in range(11,89):
  pc=b[i]
  if pc in '#.' or pc.isupper()!=w:continue
  u=pc.upper()
  if u=='P':
   fw=-10 if w else 10;home=i//10==(7 if w else 2);t=i+fw;pr='q' if t<20 or t>80 else ''
   if b[t]=='.' and not caps:
    ms.append((i,t,pr))
    if home and b[i+2*fw]=='.':ms.append((i,i+2*fw,''))
   for d in (fw-1,fw+1):
    t=i+d
    if b[t] not in '#.' and b[t].isupper()!=w:ms.append((i,t,pr))
    elif t==ep:ms.append((i,t,'e'))
  else:
   for d in D[u]:
    t=i+d
    while b[t]=='.':
     if not caps:ms.append((i,t,''))
     if u in 'NK':break
     t+=d
    else:
     if b[t]!='#' and b[t].isupper()!=w:ms.append((i,t,''))
 return ms
def M(b,m,ep):
 i,j,pr=m;pc=b[i];lst=list(b);lst[i]='.';lst[j]=('Q' if pc=='P' else 'q') if pr=='q' else pc
 if pr=='e':lst[j+10 if pc=='P' else j-10]='.'
 return "".join(lst),(i+j)//2 if pc.upper()=='P' and abs(j-i)==20 else -1
def E(b,w):
 s=0;mat=sum(V[c.upper()] for c in b if c not in '#.' and c.upper() not in 'KP')
 for i in range(11,89):
  pc=b[i]
  if pc in '#.':continue
  u=pc.upper();f=i%10-1;rr=8-i//10 if pc.isupper() else i//10-1;cen=min(f,7-f)+min(rr,7-rr)
  pos={'P':rr*7+(14 if f in (3,4) else 0),'N':cen*6-18*(rr==0),'B':cen*3,'R':16 if rr==6 else 0,'Q':cen*2,'K':cen*14-60 if mat>1600 else abs(f-3)*-6}[u]
  s+=(V[u]+pos) if pc.isupper() else -(V[u]+pos)
 s+=25*(b.count('B')>1)-25*(b.count('b')>1)
 return s if w else -s
ND=[0];Abort=Exception
def Q(b,w,ep,alpha,beta):
 ND[0]+=1
 if ND[0]>7000:raise Abort
 stand=E(b,w)
 if stand>=beta:return beta
 if stand>alpha:alpha=stand
 ms=G(b,w,ep,True);ms.sort(key=lambda m:-V.get(b[m[1]].upper(),80)*10)
 for m in ms:
  nb,nep=M(b,m,ep)
  if A(nb,nb.index('K' if w else 'k'),not w):continue
  sc=-Q(nb,not w,nep,-beta,-alpha)
  if sc>=beta:return beta
  if sc>alpha:alpha=sc
 return alpha
def S(b,w,ep,depth,alpha,beta):
 if depth<=0:return Q(b,w,ep,alpha,beta)
 ND[0]+=1
 if ND[0]>7000:raise Abort
 best=-I
 for m in sorted(G(b,w,ep),key=lambda m:(1<<20)+V[b[m[1]].upper()]*10-V[b[m[0]].upper()] if b[m[1]] not in '#.' else (1<<19) if m[2]=='q' else 0,reverse=True):
  nb,nep=M(b,m,ep)
  if A(nb,nb.index('K' if w else 'k'),not w):continue
  sc=-S(nb,not w,nep,depth-1,-beta,-alpha)
  if sc>best:best=sc
  if sc>alpha:alpha=sc
  if alpha>=beta:break
 return best
def uci(m):return "abcdefgh"[m[0]%10-1]+str(9-m[0]//10)+"abcdefgh"[m[1]%10-1]+str(9-m[1]//10)+(m[2]=='q')*'q'
def C(fen,legal):
 b,w,ep=P(fen);root=[m for m in G(b,w,ep) if uci(m) in legal]
 if not root:return legal[0]
 best=root[0];ND[0]=0
 try:
  for depth in range(1,40):
   cur=None;cs=alpha=-I
   for m in sorted(root,key=lambda m:m!=best):
    nb,nep=M(b,m,ep);sc=-S(nb,not w,nep,depth-1,-I,-alpha)
    if sc>cs:cs=sc;cur=m
    if sc>alpha:alpha=sc
   if cur:best=cur
   if ND[0]>4500:break
 except Abort:pass
 return uci(best)
if __name__=="__main__":
 U=os.environ["MAKEFUN_ENV_URL"];g=post(U,"/game",{})
 while g["status"]!="done":
  while g["status"]=="your_move":g=post(U,"/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})
  if g["status"]!="done":g=post(U,"/game",{})
