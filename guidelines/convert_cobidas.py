import pandas
import re
from pathlib import Path

guidelines_file = Path(__file__).parent / 'sources/COBIDAS_AppendixD_clean_OSF.xlsx'
df = pandas.read_excel(guidelines_file, skiprows=[r for r in range(13)])
table_df = df[[
    'Reference',
    'Table.1',
    'Aspect1',
    'Aspect2',
    'Aspect3',
    'Aspect4',
    'Detail to specify if used/applicable',
]]

# convert table to a YAML structure
table_dict = table_df.to_dict(orient='records')

output_dict = {'guidelines': []}

re_replacements = {
    r' \u00ad': '-',
    r'\u00ad ': '-',
    r'\u00ad': '-',
    r'\u00d7': 'x',
    r'\u037e': ';',
    r' \u2013': '-',
    r'\u2013 ': '-',
    r'\u2013': '-',
    r' \u2014': '-',
    r'\u2014 ': '-',
    r'\u2014': '-',
    r'\u2018': '\'',
    r'\u2019': '\'',
    r'\u201c': '\\"',
    r'\u201d': '\\"',
    r' \u2212': '-',
    r'\u2212 ': '-',
    r'\u2212': '-',
}

for row in table_dict:
    # replace characters
    row['Detail to specify if used/applicable'] = row['Detail to specify if used/applicable'].replace('"', '\\"')
    for pattern, replacement in re_replacements.items():
        row['Detail to specify if used/applicable'] = re.sub(pattern, replacement, row['Detail to specify if used/applicable'])
    row['Detail to specify if used/applicable'] = row['Detail to specify if used/applicable'].replace('--', '-')
    row['Detail to specify if used/applicable'] = row['Detail to specify if used/applicable'].replace(' -', '-')

    info_list = [ row['Table.1'] , row['Aspect1'] ]

    if not pandas.isna(row['Aspect2']):
        info_list.append(row['Aspect2'])
    if not pandas.isna(row['Aspect3']):
        info_list.append(row['Aspect3'])
    if not pandas.isna(row['Aspect4']):
        info_list.append(row['Aspect4'])

    info = ' | '.join(info_list)
    for pattern, replacement in re_replacements.items():
        info = re.sub(pattern, replacement, info)

    temp_dict = {}
    temp_dict['index'] = row['Reference']
    temp_dict['info'] = info
    temp_dict['text'] = '"' + row['Detail to specify if used/applicable'] + '"'

    output_dict['guidelines'].append(temp_dict)

# write to YAML file
output_file = Path(__file__).parent / 'cobidas.yaml'
with open(output_file, 'w') as f:
    f.write('guidelines:\n')
    for guideline in output_dict['guidelines']:
        f.write(f"  {guideline['index']}:\n")
        f.write(f"      info: {guideline['info']}\n")
        f.write(f"      text: {guideline['text']}\n")

print(f"Converted COBIDAS guidelines to: {output_file}")
