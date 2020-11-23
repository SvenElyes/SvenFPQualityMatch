import os

import argparse


parser = argparse.ArgumentParser(description='create histogramms from the cutframes')
parser.add_argument('--input', help='folder path. in which the cutframes are located')

args = parser.parse_args()
#using com/tarikd/python-kmeans-dominant-colors/blob/master/color_kmeans.py to evaluate our cut frames and find the most dominant color 
files= os.listdir(f"cutframes/{args.input}")

for file in files:
    path= f"python3 cutframes/color_kmeans.py -i cutframes/{args.input}/{file} -o cutframes/{args.input}/histogramms/histo{file} -c 1"
    os.system(path)