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
sql = 'select * from test1;'#123为数据库data里面的表名
# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)
# 输出employee表的查询结果
# print(df)
# column_list = list(df.columns)
# df1 = np.array(df)

#-------------话单用下面的代码------------------------
# df1 = df.groupby(['主叫号码','被叫号码'], as_index=False).sum().sort_values("通话时长",ascending=False) #分组求和按通话时长降序排列
#-------------资金分析用下面的代码--------------------
df1 = df.groupby(['交易卡号','交易对手账卡号'], as_index=False).sum().sort_values("交易金额",ascending=False) #分组求和
# print(df1)
vales=df1.iloc[:,0].append(df1.iloc[0:50,1]).unique()#拼接两列唯一值并去重复，df1.iloc[0:10,1]控制对方前多少名数据

nodes=[]
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
        "数据分析图",
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
        linestyle_opt=opts.LineStyleOpts(curve=0.8),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove"),
    )
    .render("数据分析图.html")
)