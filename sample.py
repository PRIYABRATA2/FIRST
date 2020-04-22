import pandas as pd

file1=r'C:\Users\Happy\Downloads\MP_WINS_UOM_UOM.csv'

read_file1=pd.read_csv(file1)

df=read_file1.rename(columns={'SEGMENT1':'ProductID'})

df['Date']='08/04/2020'

df['Date']=pd.to_datetime(df['Date'],format='%d/%m/%Y')

df=df.drop_duplicates(['ProductID','ITEM_TYPE'])

df=df.reset_index(drop=True)

file2=r'C:\Users\Happy\Downloads\MP_WINS_PRD_PRD.csv'

df1=pd.read_csv(file2,encoding='unicode_escape')

df1['PRODUCT']=df1.PRODUCT.astype(str)

df2=pd.merge(left=df,right=df1,left_on='ProductID',right_on='PRODUCT',how='inner')

df2['Index']= range(1,len(df2)+ 1)

df2=df2.drop(columns=['QUINTIQ_CATEGORY'])

df2.columns = df2.columns.str.replace(r'_x$', '')#to remove suffix

#we can also use rename method to remove suffix.
df2= df2.rename(columns={'ITEM_TYPE_y':'ITEM_TYPE'})


df3=df2[['ProductID','Date','Index','ITEM_TYPE','DESCRIPTION']]

#TASK 2 Continuation#

#adding column and values in it using if else values [method-1]
df3['Check']=['TRUE' if x =='RM' else 'FALSE' for x in df3['ITEM_TYPE']]
#adding column and values in it using .loc method [method-2]
# df3['Check']= 'FALSE'
# df3.loc[df3['ITEM_TYPE']=='RM','Check']='TRUE'

#creating Assign column using '-'.
df3['Assign']= df3['Check'] + '-' + df3['ITEM_TYPE'] + '-' + 'SPLIT'

df3['STOCKINGPOINT']=['RAW_MATERIALS' if x=='RM' or 'NS' else 'FROZEN' for x in df3['ITEM_TYPE']]

#subtracting 6 days from Date column value.
df3['Date']=df3['Date'] - pd.to_timedelta(6,unit='d')

#for splitting Assign column value to create 3 separate columns
df3[['Assign1','Assign2','Assign3']]=df3['Assign'].str.split('-',expand=True)

df3.sort_values(['ProductID'])

df3.drop(df3[df3['Check'] == 'FALSE'].index,inplace=True)

#Creating a new dataframe(df4) and assigning df3 to it.
df4=df3
#Appending df3 and df4 to create a new(df5).

df5=df3.append(df4)
#Count of rows in df5 is 565 and count of rows in df3 is 283

writer=pd.ExcelWriter(r'C:\Users\Happy\Downloads\Learning1.xlsx',engine='xlsxwriter')
df3.to_excel(writer,sheet_name='TASK2')
df5.to_excel(writer,sheet_name='Adding')
writer.save()
writer.close()




