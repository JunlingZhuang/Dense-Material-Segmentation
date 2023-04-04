import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 读取 JSON 文件
with open('taxonomy.json', 'r') as f:
    data = json.load(f)

# 获取颜色列表和标签
colors = data['srgb_colormap']
labels = data['names']



# # 绘制色卡
# fig, ax = plt.subplots(figsize=(12, 1))
# ax.imshow([colors], aspect='auto')

# # 设置标签
# ax.set_xticks(range(len(labels)))
# ax.set_xticklabels(labels, rotation=90, fontsize=8)
# ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)


# 绘制色卡
fig, ax = plt.subplots(figsize=(12, 12))
ax.imshow([colors,], aspect='auto')

# 设置标签
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=90, fontsize=8)
ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)


# 显示色卡
plt.show()
