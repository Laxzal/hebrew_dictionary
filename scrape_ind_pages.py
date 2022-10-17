import time
import logging
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.DEBUG)


def present_tense_verb(search_table):
    present_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                          'english_word', 'chaser'])

    id_list = {'AP-ms': ['singular', 'masculine'], 'AP-fs': ['singular', 'feminine'],
               'AP-mp': ['plural', 'masculine'], 'AP-fp': ['plural', 'feminine']}
    verb_form = 'present'
    person = 1

    for i in range(len(id_list)):
        index = list(id_list.keys())[i]
        form = id_list[index][0]
        gender = id_list[index][1]
        hebrew_word = search_table[i].findAll('div', {'id': str(index)})[0].select('span')[0].text
        english_word = search_table[i].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
            0].text
        try:
            chaser_word = search_table[i].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan

        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array, columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                                    'english_word', 'chaser'])
        present_table = pd.concat([present_table, temp_df])

    return present_table


def past_tense_verb(search_table):
    past_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                       'english_word', 'chaser'])
    id_list = {'PERF-1s': [1, 'singular', ['masculine', 'feminine']],
               'PERF-1p': [1, 'plural', ['masculine', 'feminine']],
               'PERF-2ms': [2, 'singular', 'masculine'], 'PERF-2fs': [2, 'singular', 'feminine'],
               'PERF-2mp': [2, 'plural', 'masculine'], 'PERF-2fp': [2, 'plural', 'feminine'],
               'PERF-3ms': [3, 'singular', 'masculine'], 'PERF-3fs': [3, 'singular', 'feminine'],
               'PERF-3p': [3, 'plural', ['masculine', 'feminine']]}
    verb_form = 'past'
    person_list = [1, 2, 3]
    counter = 4

    for x in range(len(id_list)):
        index = list(id_list.keys())[x]
        person = id_list[index][0]
        form = id_list[index][1]
        if not isinstance(id_list[index][2], list):
            gender = id_list[index][2]
        elif len(id_list[index][2]) == 2:
            gender = id_list[index][2][0]
        hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
        english_word = \
            search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                0].text
        try:
            chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                        'english_word', 'chaser'])
        past_table = pd.concat([past_table, temp_df])
        if index in ['PERF-1s', 'PERF-1p', 'PERF-3p']:
            # for feminine
            gender = id_list[index][2][1]
            hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
            english_word = \
                search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div',
                                                                                    {'class': 'meaning'})[
                    0].text
            temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1,
                                                                                                                     -1)
            temp_df = pd.DataFrame(temp_array,
                                   columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                            'english_word', 'chaser'])
            past_table = pd.concat([past_table, temp_df])
        counter += 1

    return past_table


def future_tense_verb(search_table):
    future_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                         'english_word', 'chaser'])
    id_list = {'IMPF-1s': [1, 'singular', ['masculine', 'feminine']],
               'IMPF-1p': [1, 'plural', ['masculine', 'feminine']],
               'IMPF-2ms': [2, 'singular', 'masculine'], 'IMPF-2fs': [2, 'singular', 'feminine'],
               'IMPF-2mp': [2, 'plural', 'masculine'], 'IMPF-2fp': [2, 'plural', 'feminine'],
               'IMPF-3ms': [3, 'singular', 'masculine'], 'IMPF-3fs': [3, 'singular', 'feminine'],
               'IMPF-3mp': [3, 'plural', 'masculine'], 'IMPF-3fp': [3, 'plural', 'feminine']}
    verb_form = 'future'
    counter = 13
    for x in range(len(id_list)):
        index = list(id_list.keys())[x]
        person = id_list[index][0]
        form = id_list[index][1]
        if not isinstance(id_list[index][2], list):
            gender = id_list[index][2]
        elif len(id_list[index][2]) == 2:
            gender = id_list[index][2][0]
        hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
        english_word = search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
            0].text
        try:
            chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                        'english_word', 'chaser'])
        future_table = pd.concat([future_table, temp_df])
        if index in ['IMPF-1s', 'IMPF-1p']:
            # for feminine
            gender = id_list[index][2][1]
            hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
            english_word = \
                search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                    0].text
            try:
                chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
            except IndexError:
                chaser_word = np.nan
            temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1,
                                                                                                                     -1)
            temp_df = pd.DataFrame(temp_array,
                                   columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                            'english_word', 'chaser'])
            future_table = pd.concat([future_table, temp_df])
        counter += 1
    return future_table


