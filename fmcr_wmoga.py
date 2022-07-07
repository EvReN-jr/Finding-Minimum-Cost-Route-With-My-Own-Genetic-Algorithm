!pip install openpyxl==3.0.9 
import pandas as pd
import numpy as np
import random
import openpyxl
import time


data_c1= pd.read_excel("1-2_cost.xlsx")
data_c2= pd.read_excel("2-3_cost.xlsx")
data_c3= pd.read_excel("3-4_cost.xlsx")
data_c0= pd.read_excel("1-4_cost.xlsx")
data_d0= pd.read_excel("1-4_demand.xlsx")
data_opc= pd.read_excel("OpeningCost_of_Regions.xlsx")
data_clc= pd.read_excel("ClosingCost_of_Regions.xlsx")
data_cap= pd.read_excel("Capacity_of_Regions.xlsx")

def F_create_sector_number():
  while True:
    x=random.randint(0,region_count)
    y=random.randint(0,region_count)
    if x==0 or y==0:
      x,y=0,0
    return x,y
    break

# Creates routes.
def F_creat_person(s_p,f_p):
  while True:
      x,y=F_create_sector_number()
      ch=np.concatenate(([s_p],[x],[y],[f_p]))
      if C_transport_probability(ch):
        return ch
        break
        
def F_sector_list(family):
  open_s,close_s=[],[]
  for ch in family:
    for j in ch[1:-1]:
      if j!=0:
        if j not in open_s:
          open_s.append(j)
  for i in range(1,region_count+1):
    if i not in open_s:
      close_s.append(i)
  return open_s,close_s

def F_cost(open_sectors,close_sectors,family):
    t=0
    for ch in family:
      m=0
      if ch[1]==0:
        pass
        m+=data_c0[ch[0]][ch[-1]]*data_d0[ch[-1]][ch[0]]
      else:
        m+= data_c1[ch[0]][ch[1]] + data_c2[ch[1]][ch[2]] + data_c3[ch[2]][ch[3]]
        m*=data_d0[ch[-1]][ch[0]]
      t+=m
    for i in open_sectors:
      t+=data_opc[i-1]
    for i in close_sectors:
      t+=data_clc[i-1]
    return t

#Routes total cost base package is being optimized.
def F_main_F(family,c=1,p_l=[]):
  prime_family=np.copy(family)
  c_family=np.copy(family)
  min_val=0
  epoch=len(family)

  open_s,close_s=F_sector_list(prime_family)
  ref_p_f_cost=F_cost(open_s,close_s,prime_family)

  # Routes that do not comply with the rule are corrected and optimized.
  if c==0:
    for k in range(5):
      for i in p_l:
        s_p=family[i][0]
        for j in range(int(epoch/2)):
          c_family[i]=np.concatenate(([s_p],[random.randint(1,region_count)],family[i][2:]))
          open_s,close_s=F_sector_list(c_family)
          c_f_maliyet=F_cost(open_s,close_s,c_family)
          if min_val>c_f_maliyet or min_val==0:
            min_val=c_f_maliyet
            prime_family[i]=np.copy(c_family[i])
        c_family[i]=np.copy(prime_family[i])
      open_s,close_s=F_sector_list(prime_family)
      p_f_cost=F_cost(open_s,close_s,prime_family)

  else:
    for k in range(region_count*7):
      for i in range(epoch):
        s_p=family[i][0]
        f_p=family[i][-1]
        for j in range(int(epoch/2)):
          c_family[i]=F_creat_person(s_p,f_p)
          open_s,close_s=F_sector_list(c_family)
          c_f_maliyet=F_cost(open_s,close_s,c_family)
          if min_val>c_f_maliyet or min_val==0:
            min_val=c_f_maliyet
            prime_family[i]=np.copy(c_family[i])

        c_family[i]=np.copy(prime_family[i])

      open_s,close_s=F_sector_list(prime_family)
      p_f_cost=F_cost(open_s,close_s,prime_family)

  return prime_family,p_f_cost

