import pandas as pd
import sys
from glob import glob
import os
import seaborn as sns
import matplotlib.pyplot as plt


def main(argv):
    ########  usage specifications  ########
    if (len(sys.argv) != 2):
        sys.exit("Usage: python script.py <filename>")

    ########  setting the right directories and paths ########
    directory = os.path.dirname(os.path.realpath(__file__))
    filename = sys.argv[1]
    path = os.path.join(directory, filename)

    ########  reading the csv file ########
    df = pd.read_csv(path, encoding = 'utf-16', sep='\n', header=None)
    df = df[0].str.split('\t', expand=True)

    ########  setting headers ########
    headers = df.iloc[0]
    df = df[1:]
    df.columns = headers

    ########  cleaning surgeon name data #########
    for i in df.index:
        name = df.loc[i, 'Surgeon']
        cleanedName = name[:len(name) - 1]
        df.loc[i, 'Surgeon'] = cleanedName
    ########  converting ages from strings to floats  ########
        age = df.loc[i, 'Age']
        age_float = float(age)
        df.loc[i, 'Age'] = age_float
    ########  crm to region cleaning ########
    df = replaceCRM(df)
    
    ########  calling graph functions ########
    regionList = []
    for i in df.index:
        region = df.loc[i, 'CRM']
        if region not in regionList:
            regionList.append(region)
    
    for region in regionList:
        dfRegion = df.loc[df['CRM'] == region].copy().reset_index()
        surgeriesByAge(dfRegion, region, '2020', 'Country')
    
    """
    primaryLipNoseUnilateralTypes(df, 'Africa', '2020')
    primaryLipNoseBilateralTypes(df, 'Africa', '2020')
    lipNoseRevisionTypes(df, 'Africa', '2020')
    """





def surgeriesByAge(df, location, year, hueCat):
    for i in df.index:
        if df.loc[i, 'Operations'].__contains__('+'):
            selectRow = df.iloc[[i]]
            operations = df.loc[i, 'Operations'].split('+')

            for j in range(len(operations)):
                copy = selectRow.copy()
                copy.loc[i, 'Operations'] = operations[j].strip()
                df.append(copy, ignore_index=True)
            df.drop(i, inplace=True)
        df.reset_index()
    sns.set()
    ax = sns.catplot(
        data = df,
        x = 'Operations',
        y = 'Age',
        hue = hueCat,
        jitter = 1,
        aspect = 3
    )
    title = 'Surgeries by Age in ' + location + year
    ax.set(title=title)
    plt.show()

def primaryLipNoseUnilateralTypes(df, location, year):

    ########  isolating the relevant columns  ########
    df = df.loc[:, 'Rotation/Advancement and Variants (Millard)' : 'Quadrilateral Flap Variant (Le Mesurier)']

    millard = df.loc[df['Rotation/Advancement and Variants (Millard)'] == '1']
    millardCount = millard.shape[0]

    straightLine = df.loc[df['Straight Line Repair'] == '1']
    straightLineCount = straightLine.shape[0]

    fisher = df.loc[df['Fisher'] == '1']
    fisherCount = fisher.shape[0]

    roseThompson = df.loc[df['Rose Thompson (Oxford Modification)'] == '1']
    roseThompsonCount = roseThompson.shape[0]

    triangular = df.loc[df['Triangular Variant'] == '1']
    triangularCount = triangular.shape[0]

    quadrilateral = df.loc[df['Quadrilateral Flap Variant (Le Mesurier)'] == '1']
    quadrilateralCount = quadrilateral.shape[0]

    data = {'Millard': [millardCount], 'Straight Line': [straightLineCount],
            'Fisher': [fisherCount], 'Rose Thompson': [roseThompsonCount],
            'Triangular': [triangularCount], 'Quadrilateral': [quadrilateralCount]}
    pln = pd.DataFrame(data, columns = ['Millard', 'Straight Line', 'Fisher',
                       'Rose Thompson', 'Triangular', 'Quadrilateral'])

    ax = sns.catplot(
        kind='bar',
        data=pln,
        aspect=2
    )

    title = 'Primary Lip Nose Unilateral by Techinique ' + location + ' ' + year
    ax.set(title=title, xlabel='Technique', ylabel='Count')
    plt.show()

def primaryLipNoseBilateralTypes(df, location, year):
    ########  isolating the relevant columns  ########
    df = df.loc[:, 'Quadrilateral Flap Variant (Le Mesurier)' : 'Two-stage Repair']
    df = df.loc[:, 'Straight Line Repair' : ]

    straightLine = df.loc[df['Straight Line Repair'] == '1']
    straightLineCount = straightLine.shape[0]

    millard = df.loc[df['Millard Type Variant (Forked Flap)'] == '1']
    millardCount = millard.shape[0]

    roseThompson = df.loc[df['Rose Thompson (Veau III)'] == '1']
    roseThompsonCount = roseThompson.shape[0]

    mulliken = df.loc[df['Mulliken Type Variant'] == '1']
    mullikenCount = mulliken.shape[0]

    twoStage = df.loc[df['Two-stage Repair'] == '1']
    twoStageCount = twoStage.shape[0]

    data = {'Straight Line': [straightLineCount], 'Millard': [millardCount],
            'Rose Thompson': [roseThompsonCount], 'Mulliken': [mullikenCount],
            'Two Stage': twoStageCount}
    pln = pd.DataFrame(data, columns = ['Straight Line', 'Millard',
                       'Rose Thompson', 'Mulliken', 'Two Stage'])

    ax = sns.catplot(
        kind='bar',
        data=pln,
        aspect=2
    )
    title = 'Primary Lip Nose Bilateral by Techinique ' + location + ' ' + year
    ax.set(title=title, xlabel='Technique', ylabel='Count')
    plt.show()

def lipNoseRevisionTypes(df, location, year):
    df = df.loc[:, 'Primary' : 'Late Repair']

    primary = df.loc[df['Primary'] == '1']
    primaryCount = primary.shape[0]

    open = df.loc[df['Open'] == '1']
    openCount = open.shape[0]

    closed = df.loc[df['Closed'] == '1']
    closedCount = closed.shape[0]

    lateRepair = df.loc[df['Late Repair'] == '1']
    lateRepairCount = lateRepair.shape[0]

    data = {'Primary': [primaryCount], 'Open': [openCount],
            'Closed': [closedCount], 'Late Repair': [lateRepairCount]}
    lnr = pd.DataFrame(data, columns = ['Primary', 'Open',
                       'Closed', 'Late Repair'])
    ax = sns.catplot(
        data=lnr,
        kind='bar',
        aspect=2
    )
    plt.show()

def replaceCRM(df):
    directory = '/Users/elaine01px2019/Documents/GitHub/STX_stats_sample/crm'
    crmFileName = glob(os.path.join(directory, '*.xlsx'))
    
    crmdf = pd.read_excel(crmFileName[0])
    crmdf = crmdf.loc[:, 'Name' : 'Title']
    
    crmDictionary = {}
    for i in crmdf.index:
        titleArray = crmdf.loc[i, 'Title'].split(', ')
        lastName = crmdf.loc[i, 'Name'].split()[-1]
        crmdf.loc[i, 'Title'] = titleArray[-1].strip()
        crmDictionary.update({lastName: crmdf.loc[i, 'Title']})

    for i in df.index:
        crmName = df.loc[i, 'CRM'].split()[-1]
        region = crmDictionary.get(crmName)
        df.loc[i, 'CRM'] = region
    return df




if __name__ == "__main__":
   main(sys.argv)