import json
from pathlib import Path
path = Path(r'c:\Users\derek\Desktop\ECBD_9A_IDGS_PRACTICAS_230892\Practica04\Practica04.ipynb')
nb = json.loads(path.read_text(encoding='utf-8'))

# Patch table of contents cell
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and cell['source'] and cell['source'][0].strip() == '# Contenido':
        cell['source'] = [
            '# Contenido',
            '',
            '1. [Cargar datos](#cargar-datos)',
            '2. [Explorar a los donantes](#explorando-a-los-donantes)',
            '   1. [Vista general de los donantes](#vista-general-de-los-donantes)',
            '   2. [Estados con mayor proporción de donantes por habitante](#estados-con-mayor-proporcion-de-donantes-por-habitante)',
            '   3. [Visualización de la ubicación de los donantes](#visualizacion-de-la-ubicacion-de-los-donantes)',
            '      - [Donantes de California](#donantes-de-california)',
            '      - [Donantes de Florida](#donantes-de-florida)',
            '      - [Donantes de Texas](#donantes-de-texas)',
            '      - [Donantes de Nueva York](#donantes-de-nueva-york)',
            '   4. [Visualización de todos los donantes](#visualizacion-de-todos-los-donantes)',
            '   5. [Número de donantes docentes y no docentes de cada estado](#numero-de-donantes-docentes-y-no-docentes-por-estado)',
            '3. [Exploración de donaciones](#exploracion-de-donaciones)',
            '   1. [Proyectos destacados](#proyectos-destacados)',
            '   2. [Principales donantes](#principales-donantes)',
            '   3. [Análisis de fechas de donación](#analisis-de-fechas-de-donacion)'
        ]
        break

# Anchor mapping
anchors = {
    '## 1. Cargar datos': ['<a id="cargar-datos"></a>', '## 1. Cargar datos'],
    '## 2. Explorar a los donantes': ['<a id="explorando-a-los-donantes"></a>', '## 2. Explorar a los donantes'],
    '### 2.1 Vista general de los donantes': ['<a id="vista-general-de-los-donantes"></a>', '### 2.1 Vista general de los donantes'],
    '### 2.3 Estados con mayor proporción de donantes por habitante': ['<a id="estados-con-mayor-proporcion-de-donantes-por-habitante"></a>', '### 2.3 Estados con mayor proporción de donantes por habitante'],
    '### 2.4 Visualización de la ubicación de los donantes': ['<a id="visualizacion-de-la-ubicacion-de-los-donantes"></a>', '### 2.4 Visualización de la ubicación de los donantes'],
    '#### 2.4.1 Donantes ubicados en California': ['<a id="donantes-de-california"></a>', '#### 2.4.1 Donantes ubicados en California'],
    '#### 2.4.2 Donantes ubicados en Florida': ['<a id="donantes-de-florida"></a>', '#### 2.4.2 Donantes ubicados en Florida'],
    '#### 2.4.3 Donantes ubicados en Nueva York': ['<a id="donantes-de-nueva-york"></a>', '#### 2.4.3 Donantes ubicados en Nueva York'],
    '### 2.5 Visualización general de la ubicación de los donantes': ['<a id="visualizacion-de-todos-los-donantes"></a>', '### 2.5 Visualización general de la ubicación de los donantes'],
    '2.6 Número de donantes docentes y no docentes de cada estado': ['<a id="numero-de-donantes-docentes-y-no-docentes-por-estado"></a>', '### 2.6 Número de donantes docentes y no docentes de cada estado'],
    '3. Exploración de donaciones': ['<a id="exploracion-de-donaciones"></a>', '3. Exploración de donaciones'],
    '3.3 ¿Quiénes son los principales donantes?': ['<a id="principales-donantes"></a>', '3.3 ¿Quiénes son los principales donantes?'],
    'Donaciones anuales': ['<a id="analisis-de-fechas-de-donacion"></a>', 'Donaciones anuales']
}

for cell in nb['cells']:
    if cell['cell_type'] != 'markdown':
        continue
    joined = '\n'.join(cell['source']).strip()
    for key, value in anchors.items():
        if joined == key:
            cell['source'] = [value[0], value[1]]
            break

# Fix Texas/New York section
texas_heading_index = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and '#### 2.4.3 Donantes ubicados en Nueva York' in '\n'.join(cell['source']):
        texas_heading_index = i
        cell['source'] = ['<a id="donantes-de-texas"></a>', '#### 2.4.3 Donantes ubicados en Texas']
        break

