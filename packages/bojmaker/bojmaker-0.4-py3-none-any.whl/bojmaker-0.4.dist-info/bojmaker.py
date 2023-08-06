import os, sys
from bs4 import BeautifulSoup
from urllib.request import urlopen

def bojmaker(problem_number):
    url = 'https://www.acmicpc.net/problem/'
    sol = '''import sys
    
sys.stdin = open('input.txt')'''

    html = urlopen('{}{}'.format(url, problem_number))
    bs_object = BeautifulSoup(html, 'html.parser')

    problem_title = bs_object.find('span', id='problem_title').text
    problem_input = bs_object.find('pre', id='sample-input-1').text
    folder_name = str(problem_number) + '_' + problem_title

    try:
        os.mkdir('{}'.format(folder_name))
    except OSError:
        pass

    input_text = open('./{}/input.txt'.format(folder_name), 'w')
    input_text.write(problem_input)
    input_text.close()
    sol_py = open('./{}/sol1.py'.format(folder_name), 'w')
    sol_py.write(sol)
    sol_py.close()
    print('\nㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n{}\n\nSet up completed\nㅡㅡㅡㅡㅡㅡㅡㅡㅡ'.format(folder_name))


problem_number = int(sys.argv[1])

bojmaker(problem_number)