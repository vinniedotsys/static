import sys
from textnode import *
from static_gen import generate_public_dir, generate_pages_recursive 

def main():
    if not sys.argv[1]:
        basepath = "/"
    else :
        basepath = sys.argv[1]
    print(sys.argv)
    generate_public_dir()
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
