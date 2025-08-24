from textnode import *
from htmlnode import *

def main(): 
    tn = TextNode("this is some anchor text", 
                  TextType.LINK, "https://www.boot.dev")
    print(tn)

main()
