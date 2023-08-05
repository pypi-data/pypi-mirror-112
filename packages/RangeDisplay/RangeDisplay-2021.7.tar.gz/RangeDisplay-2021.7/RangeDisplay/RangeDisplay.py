from tkinter import *
from tkinter.ttk import *
from math import sin,cos,pi


class RangeDisplay(Frame):
    bgColor="#f3ffed"
    bdColor="#000000"
    fgColor="#2ef245"
    bdSize=1

    def __init__(self,master,Height, Width, padX=6, padY=6, radiusO=20, bdSize=2, bgColor="#f3ffed", bdColor="#000000", fgColor="#2ef245", xsf=0.5, xef=0.8, ysf=0.2, yef=0.6, radiusI=20):
        RangeDisplay.bgColor=bgColor
        RangeDisplay.bdColor=bdColor
        RangeDisplay.fgColor=fgColor
        RangeDisplay.bdSize=bdSize
        if xsf<0 or xsf>1 or xef<0 or xef>1 or ysf<0 or ysf>1 or yef<0 or yef>1:
            raise Exception("Fractions should be between 0 and 1")
        Frame.__init__(self, master, height = Height+padY, width = Width+padX)
        self.xsf=xsf
        self.xef=xef
        self.ysf=ysf
        self.yef=yef
        self.master=master
        self.canv_H=Height
        self.canv_W=Width
        self.radiusO=radiusO
        if radiusO>50:
            self.radiusO=50
        if radiusO<0:
            self.radiusO=0
        self.radiusI=radiusI
        self.padY=padY
        self.padX=padX
        self.canv = Canvas(self, height = self.canv_H+padY, width = self.canv_W+padX)
        self.canv.pack(side=TOP)
        self.base=self.__draw_base(self.padX/2.0,
                                    self.padY/2.0,
                                    self.canv_W+self.padX/2.0,
                                    self.canv_H+self.padY/2.0,
                                    min(self.canv_W,self.canv_H)* self.radiusO/100,
                                    fill=RangeDisplay.bgColor,outline=RangeDisplay.bdColor,width=RangeDisplay.bdSize)
        
        self.over=self.__draw_selection(self.padX/2.0+self.canv_W*self.xsf,
                                    self.padY/2.0+self.canv_H*self.ysf,
                                    self.canv_W*self.xef+self.padX/2.0,
                                    self.canv_H*self.yef+self.padY/2.0,
                                    min(self.canv_W*(self.xef-self.xsf),self.canv_H*(self.yef-self.ysf))* self.radiusI/100,
                                    fill=RangeDisplay.fgColor,outline=RangeDisplay.bdColor,width=RangeDisplay.bdSize)

    def __draw_base(self,x1, y1, x2, y2, feather, res=50,**kwargs):
        points = []
        min_angle=(pi/2)/res
        # top side
        points += [x1 + feather, y1,
                   x2 - feather, y1]
        # top right corner
        for i in range(res):
            points += [x2 - feather + sin(min_angle*i) * feather,
                       y1 + feather - cos(min_angle*i) * feather]
        # right side
        points += [x2, y1 + feather,
                   x2, y2 - feather]
        # bottom right corner
        for i in range(res):
            points += [x2 - feather + cos(min_angle*i) * feather,
                       y2 - feather + sin(min_angle*i) * feather]
        # bottom side
        points += [x2 - feather, y2,
                   x1 + feather, y2]
        # bottom left corner
        for i in range(res):
            points += [x1 + feather - sin(min_angle*i) * feather,
                       y2 - feather + cos(min_angle*i) * feather]
        # left side
        points += [x1, y2 - feather,
                   x1, y1 + feather]
        # top left corner
        for i in range(res):
            points += [x1 + feather - cos(min_angle*i) * feather,
                       y1 + feather - sin(min_angle*i) * feather]
            
        return self.canv.create_polygon(points, **kwargs)

    def __draw_selection(self,x1, y1, x2, y2, feather, res=50,**kwargs):
        sbox=self.__draw_base(x1, y1, x2, y2, feather, res,**kwargs)
        #up line
        slineX=self.canv.create_line(self.padX/2.0,
                                    self.padY/2.0+self.canv_H*self.ysf,
                                    self.padX/2.0+self.canv_W,
                                    self.padY/2.0+self.canv_H*self.ysf,
                                    dash=(5,5),width=self.bdSize, fill=self.bdColor)

        #down line
        elineX=self.canv.create_line(self.padX/2.0,
                                    self.padY/2.0+self.canv_H*self.yef,
                                    self.padX/2.0+self.canv_W,
                                    self.padY/2.0+self.canv_H*self.yef,
                                    dash=(5,5),width=self.bdSize, fill=self.bdColor)

        #left line
        slineY=self.canv.create_line(self.padX/2.0+self.canv_W*self.xsf,
                                    self.padY/2.0,
                                    self.padX/2.0+self.canv_W*self.xsf,
                                    self.padY/2.0+self.canv_H,
                                    dash=(5,5),width=self.bdSize, fill=self.bdColor)

        #right line
        elineY=self.canv.create_line(self.padX/2.0+self.canv_W*self.xef,
                                    self.padY/2.0,
                                    self.padX/2.0+self.canv_W*self.xef,
                                    self.padY/2.0+self.canv_H,
                                    dash=(5,5),width=self.bdSize, fill=self.bdColor)

        return [sbox,slineX,elineX,slineY,elineY]

    def update(self,xsf,xef,ysf,yef):
        if xsf<0 or xsf>1 or xef<0 or xef>1 or ysf<0 or ysf>1 or yef<0 or yef>1:
            raise Exception("Fractions should be between 0 and 1")
        for i in self.over:
            self.canv.delete(i)
        self.xsf=min(xsf,xef)
        self.xef=max(xef,xef)
        self.ysf=min(ysf,yef)
        self.yef=max(yef,ysf)

        self.over=self.__draw_selection(self.padX/2.0+self.canv_W*self.xsf,
                                    self.padY/2.0+self.canv_H*self.ysf,
                                    self.canv_W*self.xef+self.padX/2.0,
                                    self.canv_H*self.yef+self.padY/2.0,
                                    min(self.canv_W*abs(self.xef-self.xsf),self.canv_H*abs(self.yef-self.ysf))* self.radiusI/100,
                                    fill=RangeDisplay.fgColor,outline=RangeDisplay.bdColor,width=RangeDisplay.bdSize)
