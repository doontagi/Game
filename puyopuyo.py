from tkinter import *
from collections import Counter
from random import choice
import time


class tetris:
    collor=["blue","purple","orange","lightblue"]
    Box_size = 40
    width= Box_size * 8
    height= Box_size * 14

    def __init__(self, _) :
        rows = int(tetris.height / tetris.Box_size)
        columns = int(tetris.width / tetris.Box_size)
        self.MyboxNum = []

        # 외곽선 맵 생성관련 논리
        for a in range(rows) :
            if a == 0 :
                for b in range(columns) :
                    canvas.create_rectangle(b * tetris.Box_size, 0, (b + 1) * tetris.Box_size, tetris.Box_size, fill = "gray", outline = "gray")

            if a == rows -1 :
                for b in range(columns) :
                    canvas.create_rectangle(b * tetris.Box_size, (tetris.Box_size * rows) - tetris.Box_size, (b + 1) * tetris.Box_size, tetris.Box_size * rows, fill = "gray", outline = "gray")

            canvas.create_rectangle(0, a * tetris.Box_size, tetris.Box_size, (a + 1) * tetris.Box_size, fill = "gray", outline = "gray")
            canvas.create_rectangle((columns - 1) * tetris.Box_size, a * tetris.Box_size, columns * tetris.Box_size , (a + 1) * tetris.Box_size, fill = "gray", outline = "gray")

        objBox = self.make_Box()
        self.objbox = objBox       # self.objbox == 현재 움직이고 있는 박스
        self.MyboxNum.append(self.objbox)

    # 박스 생성 이벤트
    def make_Box(self):
        make_box = canvas.create_rectangle(tetris.width / 2, 0, tetris.width / 2 + tetris.Box_size, tetris.Box_size, fill=choice(self.collor))
        return make_box


    # 박스 운지 이벤트
    def fall(self, objBox):
        self.overlap()

        if self.BoxCoords[1] < self.Box_size:
            canvas.move(objBox, 0, tetris.Box_size)

        elif self.can_fall :
            canvas.move(objBox, 0, tetris.Box_size)

        self.overlap()


    # 게임 조작키 이벤트
    def handle_events(self,event):
        self.overlap()

        if self.can_left :   # 오버래핑이 발생한 경우 키입력을 제한
            if event.keysym == "Left":
                canvas.move(self.objbox, -tetris.Box_size, 0)

        if self.can_right :
            if event.keysym == "Right":
                canvas.move(self.objbox, tetris.Box_size, 0)

        self.overlap()


    # 오버래핑 관련 함수
    def overlap(self):
        self.BoxCoords = canvas.coords(self.objbox)   # Boxcoords == [x1,y1,x2,y2]  / 현재 박스 좌표값 List
        if self.objbox != "Recreate" :
            overlap = [
                       canvas.find_overlapping(self.BoxCoords[0], self.BoxCoords[1] + 1, self.BoxCoords[0], self.BoxCoords[3] - 1),  # 왼쪽 선
                       canvas.find_overlapping(self.BoxCoords[2], self.BoxCoords[1] + 1, self.BoxCoords[2], self.BoxCoords[3] - 1),  # 오른쪽 선
                       canvas.find_overlapping(self.BoxCoords[0] + 1, self.BoxCoords[3], self.BoxCoords[2] - 1 , self.BoxCoords[3])  # 밑면 선
                      ]


            if len(overlap[0]) <= 1 :
                self.can_left = True
            else :
                self.can_left = False

            if len(overlap[1]) <= 1 :
                self.can_right = True
            else :
                self.can_right = False

            if len(overlap[2]) <= 1 :
                self.can_fall = True
            else :
                self.can_fall = False

    # Mr.노 함수
    def NMH(self) :
        for _ in self.MyboxNum :
            BoxCoords = canvas.coords(_)
            overlap = canvas.find_overlapping(BoxCoords[0] + 1, BoxCoords[3], BoxCoords[2] - 1 , BoxCoords[3])  # MyboxNum 리스트에 등록된 상자들의 밑면선 오버랩을 실시

            while len(overlap) == 1 :
                canvas.move(str(_), 0, tetris.Box_size)
                BoxCoords = canvas.coords(_)
                overlap = canvas.find_overlapping(BoxCoords[0] + 1, BoxCoords[3], BoxCoords[2] - 1 , BoxCoords[3])


    # 게임 메인 루프
    def timer(self):
        if self.objbox == "Recreate" :
            self.objbox = self.make_Box()
            self.MyboxNum.append(self.objbox)       # 추가되는 상자번호 MyboxNum 리스트에 등록

        self.fall(self.objbox)

        if self.can_fall == False  :
            if self.popping(self.objbox):
                self.NMH()
            #if(self.BoxCoords[1]==tetris.Box_size):
                #print("Game over")
                #return 0

            self.objbox = "Recreate"
        print(self.MyboxNum)
        canvas.after(300,self.timer)



    def find_samecolor(self,a,samecolor,aleadyseen):
        if a in aleadyseen:
            return samecolor
        color = canvas.itemcget(a, "fill")
        coords = canvas.coords(a)
        lap=canvas.find_overlapping(coords[0],(coords[1]+coords[3])/2,coords[2],(coords[1]+coords[3])/2)
        lap2=canvas.find_overlapping((coords[0]+coords[2])/2,coords[1],(coords[0]+coords[2])/2,coords[3])
        lap=lap+lap2
        for i in lap:
            if(color==canvas.itemcget(i, "fill")):
                samecolor.add(i)
        aleadyseen.add(a)
        temp=set([])
        for i in samecolor:
            temp.add(i)
        for i in temp:
            samecolor=self.find_samecolor(i,samecolor,aleadyseen)
        return samecolor


    def popping(self,a):
        samecolor=set([])
        aleadyseen=set([])
        A=self.find_samecolor(a,samecolor,aleadyseen)

        if(int(len(A))>2):
            for i in A:
                color = canvas.itemcget(i, "fill")
                canvas.delete(i)
                self.MyboxNum.remove(i)   # 삭제된 상자번호MyboxNum 리스트에서 제거
            return True
        return False



doon=Tk()
doon.title("한울")
status_var = StringVar()
status_var.set("Level: -, Score: -")
status = Label(doon,
        textvariable=status_var,
        font=("Helvetica", 10, "bold"))
status.pack()

canvas = Canvas(doon, width = tetris.width, height = tetris.height)
canvas.pack()

bb=tetris(canvas)
doon.bind("<Key>", bb.handle_events)

bb.timer()
doon.mainloop()