def imperative_tense_verb(search_table):
    imperative_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                             'english_word', 'chaser'])

    id_list = {'IMP-2ms': ['singular', 'masculine'], 'IMP-2fs': ['singular', 'feminine'],
               'IMP-2mp': ['plural', 'masculine'], 'IMP-2fp': ['plural', 'feminine']}
    verb_form = 'imperative'
    person = 2
    counter = 23
    for i in range(len(id_list)):
        index = list(id_list.keys())[i]
        form = id_list[index][0]
        gender = id_list[index][1]
        hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
        english_word = search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
            0].text
        try:
            chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan

        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array, columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                                    'english_word', 'chaser'])
        imperative_table = pd.concat([imperative_table, temp_df])
        counter += 1
    return imperative_table


def passive_present_tense_verb(search_table):
    passive_present_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                                  'english_word', 'chaser'])

    id_list = {'passive-AP-ms': ['singular', 'masculine'], 'passive-AP-fs': ['singular', 'feminine'],
               'passive-AP-mp': ['plural', 'masculine'], 'passive-AP-fp': ['plural', 'feminine']}
    verb_form = 'passive_present'
    person = 1
    counter = 28
    for i in range(len(id_list)):
        index = list(id_list.keys())[i]
        form = id_list[index][0]
        gender = id_list[index][1]
        hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
        try:
            english_word = \
                search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                    0].text
        except IndexError:
            english_word = str(f'Passive form of {row["meaning"]}')
        try:
            chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array, columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                                    'english_word', 'chaser'])
        passive_present_table = pd.concat([passive_present_table, temp_df])
        counter += 1

    return passive_present_table


def passive_past_tense_verb(search_table):
    passive_past_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                               'english_word', 'chaser'])
    id_list = {'passive-PERF-1s': [1, 'singular', ['masculine', 'feminine']],
               'passive-PERF-1p': [1, 'plural', ['masculine', 'feminine']],
               'passive-PERF-2ms': [2, 'singular', 'masculine'], 'passive-PERF-2fs': [2, 'singular', 'feminine'],
               'passive-PERF-2mp': [2, 'plural', 'masculine'], 'passive-PERF-2fp': [2, 'plural', 'feminine'],
               'passive-PERF-3ms': [3, 'singular', 'masculine'], 'passive-PERF-3fs': [3, 'singular', 'feminine'],
               'passive-PERF-3p': [3, 'plural', ['masculine', 'feminine']]}
    verb_form = 'passive_past'
    person_list = [1, 2, 3]
    counter = 32

    for x in range(len(id_list)):
        index = list(id_list.keys())[x]
        person = id_list[index][0]
        form = id_list[index][1]
        if not isinstance(id_list[index][2], list):
            gender = id_list[index][2]
        elif len(id_list[index][2]) == 2:
            gender = id_list[index][2][0]
        hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
        try:
            english_word = \
                search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                    0].text
        except IndexError:
            english_word = str(f'Passive form of {row["meaning"]}')
        try:
            chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                        'english_word', 'chaser'])
        past_table = pd.concat([passive_past_table, temp_df])
        if index in ['passive-PERF-1s', 'passive-PERF-1p', 'passive-PERF-3p']:
            # for feminine
            gender = id_list[index][2][1]
            hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
            try:
                english_word = \
                    search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                        0].text
            except IndexError:
                english_word = str(f'Passive form of {row["meaning"]}')
            try:
                chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
            except IndexError:
                chaser_word = np.nan
            temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1,
                                                                                                                     -1)
            temp_df = pd.DataFrame(temp_array,
                                   columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                            'english_word', 'chaser'])
            passive_past_table = pd.concat([passive_past_table, temp_df])
        counter += 1

    return passive_past_table


