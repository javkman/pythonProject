import pandas as pd
import json
import numpy as np
from sqlalchemy import create_engine
from pyecharts import options as opts
from pyecharts.charts import Sankey
# 初始化数据库连接，使用pymysql模块
# MySQL的用户：root, 密码:147369, 端口：3306,数据库：test
engine = create_engine('mysql+pymysql://root:root@localhost:3306/data')
# 查询语句，选出employee表中的所有数据
sql = 'select * from sheet0;'
# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)
# 输出employee表的查询结果
# print(df)
# column_list = list(df.columns)
# df1 = np.array(df)
# for row in df1:
#     lst = []
#     lst.append(dict(zip(column_list, list(row))))
#     str1 = json.dumps(lst, ensure_ascii=False)
#     print(str1)

df1 = df.groupby(['主叫号码','被叫号码'], as_index=False).sum()
# df2 = df.groupby(['主叫号码','被叫号码'], as_index=False).len()
# df1.set_index('主叫号码')
# print(type(df1))
# print(df2)
#
# print(df1.shape[1])
nodes=[]

# for i in range(df1.shape[1]-1):#python里面的for函数范围。rangge（2）是0，1.unique()
vales = np.hstack((df1.iloc[:,0].unique(),df1.iloc[:,1].unique()))
print(vales)

for value in vales:
    dic={}
    dic['name']=value
    nodes.append(dic)
# print(nodes)


linkes=[]
for i in df1.values:
    dic={}
    dic['source']=i[0]
    dic['target']=i[1]
    dic['value']=i[2]
    linkes.append(dic)

# print(linkes)
c = (
    Sankey()
    .add(
        "sankey",
        nodes=nodes,
        links=linkes,
        pos_top="10%",
        focus_node_adjacency=True,
        levels=[
            opts.SankeyLevelsOpts(
                depth=0,
                itemstyle_opts=opts.ItemStyleOpts(color="#fbb4ae"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=1,
                itemstyle_opts=opts.ItemStyleOpts(color="#b3cde3"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=2,
                itemstyle_opts=opts.ItemStyleOpts(color="#ccebc5"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=3,
                itemstyle_opts=opts.ItemStyleOpts(color="#decbe4"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
        ],
        linestyle_opt=opts.LineStyleOpts(curve=0.5),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Sankey-Level Settings"),
        tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove"),
    )
    .render("数据分析图.html")
)