
# from WindPy import w
import pandas as pd
import numpy as np


rf = 0.03
rp = [1,2,3,4,5,1,2,3,4,5,6,7]

# 测算夏普比率
def sharp_ratio(rp,rf):
    
    rp_new = np.array(rp)
    sharp_ratio = (np.mean(rp)-rf)/np.std(rp_new)
    return sharp_ratio


# 计算最大回撤，传入收益率列表
def biggest_withdraw(capital_list):
    jizhi_list = []

    for i in range(1,len(capital_list)-1):
        if capital_list[i-1]<capital_list[i] and capital_list[i+1]<capital_list[i]:
            jizhi_list.append([i,capital_list[i],'high'])
        elif capital_list[i-1]>capital_list[i] and capital_list[i+1]>capital_list[i]:
            jizhi_list.append([i,capital_list[i],'low'])
    if capital_list[-2]<capital_list[-1]:
        jizhi_list.append([len(capital_list),capital_list[-1],'high'])
    else:
        jizhi_list.append([len(capital_list),capital_list[-1],'low'])
   
    # print(jizhi_list)
    # 在极值列表中，对每一个极小值求取回撤并得到相关列表
    withdraw = []
    jidazhi_only = []
    for i in range(len(jizhi_list)):
        if jizhi_list[i][2] == 'high':
            jidazhi_only.append(jizhi_list[i][1])
        elif jizhi_list[i][2] == 'low':
            pct = jizhi_list[i][1]/max(jidazhi_only)
            withdraw.append([jizhi_list[i][0],pct])
    # print(withdraw)
    # 将回撤列表转为dataframe
    # withdraw_df = pd.DataFrame(withdraw, columns = ['index','withdraw'])
    
    # return()
    bd_index = 0
    bgwd = 1
    for i in withdraw:
        if i[1]<bgwd:
            bgwd = i[1]
            bd_index = i
    # return bd_index,1-bgwd
    return bd_index[0],1-bgwd

# 测算IC系数




# 测算信息比率




if __name__ == '__main__':
    print('hello, world')
    sharp_ratio = sharp_ratio(rp, rf)
    print(sharp_ratio)
    print(biggest_withdraw(rp))
 
