import os
import pandas as pd
from src.load_dataset import load_datasets

def school_class(school_name: str):
    cl_school = ['유치원', '초등학교', '중학교', '고등학교']
    
    return next((level 
                 for level in cl_school 
                 if level in school_name), '각종학교')

def region_school_cnt(state: str,
                      region: str,
                      tar_col: str,
                      df:pd.DataFrame) -> pd.DataFrame:
    
    g_df =  df.groupby(tar_col)[tar_col].count()
    
    return pd.DataFrame({
        'state': [state] * len(g_df),
        'region': [region] * len(g_df), 
        'school_lavel': list(g_df.index),
        'number_of_school': list(g_df.values)
    })

def processing_cnt(state: str,
                   reg_col_name: str,
                   target_col_name: str,
                   df: pd.DataFrame) -> pd.DataFrame:
    
    concated_df = pd.DataFrame()
    reg_li = df[reg_col_name].unique()
    
    for reg in reg_li:
        reg_ext = df.loc[df[reg_col_name] == reg, ]
        reg_ext = reg_ext.groupby(target_col_name)[target_col_name].count()
        reg_ext = pd.DataFrame({
            'state': [state] * len(reg_ext),
            'region': [reg] * len(reg_ext),
            'school_lavel': list(reg_ext.index),
            'number_of_school': list(reg_ext.values)
        })
        concated_df = pd.concat([concated_df, reg_ext])
        concated_df = concated_df.reset_index(drop=True)
    return concated_df

sh_dataset = load_datasets('school')

daegu_sch = sh_dataset['daegu_school_2024'].iloc[:, :3].copy()
daegu_sch['class'] = daegu_sch['학교명'].apply(school_class) 

r_path = './preprocessed_dataset'
daegu_reg_school_count = processing_cnt(state ='대구광역시',
                                        reg_col_name ='관할구군청',
                                        target_col_name ='class',
                                        df = daegu_sch)

kb_sch = sh_dataset['kb_school_2024'].iloc[:, :3].copy()
kb_sch['class'] = kb_sch['학교(유치원)명'].apply(school_class)

kb_reg_school_count = pd.DataFrame()
reg_li = kb_sch['시군명'].unique()

for reg in reg_li:
    reg_ext = kb_sch.loc[kb_sch['시군명'] == reg, ]
    reg_ext = region_school_cnt('경상북도', reg, 'class', reg_ext)
    kb_reg_school_count = pd.concat([kb_reg_school_count, reg_ext])
kb_reg_school_count = kb_reg_school_count.reset_index(drop=True)

reg_school_count = pd.concat([daegu_reg_school_count, kb_reg_school_count])
reg_school_count = reg_school_count.reset_index(drop=True)