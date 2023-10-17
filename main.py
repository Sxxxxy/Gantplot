import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 读取三个CSV文件
df1 = pd.read_csv(r"D:\Codes\VsProject\Heatoperationplanplus\page0.csv",header=None, encoding="GBK")
df2 = pd.read_csv(r"D:\Codes\VsProject\Heatoperationplanplus\page1.csv",header=None, encoding="GBK")
df3 = pd.read_csv(r"D:\Codes\VsProject\Heatoperationplanplus\page2.csv",header=None, encoding="GBK")

# 解析数据
dfs = [df1, df2, df3]
schedules = {}
machines = ['加热炉1', '加热炉2', '加热炉3']

for idx, df in enumerate(dfs):
    machine_data = []
    for _, row in df.iterrows():
        if row[0] == "repair":
            machine_data.append((row[2], row[3], '检修'))
        elif row[0] == "free":
            machine_data.append((0, row[1], '已占用'))
        else:
            machine_data.append((row[2], row[3], row[0]))
    schedules[machines[idx]] = machine_data
print(schedules)
# 定义颜色
colors = {
    '淬火': 'blue',
    '回火': 'yellow',
    '正火': 'green',
    '检修': 'grey',
    '已占用': 'red'
}


# 创建甘特图
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(figsize=(150, 6), dpi=150)  # 增加了 dpi 参数

for idx, (machine, tasks) in enumerate(schedules.items()):
    for start, end, task in tasks:
        facecolor = colors[task]
        hatch = '///' if task in ['检修', '已占用'] else None
        ax.broken_barh([(start, end-start)], (idx-0.4, 0.8), facecolors=facecolor, hatch=hatch, edgecolor='black')

ax.set_yticks(range(len(schedules)))
ax.set_yticklabels(list(schedules.keys()))
ax.set_xlabel('Minutes')
ax.set_title('Gantt Chart for Heating Furnaces Scheduling')
ax.grid(True)
ax.invert_yaxis()

handles = [patches.Patch(color=color, label=job, hatch='///' if job in ['检修', '已占用'] else None) for job, color in colors.items()]
ax.legend(handles=handles, loc='upper left')

plt.tight_layout()
plt.show()