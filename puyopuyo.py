from tkinter import *
from collections import Counter
from random import choice
import time


class tetris:
    collor=["blue","purple"]
    Box_size = 40
    width= Box_size * 8
    height= Box_size * 14

    def __init__(self, _) :
        rows = int(tetris.height / tetris.Box_size)
        columns = int(tetris.width / tetris.Box_size)
        self.MyboxNum = []
        self.changed_boxNum = []
        self.chain_trigger = []

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

        objBox2= self.make_Box2()
        self.objbox2=objBox2
        self.MyboxNum.append(self.objbox2)


    # 박스 생성 이벤트
    def make_Box(self):
        make_box = canvas.create_rectangle(tetris.width / 2, 0, tetris.width / 2 + tetris.Box_size, tetris.Box_size, fill=choice(self.collor))
        return make_box
    def make_Box2(self):
        make_box = canvas.create_rectangle(tetris.width / 2 + tetris.Box_size, 0, tetris.width / 2 + tetris.Box_size*2, tetris.Box_size, fill=choice(self.collor))
        return make_box


    # 박스 fall 이벤트
    def fall(self, objBox):
        self.overlap()

        if self.BoxCoords[1] < self.Box_size:
            canvas.move(objBox, 0, tetris.Box_size)

        elif self.can_fall :
            canvas.move(objBox, 0, tetris.Box_size)

        self.overlap()
    def fall2(self, objBox):
        self.overlap2()

        if self.BoxCoords2[1] < self.Box_size:
            canvas.move(objBox, 0, tetris.Box_size)

        elif self.can_fall2 :
            canvas.move(objBox, 0, tetris.Box_size)

        self.overlap2()




    # 게임 조작키 이벤트
    def handle_events(self,event):
        self.overlap()
        self.overlap2()

        if self.can_left:   # 오버래핑이 발생한 경우 키입력을 제한
            if event.keysym == "Left":
                canvas.move(self.objbox, -tetris.Box_size, 0)
            if event.keysym == "Left":
                canvas.move(self.objbox2, -tetris.Box_size, 0)



        if self.can_right2:
            if event.keysym == "Right":
                canvas.move(self.objbox, tetris.Box_size, 0)
            if event.keysym == "Right":
                canvas.move(self.objbox2, tetris.Box_size, 0)

        self.overlap()
        self.overlap2()


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
    def overlap2(self):
        self.BoxCoords2 = canvas.coords(self.objbox2)   # Boxcoords == [x1,y1,x2,y2]  / 현재 박스 좌표값 List
        if self.objbox2 != "Recreate" :
            overlap = [
                       canvas.find_overlapping(self.BoxCoords2[0], self.BoxCoords2[1] + 1, self.BoxCoords2[0], self.BoxCoords2[3] - 1),  # 왼쪽 선
                       canvas.find_overlapping(self.BoxCoords2[2], self.BoxCoords2[1] + 1, self.BoxCoords2[2], self.BoxCoords2[3] - 1),  # 오른쪽 선
                       canvas.find_overlapping(self.BoxCoords2[0] + 1, self.BoxCoords2[3], self.BoxCoords2[2] - 1 , self.BoxCoords2[3])  # 밑면 선
                      ]


            if len(overlap[0]) <= 1 :
                self.can_left2 = True
            else :
                self.can_left2 = False

            if len(overlap[1]) <= 1 :
                self.can_right2 = True
            else :
                self.can_right2 = False

            if len(overlap[2]) <= 1 :
                self.can_fall2 = True
            else :
                self.can_fall2 = False


    # 연쇄 제거 함수
    def gravity(self) :                # MyboxNum = 박혀있는 상자  / changed_boxNum = 위치가 변경된 상자
        self.changed_boxNum = []   # gravity함수 시작전 gravity를 체험한 상자들의 값들을 초기화

        for _ in self.MyboxNum :
            BoxCoords = canvas.coords(_)
            overlap = canvas.find_overlapping(BoxCoords[0] + 1, BoxCoords[3], BoxCoords[2] - 1 , BoxCoords[3])  # MyboxNum 리스트에 등록된 상자들의 밑면선 오버랩을 실시
            if len(overlap) == 1 :        # 위치가 변경될 상자를 change_boxNum에 담음
                self.changed_boxNum.append(_)
                list(set(self.changed_boxNum))

            while len(overlap) == 1 :     # 위치를 변경 시킴
                canvas.move(str(_), 0, tetris.Box_size)
                BoxCoords = canvas.coords(_)
                overlap = canvas.find_overlapping(BoxCoords[0] + 1, BoxCoords[3], BoxCoords[2] - 1 , BoxCoords[3])


    # 게임 메인 루프
    def timer(self):
        if self.objbox == "Recreate" :
            self.objbox = self.make_Box()
            self.MyboxNum.append(self.objbox)       # 추가되는 상자번호 MyboxNum 리스트에 등록
            self.objbox2 = self.make_Box2()
            self.MyboxNum.append(self.objbox2)

        self.fall(self.objbox)
        self.fall2(self.objbox2)

        if self.can_fall == False and self.can_fall2 ==False  :
            if self.popping(self.objbox) or self.popping(self.objbox2):
                self.gravity()
                for a in self.changed_boxNum :               # 1번이라도 위치가 변경된 모든 상자들을 popping
                    if self.popping(a) :                 # 위치 변경 후 또 한번 popping이 일어난 경우
                        self.chain_trigger.append("ON")  # 점수 계산용 아직 미구현
                        for b in list(self.removeNum) :  # popping을 해야할 목록에 있었으나(changed_boxNum2) 순서가 오기전 pop되버려서 상자가 삭제될경우, 다음 popping 목록에 들어가지 않도록 제거하는 과정
                            if b in self.changed_boxNum :
                                self.changed_boxNum.remove(b)
                self.gravity()

                while "ON" in self.chain_trigger :
                    self.chain_trigger = []
                    for a in self.changed_boxNum :
                        if self.popping(a) :
                            self.chain_trigger.append("ON")
                            for b in list(self.removeNum) :
                                if b in self.changed_boxNum :
                                    self.changed_boxNum.remove(b)
                self.gravity()


                #if(self.BoxCoords[1]==tetris.Box_size):
                    #print("Game over")
                    #return 0
            self.objbox = "Recreate"
            self.objbox2 = "Recreate"

        canvas.after(100,self.timer)



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
        self.removeNum=self.find_samecolor(a,samecolor,aleadyseen)

        if(int(len(self.removeNum)) > 2) :
            for i in self.removeNum :
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
