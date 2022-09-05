# This python helper file should be after sentiment score generation
# First create dictionary with category, sentence, sentiment
# Then can visualize through pandas dataframe
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, "/Users/leon/Income/python files/Telesales-QA-Framework")
from helper.lexicons import *

# def result_reformat(result_ls, lexicon_dic):    
#     result_dic = {} # initialize result dictionary
#     for i, result in enumerate(result_ls):
#         category = result[0]
#         sentence = result[1]
#         sentiment = result[2]

#         if category in result_dic: # check if the category is in our newly created result_dic
#             result_dic[category].append([sentence, sentiment])
#         else:
#             result_dic[category] = [[sentence, sentiment]]
#     return result_dic

# take the list generated by nlp_sentiment, and create dictionary using category name as key name
# each element in result_ls is like [category, sentence, sentiment]
def result_reformat(result_ls):    
    result_dic = {} # initialize result dictionary
    for i, result in enumerate(result_ls):
        sentence = result[0]
        category_ls = result[1]
        sentiment = result[2]
        for category in category_ls:
            if category in result_dic: # check if the category is in our newly created result_dic
                result_dic[category].append([sentence, sentiment])
            else:
                result_dic[category] = [[sentence, sentiment]]
    return result_dic

# result_ls is he result after sentiment analysis
# target label is the category list for a specific section
# 
def check_passed(result_ls, target_label, section_name = 'opening'):
    result_dic = result_reformat(result_ls)
    temp_pass_dic = {}
    for category, info in result_dic.items():
        sentiments = map(lambda x: x[1], info)
        passed = True
        for sentiment in sentiments:
            if sentiment == 'impolite':
                passed = False
        temp_pass_dic[category] = passed
    pass_dic = {}
    for key in target_label:
        if key in temp_pass_dic:
            if temp_pass_dic[key] == True:
                pass_dic[key] = True
            else:
                pass_dic[key] = False
        else:
            pass_dic[key] = False
    final_pass_dic = {section_name: pass_dic}
    return final_pass_dic

def assign_score(pass_dic, reference_dict, section_name = "opening"):
    temp_dict = {}
    score_dict = {}
    pass_result = pass_dic[section_name]
    reference_result = reference_dict[section_name]
    sum_score = 0
    for category, result in pass_result.items():
        if result == True:
            cur_score = reference_result[category]
            temp_dict[category] = cur_score
            sum_score += cur_score
        else:
            temp_dict[category] = 0
    score_dict[section_name] = temp_dict
    return score_dict, sum_score