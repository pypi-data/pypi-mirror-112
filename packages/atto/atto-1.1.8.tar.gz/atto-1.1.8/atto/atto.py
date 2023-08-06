#!/usr/bin/env python3.9	
import curses			
import cursor				
import curses.ascii
import os
import sys
__version__='1.1.5'
def wrap(s,res=[[]],name='<buffer>',bc='<unknown>'):
    cursor.hide()
    s.clear()
    ixx=0
    upperl=0
    sy=0
    
    shres=res[:os.get_terminal_size().lines-1]
    for a in range(len(shres),os.get_terminal_size().lines):
            s.addch(a,0,'~',curses.color_pair(2))

    for line in shres:
            s.addstr(ixx,0,''.join(line))
            ixx+=1

    x=0
    lastx=0

    y=0
    nf=False
    if res==[[]]:
        nf=True
    oldres=res[:]
    if nf:
        s.addstr(os.get_terminal_size().lines-1,0,'"{}" (new file)'.format(name))
    else:
        s.addstr(os.get_terminal_size().lines-1,0,'"{}" ({} lines, {} bytes)'.format(name,len(res),bc))
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    curses.init_pair(2,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.mousemask(-1)
    insert=False
        

    while True:
        try:
            curch=shres[sy][x]
        except IndexError:
            curch=' '
        s.addch(sy+x//(os.get_terminal_size().columns),x%(os.get_terminal_size().columns),curch,curses.color_pair(1)|curses.A_VERTICAL)
        try:
            a=s.getch()
        except:
            s.delch()
            continue
        s.delch()
        s.keypad(1)
        
        if curses.ascii.isprint(a):
            if insert:
                if a==27:
                    insert=False
                else:
                    res[y].insert(x,chr(a))
                    x+=1
                    lastx+=1
            else:
                if chr(a)=='i':
                    insert=True
        else:
            if a in [curses.KEY_ENTER,ord('\n')] and insert:
                br=res[y]
                res[y]=br[:x]
                res.insert(y+1,br[x:])
                if sy<os.get_terminal_size().lines-2 and y<len(res):
                    sy+=1
                else:
                    upperl+=1
                    
                    
                y+=1
                x=0 
                sx=0
                lastx=0    
            elif a in [curses.KEY_BACKSPACE,127] and insert :
                if x==0 and y>0:
                    if not res[y]:
                        del res[y]
                        a=''
                    else:
                        a=res[y]
                        del res[y]
                    if y>0:
                        y-=1
                    if sy>0:
                        sy-=1
                    
                    x=len(res[y])
                    sx=len(res[y])
                    lastx=len(res[y])
                    res[y]+=a

                elif res[y]:
                    del res[y][x-1]
                    x-=1
                    lastx-=1
            elif a==curses.KEY_F10:
                return '\n'.join([''.join(i) for i in res])+'\n'
            
            elif a==curses.KEY_LEFT:
                if x>0:
                    x-=1
                    lastx-=1
               
            elif a==curses.KEY_RIGHT:
                if x<len(shres[sy]):
                    x+=1
                    lastx+=1
            elif a==curses.KEY_MOUSE:
                state=curses.getmouse()[4]
                bot=os.get_terminal_size().lines+upperl-1
        
                shres=res[upperl:bot]

                if state==curses.BUTTON4_PRESSED:
                    if upperl>0:
                        upperl-=1
                        if sy==len(shres) and y<0:
                            y-=1
                        if sy<len(shres):
                            sy+=1
                        try:
                            x=len(res[y])
                            if x>lastx:
                                x=lastx
                        except IndexError:
                            x=0

                        
                if state==curses.BUTTON2_PRESSED or state==2097152:
                    if sy>0:
                            sy-=1

                    if upperl<len(res)-1:
                        upperl+=1
                    
                        if sy==0 and y<len(res)-1:
                            y+=1
                        try:
                            x=len(res[y])
                            if x>lastx:
                                x=lastx
                        except IndexError:
                            x=0
                

            elif a==curses.KEY_DOWN:
                
                if sy<len(shres)-1:
                    sy+=1
                elif y<len(res)-1:
                    upperl+=1
                if y<len(res)-1:
                    y+=1
                try:
                    x=len(res[y])
                    if x>lastx:
                        x=lastx
                except IndexError:
                    x=0
            elif a==curses.KEY_UP:
                if sy>0:
                    sy-=1
                elif y>0:
                    upperl-=1
                if y>0:
                    y-=1
                try:
                    x=len(res[y])
                    if x>lastx:
                        x=lastx
                except IndexError:
                    x=0

            elif a==curses.KEY_NPAGE:
                if sy<len(shres)-5:
                    sy+=5
                elif y<len(res)-5:
                    upperl+=5
                if y<len(res)-5:
                    y+=5
                x=len(res[y])
            elif a==curses.KEY_PPAGE:
                if sy>5:
                    sy-=5
                elif y>5:
                    upperl-=5
                if y>5:
                    y-=5
                x=len(res[y])
            elif a==9:
                for a in range(4):
                    res[y].insert(x,' ')
                    x+=1
            elif a==curses.KEY_F2:
                open(name,'w').write('\n'.join([''.join(i) for i in res])+'\n')
                s.clear()
                s.addstr(os.get_terminal_size().lines-1,0,'"'+name+'"'+"({} lines, {} bytes) written)".format(len(res),bc))
                s.addstr(0,0,'\n'.join([''.join(i) for i in shres]))

                continue
            elif a==curses.KEY_F4:
                return '\n'.join([''.join(i) for i in oldres])+'\n'
            elif a==27:
                insert=False
            




        s.clear()
        l=len(res)+1-os.get_terminal_size().lines
        try:
            pc=round((upperl/l)*100)
            if pc>100:
                pc=100
        except ZeroDivisionError:
            pc=0
        tq=int(pc*0.75)*"#"+(75-int(pc*0.75))*"-"
        msg='['+tq+']'
        xy='{},{}'.format(y,x)
        bot=os.get_terminal_size().lines+upperl-1
        
        shres=res[upperl:bot]
        s.addstr(0,0,'\n'.join([''.join(i) for i in shres]))
        s.addstr(os.get_terminal_size().lines-1,round(os.get_terminal_size().columns/3.5),msg,curses.A_BOLD)
        s.addstr( os.get_terminal_size().lines-1,round(os.get_terminal_size().columns/3.5)-(len(str(pc))+3)-1,"({}%)".format(pc),curses.A_STANDOUT)
        s.addstr( os.get_terminal_size().lines-1,round(os.get_terminal_size().columns/3.5)-(len(str(pc))+3)-len(xy)-2,xy)
        ols=0
        if insert:
            s.addstr(os.get_terminal_size().lines-1,0,'-- INSERT --',curses.A_BOLD)
        for jd in shres:
            ols+=len(jd)//os.get_terminal_size().columns
        for a in range(len(shres)+ols,os.get_terminal_size().lines-1):
            s.addch(a,0,'~',curses.color_pair(2))
def edit(q=None):
    if q is None:
        if '--version' in sys.argv:
                print(__version__)
                sys.exit()

        if len(sys.argv)<2:
                print("not enough args",file=sys.stderr)
                sys.exit(1)
        q=sys.argv[-1]
        
    if os.path.exists(q):
        res=[list(a) for a in open(q).read().replace('\t','    ').splitlines()]
        bc=os.stat(q).st_size
    else:
        res=[[]]
        bc=0
    fs=curses.wrapper(wrap,res=res,bc=bc,name=q)
    open(q,'w').write(fs.replace('    ','\t'))
    cursor.show()