if texas_heading_index is not None:
    code_index = texas_heading_index + 1
    if code_index < len(nb['cells']) and nb['cells'][code_index]['cell_type'] == 'code':
        nb['cells'][code_index]['source'] = [
            'import os, glob',
            '',
            'def find_zip_path(base_path):',
            '    candidates = [',
            '        os.path.join(base_path, "zip_codes_states.csv"),',
            '        os.path.join(base_path, "..", "zip_codes_states.csv"),',
            '        os.path.join(os.getcwd(), "zip_codes_states.csv"),',
            '        os.path.join(os.getcwd(), "..", "zip_codes_states.csv")',
            '    ]',
            '    for p in candidates:',
            '        p = os.path.normpath(p)',
            '        if os.path.exists(p):',
            '            return p',
            '    matches = glob.glob(os.path.join(base_path, "**", "zip_codes_states.csv"), recursive=True)',
            '    matches += glob.glob(os.path.join("..", "**", "zip_codes_states.csv"), recursive=True)',
            '    return matches[0] if matches else None',
            '',
            'zip_path = find_zip_path(base_path)',
            'if zip_path is None:',
            '    raise FileNotFoundError("zip_codes_states.csv no se encontró. Verifique la ruta.")',
            '',
            'c = pd.read_csv(zip_path)',
            'c = c.dropna(subset=["city", "state"])',
            'c["city_norm"] = c["city"].astype(str).str.title().str.strip()',
            't = donors_df[donors_df["Donor State"] == "Texas"]["Donor City"].astype(str).str.title().str.strip().value_counts()',
            'fldf = c[c["state"] == "TX"][['city_norm', 'latitude', 'longitude']].drop_duplicates()',
            'texas = t.reset_index().rename(columns={"index": "city_norm", "Donor City": "count"}).merge(fldf, on="city_norm", how="left").dropna()',
            'map_osm2 = folium.Map([31.884540, -97.077218], zoom_start=6.2, tiles="cartodbdark_matter")',
            'ziparr = []',
            'for i, row in texas.iterrows():',
            '    ziparr.append([row["latitude"], row["longitude"], row["count"]])',
            'map_osm2.add_child(plugins.HeatMap(ziparr, radius=12))',
            'map_osm2'
        ]

        # Insert New York heading/code after Texas code block
        new_york_heading = {
            'cell_type': 'markdown',
            'id': '#VSC-newyork',
            'metadata': {'language': 'markdown'},
            'source': ['<a id="donantes-de-nueva-york"></a>', '#### 2.4.4 Donantes ubicados en Nueva York']
        }
        new_york_code = {
            'cell_type': 'code',
            'id': '#VSC-newyorkcode',
            'metadata': {'language': 'python'},
            'source': [
                't = donors_df[donors_df["Donor State"] == "New York"]["Donor City"].astype(str).str.title().str.strip().value_counts()',
                'fldf = c[c["state"] == "NY"][['city_norm', 'latitude', 'longitude']].drop_duplicates()',
                'ny = t.reset_index().rename(columns={"index": "city_norm", "Donor City": "count"}).merge(fldf, on="city_norm", how="left").dropna()',
                'map_osm2 = folium.Map([40.7128, -74.0060], zoom_start=6, tiles="cartodbdark_matter")',
                'ziparr = []',
                'for i, row in ny.iterrows():',
                '    ziparr.append([row["latitude"], row["longitude"], row["count"]])',
                'map_osm2.add_child(plugins.HeatMap(ziparr, radius=12))',
                'map_osm2'
            ]
        }
        nb['cells'].insert(code_index + 1, new_york_heading)
        nb['cells'].insert(code_index + 2, new_york_code)

# Patch general donor map code at the 2.5 section
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and cell['source'] and cell['source'][0].strip().startswith('fldf = c[['):
        cell['source'] = [
            'c["city_norm"] = c["city"].astype(str).str.title().str.strip()',
            'fldf = c[["city_norm", "latitude", "longitude"]].drop_duplicates()',
            't = donors_df["Donor City"].astype(str).str.title().str.strip().value_counts()',
            'fldons = pd.DataFrame({"city_norm": t.index, "count": t.values})',
            'florida = fldons.merge(fldf, on="city_norm", how="left").dropna()',
            'map_osm2 = folium.Map([39.3714557, -94.3541242], zoom_start=3.5, tiles="cartodbdark_matter")',
            'ziparr = []',
            'for i, row in florida.iterrows():',
            '    ziparr.append([row["latitude"], row["longitude"], row["count"]])',
            'map_osm2.add_child(plugins.HeatMap(ziparr, radius=10))',
            'map_osm2'
        ]
        break

# Patch 2.6 heading
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and cell['source'] and '2.6 Número de donantes docentes y no docentes de cada estado' in cell['source'][0]:
        cell['source'] = ['<a id="numero-de-donantes-docentes-y-no-docentes-por-estado"></a>', '### 2.6 Número de donantes docentes y no docentes de cada estado']
        break

# Ensure the new heading anchor exists in TOC if not already

path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('patched notebook')
