from pynput.keyboard import Listener
from pyperclip import paste
import time, requests, html, json

def welcome():
    print("""
####################################
##  Welcome English's Simple Way  ##
####################################
""")

def pressed(key):
    global cc_time
    key= str(key)
    
    if key == r"'\x03'":          # '\x03' = "c" after "ctrl"
        if cc_time == None:
            cc_time= time.time()

        elif cc_time != None:
            if (time.time() - cc_time) <= 1:
                cc_time= time.time()
                start()
                time.sleep(1.3)
            else:                
                cc_time= time.time()
            
                
            
def start():
    # searching
    r= requests.get("https://tureng.com/tr/turkce-ingilizce/" + paste())
    site= html.unescape(r.text)

    #Is there any error
    if site.find('<td class="rc0 hidden-xs">') == -1:
        print("There isn't such word in the dictionary.")
    
    #If no error
    else:
        #separating
        low= [] # list_of_words
        
        global line
        line= 10 # how many line of tureng
        for i in range(1, line*2+1): # example you want first 3 line -> 3x2=6 6+1=7 --> range(1,7) 
            td= site.find( '<td class="rc0 hidden-xs">'+str(i)+"</td>" ) # the start of word line
            low.append( site.rfind("<tr>",0,td) ) # start line's <tr>
            low.append( site.find("</tr>", low[-1])+4) # last elements's last letter of </tr>

        #assembling
        list= []
        for i in range(0, len(low), 2):
            list.append(site[ low[i] : low[i+1] ])

        #naming
        number= []
        type= []
        w1= []
        w2= []

        for l in list:
            finish= [l.find("</td>"), l.find("</td>", l.find("</td>")+1)]
            start= [l.rfind(">", 0, finish[0]), l.rfind(">", 0, finish[1])]
            number.append( l[ start[0]+1 : finish[0] ] )
            type.append( l[ start[1]+1 : finish[1] ] )
            
            finish= [l.find("</a>"), l.find("</a>", l.find("</a>")+1)]
            start= [l.rfind(">", 0, finish[0]), l.rfind(">", 0, finish[1])]
            w1.append( l[ start[0]+1 : finish[0] ] )
            w2.append( l[ start[1]+1 : finish[1] ] )
        
        #printing
        print("-*- -*- -*-\n")
        for i in range(line):
            print("{0:2} --  {1:15}  --  {2}  --  {3}".format(number[i], type[i], w1[i], w2[i]))

        #saving
        save(number, type, w1, w2)

def save(number, type, w1, w2):
    with open("cft_db", "a") as f:
        for i in range(line):
            f.write("\n{} --  {}  --  {}  --  {}".format(number[i], type[i], w1[i], w2[i]))

if __name__ == "__main__":
    cc_time= None
    welcome()
    with Listener(on_press=pressed) as listener:
        listener.join()

# will add:
# - exams
# - history (added)
# - make fav
# - gui
