import os
import sys
os.system("")
import random
import msvcrt

class Game:
    def __init__(self, game_area, height,width,diff=0.2):
        self.width=width
        self.height=height
        self.mine_ammount=int((self.width*self.height)*diff)
        self.gamearea=game_area
        self.msg="""To reset press "r" key. Select space using arrow keys and clear marked space using "c" key, "f" for Flag."""
        self.game_over=False
        self.game_win=False
        self.clear_coord=[]
    # mine generation
    def mine_generation(self,h,w):
        
        coord_list=[]
        for i in range(0,self.height):
            for j in range(0,self.width):
                coord_list+=[[i,j]]
        coord_list.remove([h,w])
        mining= random.sample(coord_list, k=self.mine_ammount)  
        for i in mining:
            self.gamearea[i[0]][i[1]][0]=True
            coord_list.remove(i)
        self.clear_coord=coord_list
        # mines in area calculation
    
        for i in range(0,self.height):
            for j in range(0,self.width):
                for k in range(i-1,i+2):
                    if k>=0 and k<self.height:
                        for l in range(j-1, j+2):
                            if l>=0 and l<self.width:
                                if self.gamearea[k][l][0]==True:
                                    self.gamearea[i][j][1]+=1
        return
                                    
    # showing field
    def show(self, cursor_h=0, cursor_w=0):
            # clear play area
            os.system("cls")
            sys.stdout.write("\033[H")

            show_list="  "
            for i in range(1, self.width+1):
                
                if i<10:
                    show_list +="   0" + str(i)
                else:
                    show_list +="   " + str(i)
            show_list+="\033[E  "
            line=range(0,len(show_list)-5)
            for i in line:
                show_list+="_"
            show_list+="\033[E"
            for i in range(self.height):
                self.gamearea[i]
                
                if i+1<10:
                    show_list+="0"+str(i+1)+ "|"
                else:
                    show_list+=str(i+1)+ "|"
                for j in range(self.width):
                    if i == cursor_h and j == cursor_w:
                        cursor_loc="> "
                    else:
                        cursor_loc="  "
                    if self.gamearea[i][j][2]==True and self.gamearea[i][j][3]==False:
                        show_list+= " "+cursor_loc+"██"+"\033H"
                    elif self.gamearea[i][j][2]==True and self.gamearea[i][j][3]==True:
                        show_list+= " "+cursor_loc+"\033[49;38;5;51m▐▀\033[0m"+"\033H"
                    else:
                        if self.gamearea[i][j][0]==True:
                            show_list+= " "+cursor_loc+ "\033[38;49;31m" + "X" + "\033[0m"+" "+"\033H"
                        else: 
                            if self.gamearea[i][j][1]>0:
                                show_list+= " "+cursor_loc + "\033[49;38;5;226m"+ str(self.gamearea[i][j][1])+ "\033[0m" + " "+"\033H"
                            else:
                                show_list+= " "+cursor_loc + str(self.gamearea[i][j][1]) + " "+"\033H"
                if i<self.height-1:
                    show_list+= "|\033[E" +"  |" +" "*(len(line)-2)+"|\033[E"
                else:
                    show_list+= "|\033[E" + " "*(len(line)+1)+"\033[E" 
            if self.game_over==True and self.game_win==False:
                self.msg="""GAME OVER. Press "R" to reset"""
                show_list+=self.msg
            elif self.game_over==False and self.game_win==True:
                self.msg="""You won.  Press "R" to reset"""
                show_list+=self.msg
            elif self.game_win==False and len(self.clear_coord)==0:
                show_list+=self.msg
            elif self.game_win==False and len(self.clear_coord)>0:
                show_list+=self.msg+" "+ "\033[E"+"Clear spaces left: "+str(len(self.clear_coord))
            else:
                show_list+=self.msg
            return show_list

    #selection function
    def select(self, c_height, c_width, c_f_s):
            msg="""Navigate using arrow keys, "c" for clear, "f" for flag."""
            if (c_height<0 or c_height>self.height) or (c_width<0 or c_width>self.width):
                msg="""I dont know how but you are out of bounds."""
            else:
                if c_f_s == "c":
                    
                    if self.gamearea[c_height][c_width][2] == False:
                        
                        msg="Selected space has been cleared already."
                    elif self.gamearea[c_height][c_width][3] == True:
                        
                        msg="Selected space is flagged."
                    else:
                        self.gamearea[c_height][c_width][2] = False
                        self.gamearea[c_height][c_width][2] = self.gamearea[c_height][c_width][2]
                        if self.gamearea[c_height][c_width][0] == False:
                          self.clear_coord.remove([c_height, c_width])
                        self.uncover(c_height, c_width)
                        if self.gamearea[c_height][c_width][0] == True:
                            self.game_over=True
                        if len(self.clear_coord)==0:
                            self.game_win=True
                elif c_f_s == "m":
                      return c_height, c_width
                        
                elif c_f_s == "f":
                    self.gamearea[c_height][c_width][3]= not self.gamearea[c_height][c_width][3]
                    
                else:
                    
                    msg="""Press "f" key for Flag and "c" key for clear"""
            self.msg=msg

    #first selection function
    def first_select(self, c_height, c_width, c_f_s):
        
        msg="""Navigate using arrow keys, "c" for clear, "f" for flag."""
        if (c_height<0 or c_height>self.height) or (c_width<0 or c_width>self.width):
            msg="""I dont know how but you are out of bounds"""
            return self.gamearea, msg, c_height, c_width, False
        else:
                if c_f_s == "c":
                    if self.gamearea[c_height][c_width][2] == False:
                        msg="Selected space has been cleared already."
                    elif self.gamearea[c_height][c_width][3] == True:
                        
                        msg="Selected space is flagged."
                    else:
                        self.gamearea[c_height][c_width][2] = False
                        self.msg=msg
                        self.mine_generation(c_height, c_width)
                        self.uncover(c_height, c_width)
                        return c_height, c_width, True
                elif c_f_s == "m":
                      return c_height, c_width, False 
                else:
                    msg="""Press "c" key for clear"""

        self.msg=msg 
        return c_height, c_width, False
    
    #function to uncover area with no mines around
    def uncover(self,c_height, c_width):
        if self.gamearea[c_height][c_width][1] == 0:
                            clearing=[[c_height,c_width]]
                            for j in clearing:
                                    for k in range(j[0]-1,j[0]+2):
                                        if k>=0 and k<self.height:
                                            for l in range(j[1]-1, j[1]+2):
                                                if l>=0 and l<self.width:
                                                    if self.gamearea[k][l][2] == True:
                                                        self.gamearea[k][l][2]=False
                                                        self.clear_coord.remove([k, l])
                                                        if self.gamearea[k][l][1]==0:
                                                            clearing.append([k,l])
    
    def __repr__(self):
      print(self.show())
    
    #function to get input
    def input_f(self,h=0,w=0):
        
        if h==0 and w==0:
            sys.stdout.write("\033[{height};{width}H".format(width = 8, height=3))
            c_x=1
            c_y=1
        else:
            sys.stdout.write("\033[{height};{width}H".format(width = (w*5)+8, height=(h*2)+3))
            c_x=h+1
            c_y=w+1
        while True:
            
            if msvcrt.kbhit():
                thing=msvcrt.getch()
                msvcrt.ungetch(thing)
                if ord(thing) == 0 or ord(thing) ==224:
                    key=ord(msvcrt.getch())
                    if key==72:
                        if c_x>1:
                            c_x-=1
                            sys.stdout.write("\033[2A") #up
                            return [c_x-1, c_y-1, "m", False]
                    if key==80:
                        if c_x<self.height:
                            c_x+=1
                            sys.stdout.write("\033[2B") #down
                            return [c_x-1, c_y-1, "m", False]
                    if key==77:
                        if c_y<self.width:
                            c_y+=1
                            sys.stdout.write("\033[5C") #right
                            return [c_x-1, c_y-1, "m", False]
                    if key==75:
                        if c_y>1:
                            c_y-=1
                            sys.stdout.write("\033[5D") #left
                            return [c_x-1, c_y-1, "m", False]
                    if key==79:
                        pass #end
                else:
                    key=ord(msvcrt.getch())
                    if key==102:
                        return [c_x-1, c_y-1, "f", False] #f
                    if key==99:
                        return [c_x-1, c_y-1, "c", False] #c
                    if key==114:
                        return ["","" ,"" , True] #reset (r)
        
