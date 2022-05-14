import pandas as pd
import numpy as np

class Adj_Matrix(object): #class for adjacency matrix
    def __init__(self, size):
        self.matrix = np.zeros((size,size))
        self.size = size

    def get_weight(self, v_purchaser, v_user):
        return self.matrix[v_purchaser][v_user]

    def add_edge(self, v_purchaser, v_user, weight): 
        curr_weight = self.get_weight(v_purchaser, v_user)
        self.matrix[v_purchaser][v_user] = weight + curr_weight

def parse_string(name_str):
    name_str = name_str.title()
    name_list = name_str.split(' ')
    return name_list[0]

def validate_name(name_dict, name_str):
    if name_str in name_dict:
        return True
    return False

def get_users(row):
    user_list = []
    for i in range(4, len(row)):
        if row[i] == 'x':
            user_list.append(data.columns[i])
    return user_list


#read excel data into data frame
#data = pd.read_excel("adj_exp.xlsx", sheet_name="new_sheet") # for testing within directory
data = pd.read_excel("/Users/nicksharpe/Library/CloudStorage/OneDrive-UniversityofFlorida/ResearchAssistant/Expenses.xlsx", sheet_name="Expenses") # for mac 
#data = pd.read_excel("C:\\Users\\nshar\\OneDrive - University of Florida\\ResearchAssistant\\Expenses.xlsx", sheet_name="Expenses") # for windows

#create dictionary of names from column headers
name_dict = {}
for index, name in enumerate(data.columns[4:]):
    name = parse_string(name)
    name_dict[name] = index #number assigned will represent index in numpy array
    name_dict[index] = name
    
#create adj matrix graph and insert expenses into it
exp_g = Adj_Matrix(len(name_dict) // 2)

for index,row in data.iterrows():
    purchased_by = parse_string(row[2])
    user_list = get_users(row)
    if len(user_list) == 0:
        continue
    split_cost = row[3] / len(user_list)
    for user in user_list:
        user = parse_string(user)
        if user in name_dict:
            exp_g.add_edge(name_dict[purchased_by], name_dict[user], split_cost)
        else:
            print("Error: Name does not match: ", user)

#print out results
pmt_arr = []
for r in range(len(exp_g.matrix)):
    for c in range(len(exp_g.matrix)):
        amount = exp_g.get_weight(c,r) - exp_g.get_weight(r,c)
        if amount > 0:
            pmt_arr.append([name_dict[r], name_dict[c], amount])
for l in sorted(pmt_arr): print(l[0], ' -> ', l[1], ' ', l[2])

