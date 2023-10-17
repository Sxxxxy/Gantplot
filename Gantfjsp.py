import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import datetime as dt

current_time = dt.datetime.now()
current_hour = current_time.hour + 1

# 读取三个CSV文件
df1 = pd.read_csv(r"D:\Codes\VsProject\Heatoperationplanplus\page0.csv",header=None, encoding="GBK")
df2 = pd.read_csv(r"D:\Codes\VsProject\Heatoperationplanplus\page1.csv",header=None, encoding="GBK")
df3 = pd.read_csv(r"D:\Codes\VsProject\Heatoperationplanplus\page2.csv",header=None, encoding="GBK")

# 解析数据
dfs = [df1, df2, df3]
schedules = {}
machines = ['加热炉1', '加热炉2', '加热炉3']
Temperatures = {}
continuous_times = {}
for idx, df in enumerate(dfs):
    machine_data = []
    temp_data = []
    con_Data = []
    for _, row in df.iterrows():
        if row[0] == "repair":
            machine_data.append((row[2], row[3], '检修'))
            temp_data.append((row[2], row[3], 0))
            con_Data.append((row[2], row[3]))
        elif row[0] == "free":
            machine_data.append((0, row[1], '已占用'))
            temp_data.append((0, row[1], 0))
            con_Data.append((0, row[1]))
        else:
            machine_data.append((row[2] + row[4], row[3], row[0]))
            temp_data.append((row[2] + row[4], row[3], row[1]))
            con_Data.append((row[2], row[3]))
            if int(row[4]) != 0 :
                machine_data.append((row[2],row[2] + row[4],'调温'))
    schedules[machines[idx]] = machine_data
    Temperatures[machines[idx]] = temp_data
    continuous_times[machines[idx]] = con_Data
print(schedules)
print(Temperatures)

for machine, temps in Temperatures.items():
    Temperatures[machine] = sorted(temps, key=lambda x: x[0])  # 按时间 (x[0]) 排序

free_time = {}
for machine, temps in continuous_times.items():
    free_time[machine] = []
    for i in range(len(temps) - 1):
        if temps[i+1][0] - temps[i][1] > 5:
            free_time[machine].append((temps[i][1]+1, temps[i + 1][0]-1))

# 计算最大的时间值以确定x轴的上限
max_time = max([end for machine_data in schedules.values() for _, end, _ in machine_data])

# 生成x刻度: 从0到max_time，步长为60
xticks = np.arange(0, max_time + 1, 60)
xticklabels = []  # 存放x轴的标签

for i in range(len(xticks)):
    # 计算"第几天"和"第几个小时"
    day = (i+current_hour) // 24 + 1  # 以0开始，所以加1
    hour = (i % 24 + current_hour) % 24  # 加上当前小时，然后再对24取余
    # 格式化标签
    label = f"Day {day}, Hour {hour}"
    xticklabels.append(label)


# 定义颜色
colors = {
    '淬火': 'blue',
    '回火': 'yellow',
    '正火': 'green',
    '检修': 'grey',
    '已占用': 'red',
    '调温': 'purple'
}


# 创建甘特图
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(150, 12), dpi=150,sharex=True)
# 设置刻度和标签
ax1.set_xticks(xticks)
ax1.set_xticklabels(xticklabels, rotation=45)  # 设置轴标签的旋转角度，使其更易于阅读

ax2.set_xticks(xticks)
ax2.set_xticklabels(xticklabels, rotation=45)


print("========================================plot====================================")

# 为加热炉绘制甘特图
for idx, (machine, tasks) in enumerate(schedules.items()):
    temps = Temperatures[machine]
    for j, (start, end, task) in enumerate(tasks):
        facecolor = colors[task]
        hatch = '///' if task in ['检修', '已占用','调温'] else None
        ax1.broken_barh([(start, end - start)], (idx - 0.4, 0.8), facecolors=facecolor, hatch=hatch, edgecolor='black')
        # ax1.broken_barh([(start / 60, (end - start) / 60)], (idx - 0.4, 0.8), facecolors=facecolor, hatch=hatch,
        #                 edgecolor='black')

        # 在两个图上添加虚线
        # ax1.axvline(x=start, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到甘特图
        # ax2.axvline(x=start, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到温度线图

        # ax1.axvline(x=end, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到甘特图
        # ax2.axvline(x=end, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到温度线图

ax1.set_yticks(range(len(schedules)))
ax1.set_yticklabels(list(schedules.keys()))
ax1.set_xlabel('Minutes')
ax1.set_title('Gantt Chart for Heating Furnaces Scheduling')
handles = [patches.Patch(color=color, label=job, hatch='///' if job in ['检修', '已占用'] else None) for job, color in colors.items()]
ax1.legend(handles=handles, loc='upper left')
ax1.grid(True)
ax1.invert_yaxis()

# 绘制温度线图
# for machine, temps in Temperatures.items():
#     times, times2, temperature_values = zip(*temps)
#     ax2.plot(times, temperature_values, label=machine, marker='o')
#     ax2.plot(times2, temperature_values, label=machine, marker='o')
#
#
#     # 基于温度数据的开始时间点添加虚线
#     for start_time in times:
#         ax1.axvline(x=start_time, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到甘特图
#         ax2.axvline(x=start_time, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到温度线图

times_temp = {}
for machine, temps in Temperatures.items():
    times, times2, temperature_values = zip(*temps)
    if machine not in times_temp:
        times_temp[machine] = []
    for i in range(len(times)):
        times_temp[machine].append((times[i], temperature_values[i]))
        times_temp[machine].append((times2[i], temperature_values[i]))
for machine, temps in free_time.items():
    for i in range(len(temps)):
        times_temp[machine].append((temps[i][0],0))
        times_temp[machine].append((temps[i][1],0))

for machine, time_value_pairs in times_temp.items():
    times_temp[machine] = sorted(time_value_pairs, key=lambda x: x[0])


for machine, temps in times_temp.items():
    times, temperature_values = zip(*temps)

    ax2.plot(times, temperature_values, label=machine, marker='o')

    for start_time in times:
        ax1.axvline(x=start_time, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到甘特图
        ax2.axvline(x=start_time, color='grey', linestyle='--', linewidth=0.5)  # 添加虚线到温度线图








ax2.set_xlabel('Hours')
ax2.set_ylabel('Temperature (°C)')
ax2.set_title('Temperature over Time')
ax2.legend(loc='upper left')
ax2.grid(True)




plt.tight_layout()
plt.show()
