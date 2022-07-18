import os,time
import pandas as pd
from ortools.algorithms import pywrapknapsack_solver
def get_data(link):
   file_list=open(link,"r").read().split("\n") 
   capacities=[]  
   capacities.append(int(file_list[2]))  
   values=[]
   weights=[[]]
   for a in file_list[4:-1]:
      b=a.split(" ")
      values.append(int(b[0]))
      weights[0].append(int(b[1]))
   return values, weights, capacities
folderpath = "kplib"
dict_group = {0:"00Uncorrelated",1:"01WeaklyCorrelated",2:"02StronglyCorrelated",3:"03InverseStronglyCorrelated",
              4:"04AlmostStronglyCorrelated"  , 5:"05SubsetSum",6:"06UncorrelatedWithSimilarWeights" ,
              7:"07SpannerUncorrelated" ,8:"08SpannerWeaklyCorrelated" ,9: "09SpannerStronglyCorrelated"
               , 10:"10MultipleStronglyCorrelated" , 11:"11ProfitCeiling" ,12: "12Circle"
              }
item_amount_folder={50:"n00050",100:"n00100",200:"n00200",500:"n00500",
                    1000:"n01000",2000:"n02000"} #5000:"n05000",10000:"n10000"}


def main():
    computed_value_table=[]   #bang chua gia tri value da duoc tinh toan trong thoi gian toi da
    total_weight_table=[]  #bang chua gia tri total weight cho loi giai tot nhat
    optimal_table=[] #bang danh gia ket qua co toi uu hay khong
    list_size=[]     #danh sach chua cac kich thuoc duoc su dung, muc dich de tao thong tin cot cho table
    list_name=[]     #danh sach ten thu muc duoc su dung, muc dich de tao cot header cho table
   
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    #Cai dat thoi gian thuc nghiem de danh gia toi uu
    
    time_limit=1

    #Tao list ten cac nhom test case duoc su dung
    for group in dict_group:
      list_name.append(dict_group[group])  
    for item in item_amount_folder:
      computed_value_list = []
      total_weight_list=[]
      list_optimal=[]
      list_size.append(item)
      for group in dict_group:
         path=(os.path.join(folderpath,dict_group[group],item_amount_folder[item],"R01000","s000.kp"))   #join string to get path to kp file
         values,weights,capacities= get_data(path) 
         solver.Init(values, weights, capacities)
         solver.set_time_limit(time_limit)
         t0=time.time()        #Thoi gian luc chuan bi chay thuat toan
         computed_value = solver.Solve()   #Chuong trinh hoat dong
         t1=time.time()-t0    #Bien t1 la hieu thoi gian luc chua chay va sau khi chay thuat toan
         optimal=True         #Tra ve ket qua dung cho bai toan toi uu hay chua
         if t1>=time_limit:   #Neu thoi gian chay > thoi gian toi da, tra ve False
            optimal=False
         packed_items = []   
         packed_weights = []
         total_weight = 0
         #print('Total value =', computed_value)
         for i in range(len(values)):
              if solver.BestSolutionContains(i):
                packed_items.append(i)
                packed_weights.append(weights[0][i])
                total_weight += weights[0][i]
         total_weight_list.append(total_weight)          #them gia tri tong trong luong vao list
         computed_value_list.append(computed_value)         #them gia tri da duoc giai trong thoi gian time_limit
         list_optimal.append(optimal)   
         print("Result for",path)
         print('Total weight:', total_weight)
         print('Packed items:', packed_items)
         print('Packed_weights:', packed_weights)  
                    #them gia tri 
      computed_value_table.append(computed_value_list)               #them list de tao dataframe
      total_weight_table.append(total_weight_list)
      optimal_table.append(list_optimal)
      print("--------------------------------------")
      print("Case with",item, "items done")
      print("--------------------------------------")
    #Tao dataframe voi value_table, header la list_name
    computed_value_table_df=pd.DataFrame(computed_value_table,columns=list_name)
    #Them cot chua kich thuoc
    computed_value_table_df.insert(loc=0, column="testcases", value=list_size)   
    #Ghi ket qua ra file csv
    computed_value_table_df.to_csv("computed_value_table.csv", index=False)   
    #Tuong tu o tren       
    total_weight_table=pd.DataFrame(total_weight_table,columns=list_name)
    total_weight_table.insert(loc=0, column="testcases", value=list_size)
    total_weight_table.to_csv("total_weight_table.csv", index=False)
    optimal_table_df=pd.DataFrame(optimal_table, columns=list_name)
    optimal_table_df.insert(loc=0, column="testcases", value=list_size)
    optimal_table_df.to_csv("optimal_table.csv", index=False)
     

if __name__ == '__main__':
    main()

