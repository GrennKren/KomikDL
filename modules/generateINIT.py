import os
import sys
import re

def main():
    a = os.listdir()
    b = []
    for i in a:
        if(re.match('.+\.py$',i) and i != sys.argv[0].rsplit('\\',1)[1] and i != '__init__.py'):
            b.append("from .{} import *".format(re.sub('\.py$','',i)))

    with open('__init__.py','w') as f:
        f.write("\n".join(b))

if __name__ == '__main__':
    main()
