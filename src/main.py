from textnode import *
from static_gen import generate_public_dir, generate_pages_recursive 

def main():

    generate_public_dir()
    generate_pages_recursive("content", "template.html", "public")

main()
