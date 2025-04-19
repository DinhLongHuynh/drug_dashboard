import time
from tqdm import tqdm
import pandas as pd
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Descriptors

class DataProcessor():
    def __init__(self, data_path="../data_csv", data_file = 'Products.csv'):
        self.data_path = data_path
        self.data_file = data_file
        self.df = pd.read_csv("/".join([self.data_path,self.data_file]))


    def ingredients_cleaner(self, ingredietns):
        # For patterns like TRIPLE SULFA (SULFABENZAMIDE;SULFACETAMIDE;SULFATHIAZOLE)
        if '(' in ingredietns and ')' in ingredietns:
            inside = ingredietns[ingredietns.find('(')+1:ingredietns.find(')')]
            return [item.strip() for item in inside.split(';')]
        
        # For patterns like AMPHETAMINE ASPARTATE; AMPHETAMINE SULFATE; DEXTROAMPHETAMINE SACCHARATE'
        else:
            return [item.strip() for item in ingredietns.split(';')]


    def smile_generator(self):
        self.df['ProductID'] = self.df.index
        self.df = self.df[self.df['ReferenceDrug']==1]
        ActiveIngredient_list = self.df['ActiveIngredient'].tolist()
        ProdcutID_list = self.df['ProductID'].tolist()

        results = {'ProductID': [], 'smiles': []}

        # Loops through products
        for index, ingredients in tqdm(list(zip(ProdcutID_list, ActiveIngredient_list)), total=len(ActiveIngredient_list), desc="Fetching SMILES"):
            start = time.time()
            ingredients = self.ingredients_cleaner(ingredients)
            
            # Loops through many active ingredients in 1 product
            for name in ingredients:
                compounds = pcp.get_compounds(name, 'name')
                duration = time.time() - start

                if compounds:
                    results['smiles'].append(compounds[0].isomeric_smiles)
                    results['ProductID'].append(index)

                else:
                    tqdm.write(f"{index}: {name} -> Not found (took {duration:.2f}s)")

        self.df_smile = pd.DataFrame(results)
    
    def standardize_smiles(self, smiles,desalt,remove_stereo):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        try:
            if desalt:
                frags = Chem.GetMolFrags(mol, asMols=True)
                mol = max(frags, key=lambda m: m.GetNumAtoms())
            if remove_stereo:
                Chem.RemoveStereochemistry(mol)
            
            Chem.SanitizeMol(mol)
            return Chem.MolToSmiles(mol, canonical=True)
        
        except Exception as e:
            print(f"Error in standardizing {smiles}: {str(e)}")
            return mol 
        

    def smile_standardizer(self,smile_columns = 'smiles',desalt=True,remove_stereo=True):
        tqdm.pandas()
        self.df_smile['standardized_smiles'] = self.df_smile[smile_columns].progress_apply(lambda smiles: self.standardize_smiles(smiles,desalt=desalt,remove_stereo=remove_stereo))



    def get_properties(self):
        self.df_smile['mol'] = self.df_smile['smiles'].apply(Chem.MolFromSmiles)
        self.df_smile['MolWt'] = self.df_smile['mol'].apply(Descriptors.MolWt)
        self.df_smile['LogP'] = self.df_smile['mol'].apply(Descriptors.MolLogP)
        self.df_smile['NumHDonors'] = self.df_smile['mol'].apply(Descriptors.NumHDonors)
        self.df_smile['NumHAcceptors'] = self.df_smile['mol'].apply(Descriptors.NumHAcceptors)
        self.df_smile['TPSA'] = self.df_smile['mol'].apply(Descriptors.TPSA)
        self.df_smile['NumRotatableBonds'] = self.df_smile['mol'].apply(Descriptors.NumRotatableBonds)
        self.df_smile['RingCount'] = self.df_smile['mol'].apply(Descriptors.RingCount)
        self.df_smile['HeavyAtomCount'] = self.df_smile['mol'].apply(Descriptors.HeavyAtomCount)
        self.df_smile['FractionCSP3'] = self.df_smile['mol'].apply(Descriptors.FractionCSP3)
        self.df_smile['FormalCharge'] = self.df_smile['mol'].apply(Chem.GetFormalCharge)

    def get_fingerpirnt(self):
        pass
    def dimension_reduction(self):
        pass

    def export(self, file_name = 'data_processed.csv'):
        file_path = "/".join([self.data_path,file_name])
        self.df_smile.to_csv(file_path)
        
