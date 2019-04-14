import re
import time

s = open('./notebooks/frenetic/data/wolf.xml','rb').read().decode('utf-8')

#output  = re.compile('<DEF>(.*?)</DEF>', re.DOTALL |  re.IGNORECASE).findall(s)
output  = re.split('<DEF>(.*?)</DEF>',s)


t = 5

for i,txt in enumerate(output):

    if '<' in txt or '>' in txt:
        print(txt)
    else:
        print('<DEF>')
        print(txt)
        print('</DEF>')
        time.sleep(t)
    print('\n\n')