def passive_future_tense_verb(search_table):
    passive_future_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                                 'english_word', 'chaser'])
    id_list = {'passive-IMPF-1s': [1, 'singular', ['masculine', 'feminine']],
               'passive-IMPF-1p': [1, 'plural', ['masculine', 'feminine']],
               'passive-IMPF-2ms': [2, 'singular', 'masculine'], 'passive-IMPF-2fs': [2, 'singular', 'feminine'],
               'passive-IMPF-2mp': [2, 'plural', 'masculine'], 'passive-IMPF-2fp': [2, 'plural', 'feminine'],
               'passive-IMPF-3ms': [3, 'singular', 'masculine'], 'passive-IMPF-3fs': [3, 'singular', 'feminine'],
               'passive-IMPF-3mp': [3, 'plural', 'masculine'], 'passive-IMPF-3fp': [3, 'singular', 'feminine']}
    verb_form = 'passive_future'
    counter = 41
    for x in range(len(id_list)):
        index = list(id_list.keys())[x]
        person = id_list[index][0]
        form = id_list[index][1]
        if not isinstance(id_list[index][2], list):
            gender = id_list[index][2]
        elif len(id_list[index][2]) == 2:
            gender = id_list[index][2][0]
        hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
        try:
            english_word = \
                search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                    0].text
        except IndexError:
            english_word = str(f'Passive form of {row["meaning"]}')
        try:
            chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                        'english_word', 'chaser'])
        passive_future_table = pd.concat([passive_future_table, temp_df])
        if index in ['passive-IMPF-1s', 'passive-IMPF-1p']:
            # for feminine
            gender = id_list[index][2][1]
            hebrew_word = search_table[counter].findAll('div', {'id': str(index)})[0].select('span')[0].text
            try:
                english_word = \
                    search_table[counter].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                        0].text
            except IndexError:
                english_word = str(f'Passive form of {row["meaning"]}')
            try:
                chaser_word = search_table[counter].select('span[class*=chaser]')[0].text.replace('~', '').strip()
            except IndexError:
                chaser_word = np.nan
            temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1,
                                                                                                                     -1)
            temp_df = pd.DataFrame(temp_array,
                                   columns=['verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                            'english_word', 'chaser'])
            passive_future_table = pd.concat([passive_future_table, temp_df])
        counter += 1
    return passive_future_table


def single_adjective(search_table):
    pealim_adjective_db = pd.DataFrame(columns=['form',
                                                'gender',
                                                'hebrew_word',
                                                'pronunciation',
                                                'english_word'])
    id_list = {'ms-a': ['singular', 'masculine'],
               'fs-a': ['singular', 'feminine']}
    list_of_webpage_ids = []
    for z in search_table.findAll('div', {'id': True}):
        # print(z.attrs)
        if len(z.attrs) == 2:
            list_of_webpage_ids.append(list(z.attrs.values())[1])
        else:
            list_of_webpage_ids.append(list(z.attrs.values())[0])

    if not (list_of_webpage_ids - id_list.keys()):
        print('Reducing id_list keys')
        id_list = {x: id_list[x] for x in list_of_webpage_ids if x in id_list}
        print(id_list)

    for i, (k, v) in enumerate(id_list.items()):
        form = v[0]
        gender = v[1]

        hebrew_word = search_table.findAll('div', {'id': str(k)})[0].select('span')[0].text
        english_word = search_table.findAll('div', {'id': str(k)})[0].findAll('div', {'class': 'meaning'})[
            0].text
        try:
            chaser_word = search_table.findAll('div', {'id': str(k)})[0].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['form', 'gender', 'hebrew_word', 'english_word',
                                        'chaser'])

        pealim_adjective_db = pd.concat([pealim_adjective_db, temp_df])

    return pealim_adjective_db


def plural_adjective(search_table):
    pealim_adjective_db = pd.DataFrame(columns=['form',
                                                'gender',
                                                'hebrew_word',
                                                'pronunciation',
                                                'english_word'])
    id_list = {'mp-a': ['plural', 'masculine'],
               'fp-a': ['plural', 'feminine']}
    list_of_webpage_ids = []
    for z in search_table.findAll('div', {'id': True}):
        # print(z.attrs)
        if len(z.attrs) == 2:
            list_of_webpage_ids.append(list(z.attrs.values())[1])
        else:
            list_of_webpage_ids.append(list(z.attrs.values())[0])

    if not (list_of_webpage_ids - id_list.keys()):
        print('Reducing id_list keys')
        id_list = {x: id_list[x] for x in list_of_webpage_ids if x in id_list}
        print(id_list)

    for i, (k, v) in enumerate(id_list.items()):
        form = v[0]
        gender = v[1]

        hebrew_word = search_table.findAll('div', {'id': str(k)})[0].select('span')[0].text
        english_word = search_table.findAll('div', {'id': str(k)})[0].findAll('div', {'class': 'meaning'})[
            0].text
        try:
            chaser_word = search_table.findAll('div', {'id': str(k)})[0].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([form, gender, hebrew_word, english_word, chaser_word]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['form', 'gender', 'hebrew_word', 'english_word',
                                        'chaser'])

        pealim_adjective_db = pd.concat([pealim_adjective_db, temp_df])

    return pealim_adjective_db


def single_noun(search_table):
    pealim_pronomial_db = pd.DataFrame(columns=['noun_form',  # singular/plural
                                                'person',  # 1/2/3
                                                'form',  # singular/plural
                                                'gender',  # masc/fem
                                                'hebrew_word',
                                                'english_word',
                                                'chaser'])
    id_list = {'s-P-1s': ['singular', 1, 'singular', ['masculine', 'feminine']],
               's-P-2ms': ['singular', 2, 'singular', 'masculine'],
               's-P-2fs': ['singular', 2, 'singular', 'feminine'],
               's-P-3ms': ['singular', 3, 'singular', 'masculine'],
               's-P-3fs': ['singular', 3, 'singular', 'feminine'],
               's-P-1p': ['singular', 1, 'plural', ['masculine', 'feminine']],
               's-P-2mp': ['singular', 2, 'plural', 'masculine'],
               's-P-2fp': ['singular', 2, 'plural', 'feminine'],
               's-P-3mp': ['singular', 3, 'plural', 'masculine'],
               's-P-3fp': ['singular', 3, 'plural', 'feminine']}

    # Checl which ID exists in search table
    list_of_webpage_ids = []
    for z in search_table.findAll('div', {'id': True}):
        # print(z.attrs)
        if len(z.attrs) == 2:
            list_of_webpage_ids.append(list(z.attrs.values())[1])
        else:
            list_of_webpage_ids.append(list(z.attrs.values())[0])

    substring = 'p-'

    list_of_webpage_ids = [item for item in list_of_webpage_ids if not item.startswith(substring)]

    if not (list_of_webpage_ids - id_list.keys()):
        print('Reducing id_list keys')
        id_list = {x: id_list[x] for x in list_of_webpage_ids if x in id_list}
        print(id_list)

    for i, (k, v) in enumerate(id_list.items()):
        noun_number = v[0]
        person = v[1]
        form = v[2]
        if not isinstance(v[3], list):
            gender = v[3]
        else:
            gender = v[3][0]
        hebrew_word = search_table.findAll('div', {'id': str(k)})[0].select('span')[0].text
        english_word = search_table.findAll('div', {'id': str(k)})[0].findAll('div', {'class': 'meaning'})[
            0].text
        try:
            chaser_word = search_table.findAll('div', {'id': str(k)})[0].select('span[class*=chaser]')[0].text.replace('~', '').strip()
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([noun_number, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1,
                                                                                                                   -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['noun_form', 'person', 'form', 'gender', 'hebrew_word', 'english_word',
                                        'chaser'])
        pealim_pronomial_db = pd.concat([pealim_pronomial_db, temp_df])
        if k in ['s-P-1s', 's-P-1p', 'p-P-1s']:
            gender = v[3][1]
            hebrew_word = table_pronomial.findAll('div', {'id': str(k)})[0].select('span')[0].text
            english_word = \
                table_pronomial.findAll('div', {'id': str(k)})[0].findAll('div', {'class': 'meaning'})[
                    0].text
            try:
                chaser_word = search_table.findAll('div', {'id': str(k)})[0].select('span[class*=chaser]')[0].text.replace('~', '').strip()
            except IndexError:
                chaser_word = np.nan
            temp_array = np.array([noun_number, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(
                1, -1)
            temp_df = pd.DataFrame(temp_array, columns=['noun_form', 'person', 'form', 'gender', 'hebrew_word',
                                                        'english_word', 'chaser'])
            pealim_pronomial_db = pd.concat([pealim_pronomial_db, temp_df])

    return pealim_pronomial_db


def plural_noun(search_table):
    pealim_pronomial_db = pd.DataFrame(columns=['noun_form',  # singular/plural
                                                'person',  # 1/2/3
                                                'form',  # singular/plural
                                                'gender',  # masc/fem
                                                'hebrew_word',
                                                'english_word',
                                                'chaser'])
    id_list = {'p-P-1s': ['plural', 1, 'plural', ['masculine', 'feminine']],
               'p-P-2ms': ['plural', 2, 'plural', 'masculine'],
               'p-P-2fs': ['plural', 2, 'plural', 'feminine'],
               'p-P-3ms': ['plural', 3, 'plural', 'masculine'],
               'p-P-3fs': ['plural', 3, 'plural', 'feminine']}

    # Checl which ID exists in search table
    list_of_webpage_ids = []
    for z in search_table.findAll('div', {'id': True}):
        # print(z.attrs)
        if len(z.attrs) == 2:
            list_of_webpage_ids.append(list(z.attrs.values())[1])
        else:
            list_of_webpage_ids.append(list(z.attrs.values())[0])

    substring = 's-'

    list_of_webpage_ids = [item for item in list_of_webpage_ids if not item.startswith(substring)]

    if not (list_of_webpage_ids - id_list.keys()):
        print('Reducing id_list keys')
        id_list = {x: id_list[x] for x in list_of_webpage_ids if x in id_list}
        print(id_list)

    for i, (k, v) in enumerate(id_list.items()):
        noun_number = v[0]
        person = v[1]
        form = v[2]
        if not isinstance(v[3], list):
            gender = v[3]
        else:
            gender = v[3][0]
        hebrew_word = search_table.findAll('div', {'id': str(k)})[0].select('span')[0].text
        english_word = search_table.findAll('div', {'id': str(k)})[0].findAll('div', {'class': 'meaning'})[
            0].text
        try:
            chaser_word = search_table.findAll('div', {'id': str(k)})[0].select('span[class*=chaser]')[0].text.replace('~', '').strip()
            #print(chaser_word)
        except IndexError:
            chaser_word = np.nan
        temp_array = np.array([noun_number, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(1,
                                                                                                                   -1)
        temp_df = pd.DataFrame(temp_array,
                               columns=['noun_form', 'person', 'form', 'gender', 'hebrew_word', 'english_word',
                                        'chaser'])
        pealim_pronomial_db = pd.concat([pealim_pronomial_db, temp_df])
        if k in ['s-P-1s', 's-P-1p', 'p-P-1s']:
            gender = v[3][1]
            hebrew_word = table_pronomial.findAll('div', {'id': str(k)})[0].select('span')[0].text
            english_word = \
                table_pronomial.findAll('div', {'id': str(k)})[0].findAll('div', {'class': 'meaning'})[
                    0].text
            try:
                chaser_word = search_table.findAll('div', {'id': str(k)})[0].select('span[class*=chaser]')[0].text.replace('~', '').strip()
            except IndexError:
                chaser_word = np.nan
            temp_array = np.array([noun_number, person, form, gender, hebrew_word, english_word, chaser_word]).reshape(
                1, -1)
            temp_df = pd.DataFrame(temp_array, columns=['noun_form', 'person', 'form', 'gender', 'hebrew_word',
                                                        'english_word', 'chaser'])
            pealim_pronomial_db = pd.concat([pealim_pronomial_db, temp_df])

    return pealim_pronomial_db


user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
url = 'https://www.pealim.com'

pealim_database = pd.read_csv('pealim_database.csv')

pealim_noun = pd.DataFrame(columns=['id', 'word', 'single_state', 'plural_state', 'single_construct_state',
                                    'plural_construct_state', 'meaning'])
pealim_verb = pd.DataFrame(columns=['id', 'infinitive_form', 'meaning'])

pealim_pronomial_db = pd.DataFrame(columns=['id',
                                            'noun_form',  # singular/plural
                                            'person',  # 1/2/3
                                            'form',  # singular/plural
                                            'gender',  # masc/fem
                                            'hebrew_word',
                                            'english_word',
                                            'chaser'])

future_table = pd.DataFrame(columns=['id', 'verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                     'english_word', 'chaser'])
present_table = pd.DataFrame(columns=['id', 'verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                      'english_word', 'chaser'])
past_table = pd.DataFrame(columns=['id', 'verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                   'english_word', 'chaser'])
imperative_table = pd.DataFrame(columns=['id', 'verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                         'english_word', 'chaser'])

passive_future_table = pd.DataFrame(columns=['id', 'verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                             'english_word', 'chaser'])
passive_past_table = pd.DataFrame(columns=['id', 'verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                           'english_word', 'chaser'])
passive_present_table = pd.DataFrame(columns=['id', 'verb_form', 'person', 'form', 'gender', 'hebrew_word',
                                              'english_word', 'chaser'])
pealim_adjective_db = pd.DataFrame(columns=['id',
                                            'form',
                                            'gender',
                                            'hebrew_word',
                                            'pronunciation',
                                            'english_word'])
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
s.mount('https://', HTTPAdapter(max_retries=retries))
for index, row in pealim_database.iterrows():
    time.sleep(0.05)
    progress = index / len(pealim_database)
    print(np.round(progress * 100))
    print(f'{index} / {len(pealim_database)}')
    print(row['word'])

    # If word is noun
    if 'Noun' in row['part_of_speech']:
        response = s.get(url + row['link'])
        soup = BeautifulSoup(response.text, 'html.parser')
        search_table = soup.findAll('td', {'class': 'conj-td'})
        # single_state
        '''loop'''

        try:
            div_s = search_table[0].findAll('div', {'id': 's'})
            single_state_word = div_s[0].findAll('span', {'class': 'menukad'})[0].text
        except IndexError:
            single_state_word = np.nan
            continue
        # plural_state
        if len(search_table) > 1:
            div_p = search_table[1].findAll('div', {'id': 'p'})
            if not div_p:
                plural_state = np.nan
            else:
                plural_state = div_p[0].findAll('span', {'class': 'menukad'})[0].text
        else:
            plural_state = np.nan

        # constructor state - singular
        try:
            div_sc = search_table[2].findAll('div', {'id': 'sc'})
            single_construct_state = div_sc[0].findAll('span', {'class': 'menukad'})[0].text.replace('־',
                                                                                                     '')  # Weird dash char
        except IndexError:
            single_construct_state = np.nan
        # constructor state - plural
        try:
            div_pc = search_table[3].findAll('div', {'id': 'pc'})
            plural_construct_state = div_pc[0].findAll('span', {'class': 'menukad'})[0].text.replace('־',
                                                                                                     '')  # Weird dash char
        except IndexError:
            plural_construct_state = np.nan

        temp_array = np.array([row['id'], row['word'], single_state_word, plural_state, single_construct_state,
                               plural_construct_state, row['meaning']]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array, columns=['id', 'word', 'single_state', 'plural_state',
                                                    'single_construct_state', 'plural_construct_state', 'meaning'])
        pealim_noun = pd.concat([pealim_noun, temp_df])
        # IF pronomial state is existing
        if not not soup.findAll('button', {'id': 'pronominal-forms-control'}):
            table_pronomial = soup.findAll('tbody')[1]
            # singular 1 singular masc/fem
            if pd.isnull(single_state_word):
                continue
            else:
                temp_df = single_noun(table_pronomial)
                temp_df.insert(0, 'id', row['id'])

                pealim_pronomial_db = pd.concat([pealim_pronomial_db,
                                                 temp_df])

            if pd.isnull(plural_state):
                continue
            else:
                temp_df = plural_noun(table_pronomial)
                temp_df.insert(0, 'id', row['id'])
                pealim_pronomial_db = pd.concat([pealim_pronomial_db,
                                                 temp_df])



    elif 'Verb' in row['part_of_speech']:
        response = s.get(url + row['link'])
        soup = BeautifulSoup(response.text, 'html.parser')
        search_table = soup.findAll('td', {'class': 'conj-td'})

        # infinitive word

        try:
            div_infinitive = soup.findAll('div', {'id': 'INF-L'})[0]
            infinitive_word = div_infinitive.select('span')[0].text
        except IndexError:
            infinitive_word = row['word']
        temp_array = np.array([row['id'], infinitive_word, row['meaning']]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array, columns=['id', 'infinitive_form', 'meaning'])
        pealim_verb = pd.concat([pealim_verb, temp_df])

        try:
            temp_present_table = present_tense_verb(search_table)
            temp_present_table['id'] = row['id']
            present_table = pd.concat([present_table, temp_present_table])
        except IndexError:
            continue

        try:
            temp_past_table = past_tense_verb(search_table)
            temp_past_table['id'] = row['id']
            past_table = pd.concat([past_table, temp_past_table])
        except IndexError:
            continue

        try:
            temp_future_table = future_tense_verb(search_table)
            temp_future_table['id'] = row['id']
            future_table = pd.concat([future_table, temp_future_table])
        except IndexError:
            continue

        try:
            temp_imperative_table = imperative_tense_verb(search_table)
            temp_imperative_table['id'] = row['id']
            imperative_table = pd.concat([imperative_table, temp_imperative_table])
        except IndexError:
            continue

        # check if passive form exists
        for i in range(len(soup.findAll('h3', {'class': "page-header"}))):
            if 'Passive' in soup.findAll('h3', {'class': "page-header"})[i].text:
                print('Passive')
                temp_passive_future_table = passive_future_tense_verb(search_table)
                temp_passive_future_table['id'] = row['id']
                passive_future_table = pd.concat([passive_future_table, temp_passive_future_table])

                temp_passive_present_table = passive_present_tense_verb(search_table)
                temp_passive_present_table['id'] = row['id']
                passive_present_table = pd.concat([passive_present_table, temp_passive_present_table])

                temp_passive_past_table = passive_past_tense_verb(search_table)
                temp_passive_past_table['id'] = row['id']
                passive_past_table = pd.concat([passive_past_table, temp_passive_past_table])
    elif 'Adjective' in row['part_of_speech']:
        response = s.get(url + row['link'])
        soup = BeautifulSoup(response.text, 'html.parser')
        search_table = soup.findAll('td', {'class': 'conj-td'})

        table_pronomial = soup.findAll('tbody')[0]
        try:
            temp_df = single_adjective(table_pronomial)
            temp_df.insert(0, 'id', row['id'])

            pealim_adjective_db = pd.concat([pealim_adjective_db,
                                             temp_df])
        except IndexError:
            continue
        try:
            temp_df = plural_adjective(table_pronomial)
            temp_df.insert(0, 'id', row['id'])
            pealim_adjective_db = pd.concat([pealim_adjective_db,
                                             temp_df])
        except IndexError:
            continue

pealim_noun.to_csv('pealim_noun_db.csv', index=False)
pealim_verb.to_csv('pealim_verb_db.csv', index=False)
pealim_pronomial_db.to_csv('pealim_pronomial_db.csv', index=False)
present_table.to_csv('pealim_verb_present_table_db.csv', index=False)
past_table.to_csv('pealim_verb_past_table_db.csv', index=False)
future_table.to_csv('pealim_verb_future_table_db.csv', index=False)
imperative_table.to_csv('pealim_verb_imperative_table_db.csv', index=False)
passive_future_table.to_csv('pealim_passive_future_table.csv', index=False)
passive_present_table.to_csv('pealim_passive_present_table.csv', index=False)
passive_past_table.to_csv('pealim_passive_past_table.csv', index=False)
pealim_adjective_db.to_csv('pealim_adjective_table_db.csv', index=False)
