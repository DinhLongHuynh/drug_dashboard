import time
from tqdm import tqdm
import pandas as pd
import pubchempy as pcp

def ingredients_cleaner(ingredietns):
    # For patterns like TRIPLE SULFA (SULFABENZAMIDE;SULFACETAMIDE;SULFATHIAZOLE)
    if '(' in ingredietns and ')' in ingredietns:
        inside = ingredietns[ingredietns.find('(')+1:ingredietns.find(')')]
        return [item.strip() for item in inside.split(';')]
    
    # For patterns like AMPHETAMINE ASPARTATE; AMPHETAMINE SULFATE; DEXTROAMPHETAMINE SACCHARATE'
    else:
        return [item.strip() for item in ingredietns.split(';')]


def smile_generator(data_path="../data_csv",data_file='Products.csv'):
    df = pd.read_csv("/".join([data_path,data_file]))
    df['ProductID'] = df.index
    df = df[df['ReferenceDrug']==1]
    ActiveIngredient_list = df['ActiveIngredient'].tolist()
    ProdcutID_list = df['ProductID'].tolist()

    results = {'ProductID': [], 'smiles': []}

    # Loops through products
    for index, ingredients in tqdm(list(zip(ProdcutID_list, ActiveIngredient_list)), total=len(ActiveIngredient_list), desc="Fetching SMILES"):
        start = time.time()
        ingredients = ingredients_cleaner(ingredients)
        
        # Loops through many active ingredients in 1 product
        for name in ingredients:
            compounds = pcp.get_compounds(name, 'name')
            duration = time.time() - start

            if compounds:
                results['smiles'].append(compounds[0].isomeric_smiles)
                results['ProductID'].append(index)

            else:
                tqdm.write(f"{index}: {name} -> Not found (took {duration:.2f}s)")

    df_smile = pd.DataFrame(results)
    df_smile.to_csv("/".join([data_path,'Smiles.csv']), index=False)
