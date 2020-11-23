import argparse


parser = argparse.ArgumentParser(description='Get the video input and output path to perfrom tracking on')
parser.add_argument('--input', help='input path')
parser.add_argument('--output', help='output path')

args = parser.parse_args()

print(args.input)