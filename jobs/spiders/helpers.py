import autopager
import requests

def find_page_data(url):
    res_arr = autopager.urls(requests.get(url))
    arr = []
    unique_str = set(res_arr)

    for number in unique_str:
        arr.append(number)

    while url in arr:
        arr.remove(url)

    n = len(arr)
    s = arr[1]
    l = len(s)
    pattern = ""

    for i in range(l):
        for j in range(i + 1, l + 1):
            stem = s[i:j]
            k = 1
            for k in range(1, n):
                if stem not in arr[k]:
                    break
            if (k + 1 == n and len(pattern) < len(stem)):
                pattern = stem

    sub_str = 0
    sub_arr = []
    sub_step = 0

    for item in arr:
        sub_str = max(int(sub_str), int(item[len(pattern):]))
        sub_arr.append(int(item[len(pattern):]))

    sub_arr.sort()
    sub_step = sub_arr[0]

    if len(sub_arr) >= 3:
        sub_step = sub_arr[1] - sub_arr[0]

    return pattern + "{}", sub_str, sub_step
