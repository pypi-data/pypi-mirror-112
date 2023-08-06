import unicodedata
import os

def punctuation_mend(string):
    """return 英文标点符号

    Returns
    -------
    str
        输入字符串或者txt文件路径
    """
    table = {ord(f):ord(t) for f,t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０“”‘’',
        u',.!?[]()%#@&1234567890""\'\'')}   #其他自定义需要修改的符号可以加到这里
    if os.path.isfile(string):
        with open(string, 'r', encoding='utf-8') as f:
            res = unicodedata.normalize('NFKC', f.read())
            res = res.translate(table)
        with open(string, 'w', encoding='utf-8') as f:
            f.write(res)
    else:
        res = unicodedata.normalize('NFKC', string)
        res = res.translate(table)
        return res

# print(punctuation_mend('【】（）％＃＠＆“”'))
# punctuation_mend('F:/z.txt')
