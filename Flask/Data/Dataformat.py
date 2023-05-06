import csv
import json

csvFilePath = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/Data/Columbia_SVIpoints_4326_copy_output.csv'
jsonFilePath = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/Data/Columbia_SVIpoints_4326_copy_output.json'

# 读取CSV文件并将其解析为Python中的列表或字典
with open(csvFilePath, 'r') as csvFile:
    csvData = csv.DictReader(csvFile)
    jsonData = list(csvData)

# 将Python中的列表或字典转换为JSON格式
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(jsonData, indent=4))
