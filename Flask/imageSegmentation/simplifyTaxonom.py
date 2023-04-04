import json
import pandas as pd

with open('taxonomy.json', 'r') as f:
    data = json.load(f)

colormap = data['srgb_colormap']
names = data['names']
shortnames = data['shortnames']

lookup_table = pd.DataFrame({'Color': colormap, 'Name': names, 'Short Name': shortnames})
print(lookup_table)
lookup_table_dict = lookup_table.to_dict(orient='records')
output_json = {'lookup_table': lookup_table_dict}

with open('output_lookup_table.json', 'w') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)