s_t=time.time()
decision=[]
for c in range(5): 
  def C_transport_probability(p):
    v=data_d0[p[-1]][p[0]]
    for i in p:
      c=data_cap[i]
      if v>c:
        return False
      elif i==p[-1]:
        return True

  def C_sector_status():
    open_s=[]
    close_s=[]
    for j,i in enumerate(data_opc):
      if i==0:
        open_s.append(j+1)
      else:
        close_s.append(j+1)
    return open_s,close_s

  # List of sector to open and close according to the ideal route.
  def C_sector_list(p,open_s,close_s):
    for i in range(total_region_count):
      if (i in p[1:-1]) and (i in close_s):
        close_s.remove(i)
        open_s.append(i)
      elif (i not in p[1:-1]) and (i in open_s):
        open_s.remove(i)
        close_s.append(i)           
    return open_s,close_s

  def C_route_cost(w):
    q=0
    if w[1]==0:
      q+=round(data_c0[w[0]][w[-1]],4)
      q*=data_d0[w[-1]][w[0]]# Unit cost multiplied by demand
      for i in range(1,region_count+1):
        if i not in w:
          q+= data_clc[i-1]# The cost of closing unused sector.

    if w[1]!=0:
      q += round(data_c1[w[0]][w[1]] + data_c2[w[1]][w[2]] + data_c3[w[2]][w[3]],4)
      q*=data_d0[w[-1]][w[0]]
      for i in range(1,region_count+1):
        if i in w[1:-1]:
          q+=data_opc[i-1]
        else:
          q+= data_clc[i-1]

    return q

  def C_create_sector_number(c):
    while True:
      x=random.randint(1,region_count)
      if c==0:
        y=random.randint(1,region_count)
        return x,y
        break
      if c==1:
        return x
        break

  def C_cr_pa():
    while True:
      p_1=[]
      p_1.append(s)
      while True:
        x=random.randint(1,region_count)
        p_1.append(x)
        if len(p_1)==3:
          p_1.append(f)
          break
        if region_count<4:
          p_1.append(f)
          break
      
      p_2=[]
      p_2.append(s)
      while True:
        x=random.randint(1,region_count)
        p_2.append(x)
        if len(p_2)==3:
          p_2.append(f)
          break

      if C_transport_probability(p_1) and C_transport_probability(p_2) and (not np.array_equal(p_1,p_2)):
        break

    return p_1,p_2

  def C_route_test(p,chl):
    if np.array_equal([not np.array_equal(i,p) for i in chl],np.ones(len(chl))):
      return True
    else:
      return False

  def C_create_route(p_1,p_2):
    chl=[]
    costs=[]
    costs.append(C_route_cost(p_1))
    costs.append(C_route_cost(p_2))
    chl.append(p_1)
    chl.append(p_2)

    while len(chl)<=region_count:
      #Mutation
        #two point mutation
      if region_count>4:
        for i in range(10):
          while True:
            x,y=C_create_sector_number(0)
            c_1_1=np.concatenate(([s],[x],[y],[f]))
            
            x,y=C_create_sector_number(0)
            c_1_2=np.concatenate(([s],[x],[y],[f]))

            if C_transport_probability(c_1_1) and C_transport_probability(c_1_2):
              cc_1_1=C_route_cost(c_1_1)
              cc_1_2=C_route_cost(c_1_2)

              if cc_1_1<cc_1_2:
                if C_route_test(c_1_1,chl):
                  costs.append(cc_1_1)
                  chl.append(c_1_1)
              else:
                if C_route_test(c_1_2,chl):
                  costs.append(cc_1_2)          
                  chl.append(c_1_2)
              break

            else:
              continue
      
      
          #one point mutation
      if region_count>4:
        for i in range(10):
          while True:  
            x=C_create_sector_number(1)
            c_3_1=np.concatenate((p_1[:2],[x],[f]))
            x=C_create_sector_number(1)
            c_3_2=np.concatenate((p_2[:2],[x],[f]))
            if C_transport_probability(c_3_1) and C_transport_probability(c_3_2):
              cc_3_1=C_route_cost(c_3_1)
              cc_3_2=C_route_cost(c_3_2)

              if cc_3_1<cc_3_2:
                if C_route_test(c_3_1,chl):
                  costs.append(cc_3_1)          
                  chl.append(c_3_1)
              
              else:
                if C_route_test(c_3_2,chl):
                  costs.append(cc_3_2)          
                  chl.append(c_3_2)
              break
              
            else:
              continue
        
        for i in range(10):
          while True:  
            x=C_create_sector_number(1)
            c_2_1=np.concatenate(([s],[x],p_1[2:]))
            x=C_create_sector_number(1)
            c_2_2=np.concatenate(([s],[x],p_1[2:]))

            if C_transport_probability(c_2_1) and C_transport_probability(c_2_2):
              cc_2_1=C_route_cost(c_2_1)
              cc_2_2=C_route_cost(c_2_2)

              if cc_2_1<cc_2_2:
                if C_route_test(c_2_1,chl):
                  costs.append(cc_2_1)          
                  chl.append(c_2_1)
                
              else:
                if C_route_test(c_2_2,chl):
                  costs.append(cc_2_2)          
                  chl.append(c_2_2)
              break
              
            else:
              continue
    # crossing over
    for i in range(region_count):
      while True:
        if region_count<5:
          x,y=0,1
        else:
          x,y=C_create_sector_number(0)

        c_4_1=np.concatenate(([s],[chl[y][1]],chl[x][2:]))
        c_4_2=np.concatenate((chl[y][:2],[chl[x][2]],[f]))

        if C_transport_probability(c_4_1) and C_transport_probability(c_4_2):
          cc_4_1=C_route_cost(c_4_1)
          cc_4_2=C_route_cost(c_4_2)
          if cc_4_1<cc_4_2:
            if C_route_test(c_4_1,chl):
                costs.append(cc_4_1)          
                chl.append(c_4_1)
          else:
            if C_route_test(c_4_2,chl):
                costs.append(cc_4_2)          
                chl.append(c_4_2)
          break
          
        else:
          continue

    #directly
    c_5_1=np.concatenate(([s],[0],[0],[f]))
    if C_route_test(c_5_1,chl):
      costs.append(C_route_cost(c_5_1))          
      chl.append(c_5_1)
    
    return chl[np.argmin(costs)]


  
  def C_routes_cost(pool):
    p_c=[]
    for i in pool:
      p_c.append(C_route_cost(i))
    return min(p_c)

  
  def C_sector_status_and_cost(open_sectors,rotalar):
    dsda=[]
    dsdk=[]
    t=0

    for p in rotalar:
      m=0
      if p[1]==0:
        m+= data_c0[p[0]][p[-1]]
      else:
        m+= data_c1[p[0]][p[1]] + data_c2[p[1]][p[2]] + data_c3[p[2]][p[3]]
      m*=data_d0[p[-1]][p[0]]
      t+=m
        
    for i in open_sectors:
      for j in i:
        if j not in dsda:
          dsda.append(j)

    for i in range(1,region_count+1):
      if i not in dsda:
        dsdk.append(i)
    

    for i in dsda:
      t+=data_opc[i-1]
    for i in dsdk:
      t+=data_clc[i-1]

    return dsda,dsdk,t

  
  def C_best_chl():
    p_1,p_2=C_cr_pa()
    pool=[p_1,p_2]
    C_sector_status()
    for i in range(5):
      x,y=0,0
      while x==y:
        x=random.randint(0,len(pool)-1)
        y=random.randint(0,len(pool)-1)
      
      if 0 not in pool[x] and 0 not in pool[y]:
        pr_chl=C_create_route(pool[x],pool[y])
        if C_route_cost(pr_chl)<C_routes_cost(pool):
          pool.append(pr_chl)
      

    best=[]
    for i in pool:
      best.append(C_route_cost(i))

    best=np.array(best)

    open_s,close_s=C_sector_status()
    open_s,close_s=C_sector_list(pool[np.argmin(best)],open_s,close_s)
    return open_s,np.array(pool[np.argmin(best)])
  
  ### Write how much region use for this transport process.
  region_count=7
    
  total_region_count=len(data_c0)
  open_sectors=[]
  routes=[]
  open_s=[]
  route=[]

  for i in range(1,region_count+1):
    for j in range(1,region_count+1):
      if data_d0[j][i]!=0:
        s,f=i,j
        open_s,route=C_best_chl()
        open_sectors.append(open_s)
        routes.append(list(route))

  decision.append([routes,C_sector_status_and_cost(open_sectors,routes)[2]])

