import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
url = 'https://www.pealim.com'

pealim_database = pd.read_csv('pealim_database.csv')

pealim_noun = pd.DataFrame(columns=['word', 'meaning', ''])

pealim_pronomial_db = pd.DataFrame(columns=['noun_number',  # singular/plural
                                            'person',  # 1/2/3
                                            'form',  # singular/plural
                                            'gender',  # masc/fem
                                            'hebrew_word',
                                            'english_word'])

for index, row in pealim_database.iterrows():

    # If there is no root
    if 'Noun' in row['part_of_speech']:
        response = requests.get(url + row['link'])
        soup = BeautifulSoup(response.text, 'html.parser')
        search_table = soup.findAll('td', {'class': 'conj-td'})
        # single_state
        '''loop'''
        div_s = search_table[0].findAll('div', {'id': 's'})
        single_state_word = div_s[0].findAll('span', {'class': 'menukad'})[0].text
        # plural_state
        if len(search_table) > 1:
            div_p = search_table[1].findAll('div', {'id': 'p'})
            plural_state = div_p[0].findAll('span', {'class': 'menukad'})[0].text

        # IF pronomial state is existing
        if not not soup.findAll('button', {'id': 'pronominal-forms-control'}):
            table_pronomial = soup.findAll('tbody')[1]
            # singular 1 singular masc/fem
            noun_number = 'singular'
            person = 1
            form = 'singular'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-1s'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-1s'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_1_s_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])
            gender = 'feminine'
            s_P_1_s_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # singular 2 singular masc/fem
            noun_number = 'singular'
            person = 2
            form = 'singular'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-2ms'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-2ms'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_2_s_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-2fs'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-2fs'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_2_s_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # singular 3 singular masc/fem
            noun_number = 'singular'
            person = 3
            form = 'singular'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-3ms'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-3ms'})[0].findAll('div', {'class': 'meaning'})[
                0].text

            s_P_3_s_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-3fs'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-3fs'})[0].findAll('div', {'class': 'meaning'})[
                0].text

            s_P_3_s_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # singular 1 plural masc/fem
            noun_number = 'singular'
            person = 1
            form = 'plural'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-1p'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-1p'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_1_p_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])
            gender = 'feminine'
            s_P_1_p_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # singular 2 plural masc/fem
            noun_number = 'singular'
            person = 2
            form = 'plural'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-2mp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-2mp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_2_p_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-2fp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-2fp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_2_p_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # singular 3 plural masc/fem
            noun_number = 'singular'
            person = 3
            form = 'plural'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-3mp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-3mp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_3_p_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 's-P-3fp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 's-P-3fp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            s_P_3_p_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # plural 1 singular masc/fem
            noun_number = 'plural'
            person = 1
            form = 'singular'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-1s'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-1s'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_1_s_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])
            gender = 'feminine'
            p_P_1_s_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # plural 2 singular masc/fem
            noun_number = 'plural'
            person = 2
            form = 'singular'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-2ms'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-2ms'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_2_s_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-2fs'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-2fs'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_2_s_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # plural 3 singular masc/fem
            noun_number = 'plural'
            person = 3
            form = 'singular'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-3ms'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-3ms'})[0].findAll('div', {'class': 'meaning'})[
                0].text

            p_P_3_s_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-3fs'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-3fs'})[0].findAll('div', {'class': 'meaning'})[
                0].text

            p_P_3_s_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # plural 1 plural masc/fem
            noun_number = 'plural'
            person = 1
            form = 'plural'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-1p'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-1p'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_1_p_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])
            gender = 'feminine'
            p_P_1_p_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # plural 2 plural masc/fem
            noun_number = 'plural'
            person = 2
            form = 'plural'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-2mp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-2mp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_2_p_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-2fp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-2fp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_2_p_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            # singular 3 plural masc/fem
            noun_number = 'plural'
            person = 3
            form = 'plural'
            gender = 'masculine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-3mp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-3mp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_3_p_m = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            gender = 'feminine'
            hebrew_word = table_pronomial.findAll('div', {'id': 'p-P-3fp'})[0].select('span')[0].text
            english_word = table_pronomial.findAll('div', {'id': 'p-P-3fp'})[0].findAll('div', {'class': 'meaning'})[
                0].text
            p_P_3_p_f = np.array([noun_number, person, form, gender, hebrew_word, english_word])

            temp_array = np.vstack([s_P_1_s_m,
                                    s_P_1_s_f,
                                    s_P_2_s_m,
                                    s_P_2_s_f,
                                    s_P_3_p_m,
                                    s_P_3_p_f,
                                    s_P_1_p_m,
                                    s_P_1_p_f,
                                    s_P_2_p_m,
                                    s_P_2_p_f,
                                    s_P_3_p_m,
                                    s_P_3_p_f,
                                    p_P_1_s_m,
                                    p_P_1_s_f,
                                    p_P_2_s_m,
                                    p_P_2_s_f,
                                    p_P_3_s_m,
                                    p_P_3_s_f,
                                    p_P_1_p_m,
                                    p_P_1_p_f,
                                    p_P_2_p_m,
                                    p_P_2_p_f,
                                    p_P_3_p_m,
                                    p_P_3_p_f
                                    ])
            print(temp_array)

            temp_df = pd.DataFrame(temp_array, columns=['noun_number',  # singular/plural
                                                        'person',  # 1/2/3
                                                        'form',  # singkar/plural
                                                        'gender',  # masc/fem
                                                        'hebrew_word',
                                                        'english_word'])

            pealim_pronomial_db = pd.concat([pealim_pronomial_db, temp_df])

    elif 'Verb' in row['part_of_speech']:
        response = requests.get(url + row['link'])
        soup = BeautifulSoup(response.text, 'html.parser')
        search_table = soup.findAll('td', {'class': 'conj-td'})

        # infinitive word
        div_infinitive = search_table[-1].findAll('div', {'id': 'INF-L'})
        infinitive_word = div_infinitive[-1].findAll('span', {'class': 'menukad'})[0].text


