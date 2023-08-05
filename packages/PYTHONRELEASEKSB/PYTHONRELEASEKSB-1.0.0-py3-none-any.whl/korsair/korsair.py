import requests
import pandas as pd
import json
import urllib


CONST_SHOWNUM = 7 # 한 번에 출력할 data숫자.
CONST_MAX_COLUMNS = 20 # 최대 columns 개수
CONST_MAX_ROWS = 10000 # 최대 rows 개수
CONST_MAX_WIDTH = 1000 # 한 줄에 출력 가능한 최대 데이터 크기
CONST_URL = 'http://korsair.kisti.re.kr/api/'


def get_vaiant(chro, pos, ref, alt):
    queryString = urllib.parse.urlencode({
            'chr' : chro,
            'pos' : pos,
            'ref' : ref,
            'alt' : alt
        })
    requestUrl = CONST_URL + "variant/?" + queryString
    response = requests.get(requestUrl)
    data = response.json()

    pd.set_option('display.max_columns', CONST_MAX_COLUMNS)
    pd.set_option('display.width', CONST_MAX_WIDTH)

    df = pd.DataFrame.from_dict(data, orient='columns')
    print(df)
    
    return df


def get_variant_id(rsid):
    requestUrl = 'http://korsair.kisti.re.kr/api/variant/' + rsid
    response = requests.get(requestUrl)
    data = response.json()

    pd.set_option('display.max_columns', CONST_MAX_COLUMNS)
    pd.set_option('display.width', CONST_MAX_WIDTH)

    df = pd.DataFrame.from_dict(data, orient='columns')
    print(df)
    
    return df


def get_gene_v1(gene_id):
    requestUrl = 'http://korsair.kisti.re.kr/api/gene/' + gene_id
    response = requests.get(requestUrl)
    data = response.json()

    print(data)

    pd.set_option('display.max_columns', CONST_MAX_COLUMNS)
    pd.set_option('display.max_rows',CONST_MAX_ROWS)
    pd.set_option('display.width', CONST_MAX_WIDTH) 
    # pd.set_option('display.max_colwidth', None) # 셀 안의 데이터 생략 방지. 단,정렬이 안됨

    df = pd.DataFrame.from_dict(data, orient='columns')

    count = 0
    rowLength = len(df)
    
    for i in range(count, rowLength, CONST_SHOWNUM):
        currentRange = count + CONST_SHOWNUM
        if(currentRange < rowLength):
            print(df.loc[count: (currentRange-1),:]) # 남아있는 출력 데이터가 CONST_SHOWNUM보다 많을 때
        else:
            print(df.loc[count: rowLength,:]) # 남아있는 출력 데이터가 CONST_SHOWNUM보다 적을 때
        count = currentRange
        print('\n')
    return df


def get_gene_v2(gene_id):
    requestUrl = 'http://korsair.kisti.re.kr/api/gene/' + gene_id
    response = requests.get(requestUrl)
    data = response.json()

    pd.set_option('display.max_columns', CONST_MAX_COLUMNS)
    pd.set_option('display.max_rows',CONST_MAX_ROWS)
    pd.set_option('display.width', CONST_MAX_WIDTH)
    # pd.set_option('display.max_colwidth', None) # 셀 안의 데이터 생략 방지. 단,정렬이 안됨

    df = pd.DataFrame.from_dict(data, orient='columns')

    print(df)

    return df


def get_region_v1(chro, start, end):
    queryString = urllib.parse.urlencode({
            'chr' : chro,
            'start' : start,
            'end' : end
        })
    requestUrl = CONST_URL + "region/?" + queryString
    response = requests.get(requestUrl)
    data = response.json()

    pd.set_option('display.max_columns', CONST_MAX_COLUMNS)
    pd.set_option('display.max_rows',CONST_MAX_ROWS)
    pd.set_option('display.width', CONST_MAX_WIDTH) 
    # pd.set_option('display.max_colwidth', None) # 셀 안의 데이터 생략 방지. 단,정렬이 안됨

    df = pd.DataFrame.from_dict(data, orient='columns')

    count = 0
    rowLength = len(df)
    
    for i in range(count, rowLength, CONST_SHOWNUM):
        currentRange = count + CONST_SHOWNUM
        if(currentRange < rowLength):
            print(df.loc[count: (currentRange-1),:]) # 남아있는 출력 데이터가 CONST_SHOWNUM보다 많을 때
        else:
            print(df.loc[count: rowLength,:]) # 남아있는 출력 데이터가 CONST_SHOWNUM보다 적을 때
        count = currentRange
        print("\n")

    return df
    

def get_region_v2(chro, start, end):
    queryString = urllib.parse.urlencode({
            'chr' : chro,
            'start' : start,
            'end' : end
        })
    requestUrl = CONST_URL + "region/?" + queryString
    response = requests.get(requestUrl)
    data = response.json()

    pd.set_option('display.max_columns', CONST_MAX_COLUMNS)
    pd.set_option('display.max_rows',CONST_MAX_ROWS)
    pd.set_option('display.width', CONST_MAX_WIDTH)

    df = pd.DataFrame.from_dict(data, orient='columns')
    print(df)
    
    return df


# get_vaiant('chr7', 140787574, 'C', 'T')
# get_variant_id('rs397507456')
# get_gene_v1('CHD8')
# get_gene_v2('CHD8')
# get_region_v1(17, 7676272, 7675994)
# get_region_v2(17, 7676272, 7675994)
