

import re


def prepare_url(url, params, pachs=[]):
    url = url + "?"
    for param in params:
        for pach in pachs:
            print((pach[0], param[1]))
            print(pach[0] in param[1])
            regexp = re.compile(pach[0])
            if regexp.search(param[1]):
                print("replace with:", pach[1])
                param[1] = re.sub(pach[0], pach[1], param[1])
                print("output:", param)
        url = url + param[0]+"="+param[1]+"&"
    print(url)
    return url[0:-1]
