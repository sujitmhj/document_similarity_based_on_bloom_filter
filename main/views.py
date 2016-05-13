from django.shortcuts import render, HttpResponse
from django.views.generic import View
from pybloom.pybloom import BloomFilter
import uuid
from django import forms
import json
from nltk.corpus import stopwords
import nltk

nltk.data.path.append('/home/sujit/nltk_data')
# Create your views here.


### Settings for similarity detection ###
# shinglelength = 4

def get_filter(shingles):
    f = BloomFilter(capacity=10000, error_rate=0.001)
    for sg in shingles:
        f.add(" ".join(sg))
    return f





def shingle(tokens, shinglelength):
    arr = []
    if len(tokens)%2 == 1:
        max_i = len(tokens) - shinglelength
    else:
        max_i = len(tokens) - shinglelength + 1

    for i in range(max_i):
        arr.append(tokens[i:i+shinglelength])

    return arr


def get_similarity_value(tokens_A,tokens_B,single_length):
    shingle_A = shingle(tokens_A, single_length)
    shingle_B = shingle(tokens_B, single_length)



    print shingle_A

    b1 = get_filter(shingle_A)
    b2 = get_filter(shingle_B)

    common_count = 0

    for sg in shingle_B:
        if " ".join(sg) in b1:
            common_count = common_count + 1



    a_union_b = (len(shingle_A) + len(shingle_B) - common_count)
    print "single_size:", single_length
    print "union:",a_union_b
    print "common:", common_count

    similarity = (common_count*1.0)/a_union_b
    return similarity

def calculate_similarity(doc1, doc2, single_length):
    tokens_A = doc1.split()
    tokens_B = doc2.split()



    filtered_words_A = [word for word in tokens_A if word not in stopwords.words('english')]

    filtered_words_B = [word for word in tokens_B if word not in stopwords.words('english')]


    similarity_with_stop_words = get_similarity_value(tokens_A,tokens_B,single_length)

    similarity_without_stop_words = get_similarity_value(filtered_words_A,filtered_words_B,single_length)






    # if 
    # # print(b1.bitarray)
    # # print(b2.bitarray)
    # union = b1.union(b2)
    # intersection = b1.intersection(b2)
    # total_one = intersection.bitarray.count()
    # # print b1.bitarray
    # # print b2.bitarray
    # # print(union.bitarray.count())
    # total_bits = intersection.num_bits
    # percent = total_one*100.00/union.bitarray.count()
    return {"s_without":similarity_without_stop_words, "s_with":similarity_with_stop_words}



class FileUploadForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()

def handle_uploaded_file(f):
    file_name = uuid_str = "../uploaded_files/"+str(uuid.uuid1()) +".txt"
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class CalculateSimilarity(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

    def post(self, request, *args, **kwargs):
        doc1 = request.POST.get("file1")
        doc2 = request.POST.get("file2")
        single_size = int(request.POST.get("shingle_size",4))
        # form = FileUploadForm(request.POST)
        # if form.is_valid():
        #     handle_uploaded_file(request.FILES['file1'])
        #     handle_uploaded_file(frequest.FILES['file2'])

        # # form.file1
        if doc1!=None and doc2!=None:

            return HttpResponse(json.dumps(calculate_similarity(doc1,doc2, single_size)))
        # print "not gone"

