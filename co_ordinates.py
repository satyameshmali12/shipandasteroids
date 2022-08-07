# creating the co_ordinates list

try:
    noofrotation = 360
    # initial speed
    x = 0
    y = -8
    # difference to make
    dtm = 0.08
    xychangeable = True
    co_ordinates = []
    for i in range(noofrotation):
        if i > 0 and i <90 or i == 0:
            co_ordinates.append([x,y])
            x+=-dtm
            y+=dtm
        
        if i>90 and i<180 or i == 90:
            if xychangeable:
                x = -8
                y = 0
                xychangeable = False
            co_ordinates.append([x,y])
            x+=dtm
            y+=dtm
            if i==180:
                xychangeable = True
        
        if i>180 and i<270 or i == 180:
            if xychangeable:
                x = 0 
                y = 8
                xychangeable = False
            
            co_ordinates.append([x,y])
            x+=dtm
            y-=dtm
            if i == 269:
                xychangeable = True
        
        if i>270 and i<360 or i==270:
            if xychangeable:
                x = 8
                y = 0
                xychangeable = False
            co_ordinates.append([x,y])
            x-=dtm
            y-=dtm
except Exception as e:
    print("Hey some error occurred! 🟠")