family=[i[0] for i in decision if i[1]==np.min([i[1] for i in decision])][0]
f_family=F_main_F(family)[0]

# Routes that do not comply with the rule have been detected, corrected and optimized.
c=[]
v=[]
for j in range(1,region_count+1):
  f=[[k,list(i)] for k,i in enumerate(f_family) if i[3]==j and i[2]!=0]
  chc=[[k[1][2]==[i[1][2] for i in f][t] for k in f ] for t in range(len(f)-1)]
  if not np.array_equal(chc,np.array(np.ones(len(f)),ndmin=2)) and len(f)>1:
    if not np.array_equal([i[1][2] for i in f]-f[0][1][2],np.zeros(len(f))):
      t=list(set([i[1][2] for i in f]))
      v.append(t)
      c.append(f)
        
for i,j in enumerate(c):
  f_f=[]
  for k in v[i]:
    for l in j:
      f_family[l[0]][2]=k
    f_f.append(F_main_F(f_family,0,[i[0] for i in j]))
  f_family=np.copy(f_f[np.argmin([i[1] for i in f_f])][0])

# Output.
open_s,close_s=F_sector_list(f_family)
print("routes\n",f_family)
print("Cost:",F_cost(open_s,close_s,f_family))
print("Open Sectors:",open_s)
print("Time Elapsed (s):",int(time.time()-s_t))
