from django.shortcuts import render, render_to_response
import os, json

def main(request):
    rawdata = open("data/aamas2007affil.txt")
    return render(request, "main.html")