# list containing: [inicial value for mine: False, initial value for mines in area: 0, inicial value for hiden: True, inicial value for flag: False]
def gamearea(height=25,width=25):
        game_area=[[]for i in range(0,height)]
        for i in range(0,height):
            for j in range(0,width):
                    game_area[i]+= [[False, 0, True, False]]
        return game_area, height, width





def game(h,w,diff):
    game_area=gamearea(h,w)
    one=Game(game_area[0],game_area[1],game_area[2],diff)
    os.system("mode con cols={col} lines={lines}".format(col=one.width*6, lines=one.height*2+7))
    print(one.show())
    # Game start
    get_input=[0,0]
    while True:
        get_input=one.input_f(get_input[0],get_input[1])
        if get_input[3]==True:
            return
        cursor_coord_set=[get_input[0],get_input[1]]
        area_new=one.first_select(get_input[0],get_input[1],get_input[2])
        print(one.show(get_input[0],get_input[1]))
        if area_new[2]:
                while True:
                    cursor_coord_set=[get_input[0],get_input[1]]
                    get_input=one.input_f(cursor_coord_set[0],cursor_coord_set[1])
                    if get_input[3]==True:
                        return
                    else:
                        area_new=one.select(get_input[0],get_input[1],get_input[2])
                        print(one.show(get_input[0],get_input[1]))

while True:
    repeat=True
    while repeat:
        os.system("cls")
        sys.stdout.write("\033[H")
        print("Welcome to minesweeper.")
        print("Input height between 5 and 30: ")  
        height=input()
        print("Input height between 5 and 30: ")
        width=input()
        print("Input 1 for Easy, 2 for Medium, 3 for expert.")
        diff=input()
        try:
            h=int(height)
            if h>=5 and h<=30:
                repeat=False
            else:
                repeat=False
        except:
            repeat=True
        try:
            w=int(width)
            if  w>=5 and w<=30:
                repeat=False
            else:
                repeat=False
        except:
            repeat=True  
        try:
            diff=int(diff)
            if diff<=3 and diff>=1:
                repeat=False
                if diff==1:
                    d=0.126
                elif diff==2:
                    d=0.181
                elif diff==3:
                    d=0.206
                else:
                    repeat=False
        except:
            repeat=True
    game(h,w,d)


