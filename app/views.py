from django.shortcuts import render, render_to_response
import os, json

def main(request):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    rawdata = open(os.path.join(cur_path, "data/aamas2007affil.txt"))
    lines = rawdata.readlines()
    data = []
    rank = 1
    for i in range(2, len(lines), 3):
        uname = lines[i].split(' ', 1)[1].strip()
        citation = float(lines[i+1].split(' ', 1)[1].strip())
        data.append((rank, uname, (100-rank), citation, 0))
        rank += 1
    return render(request, "main.html", {"data": data})
