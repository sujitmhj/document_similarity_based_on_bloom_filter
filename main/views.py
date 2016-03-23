from django.shortcuts import render, HttpResponse
from django.views.generic import View
from pybloom import BloomFilter

import json

# Create your views here.


### Settings for similarity detection ###
shinglelength = 4

def get_filter(shingles):
    f = BloomFilter(capacity=10000, error_rate=0.001)
    for shingle in shingles:
        f.add(" ".join(shingle))
    return f





def shingle(tokens):
    arr = []
    if len(tokens)%2 == 1:
        max_i = len(tokens) - shinglelength
    else:
        max_i = len(tokens) - shinglelength + 1

    for i in range(max_i):
        arr.append(tokens[i:i+shinglelength])

    return arr

def calculate_similarity(doc1, doc2):
    tokens_A = doc1.split()
    tokens_B = doc2.split()
    shingle_A = shingle(tokens_A)
    shingle_B = shingle(tokens_B)
    b1 = get_filter(shingle_A)
    b2 = get_filter(shingle_B)
    # print(b1.bitarray)
    # print(b2.bitarray)
    union = b1.union(b2)
    intersection = b1.intersection(b2)
    total_one = intersection.bitarray.count()
    # print b1.bitarray
    # print b2.bitarray
    # print(union.bitarray.count())
    total_bits = intersection.num_bits
    percent = total_one*100.00/union.bitarray.count()
    return {"similarity":percent}



class CalculateSimilarity(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

    def post(self, request, *args, **kwargs):
        doc1 = request.POST.get("doc1")
        doc2 = request.POST.get("doc2")
        if doc1!=None and doc2!=None:

            return HttpResponse(json.dumps(calculate_similarity(doc1,doc2)))