def present_tense_verb(search_table):
    present_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'gender', 'hebrew_word',
                                          'english_word'])

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

        temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word])
        temp_df = pd.DataFrame(temp_array, columns=['verb_form', 'person', 'form', 'gender', 'gender', 'hebrew_word',
                                                    'english_word'])
        present_table = present_table.concat([present_table, temp_df])

    return present_table


def past_tense_verb(search_table):
    past_table = pd.DataFrame(columns=['verb_form', 'person', 'form', 'gender', 'gender', 'hebrew_word',
                                       'english_word'])
    id_list = {'PERF-1s': ['singular', ['masculine', 'feminine']],
               'PERF-1p': ['plural', ['masculine', 'feminine']],
               'PERF-2ms': ['singular', 'masculine'], 'PERF-2fs': ['singular', 'feminine'],
               'PERF-2mp': ['plural', 'masculine'], 'PERF-2fp': ['plural', 'feminine'],
               'PERF-3ms': ['singular', 'masculine'], 'PERF-3fs': ['singular', 'feminine'],
               'PERF-3p': ['plural', ['masculine', 'feminine']]}
    verb_form = 'past'
    person_list = [1, 2, 3]

    for i in person_list:
        for x in range(len(id_list)):
            person = person_list[i]
            index = list(id_list.keys())[x]
            form = id_list[index][0]
            if len(id_list[index][1]) == 1:
                gender = id_list[index][1]
            elif len(id_list[index][1]) == 2:
                gender = id_list[index][1][0]
            hebrew_word = search_table[i].findAll('div', {'id': str(index)})[0].select('span')[0].text
            english_word = search_table[i].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                0].text
            temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word])
            temp_df = pd.DataFrame(temp_array,
                                   columns=['verb_form', 'person', 'form', 'gender', 'gender', 'hebrew_word',
                                            'english_word'])
            past_table = past_table.concat([past_table, temp_df])
            if x == 0 or x == 1:
                # for feminine
                gender = id_list[index][1][1]
                hebrew_word = search_table[i].findAll('div', {'id': str(index)})[0].select('span')[0].text
                english_word = \
                    search_table[i].findAll('div', {'id': str(index)})[0].findAll('div', {'class': 'meaning'})[
                        0].text
                temp_array = np.array([verb_form, person, form, gender, hebrew_word, english_word])
                temp_df = pd.DataFrame(temp_array,
                                       columns=['verb_form', 'person', 'form', 'gender', 'gender', 'hebrew_word',
                                                'english_word'])
                past_table = past_table.concat([past_table, temp_df])

    return past_table
