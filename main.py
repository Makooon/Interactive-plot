# Reading an excel file using Python
import sys
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import * #RectangleSelector

dic = {} # store the chip data
dic_color = {}

fig, current_ax = plt.subplots()  # make a new plotting range
axes = plt.axes([0.8, 0.02, 0.15, 0.035])

# Give the location of the file
loc = ("D:\Makon\python\prjs\Interactive select data\data\example_data.xlsx")

### classes ###
class Index(object):
    def push_button(self, event):
        global dic_color
        global dic
        global fig
        print("button is pressed...")
        # delet the selected points which has red color
        for k in dic_color.keys():
            if dic_color[k] == 'red':
                del dic[k]
        dic_color = {k: v for k, v in dic_color.items() if v == 'blue'} # save the points with blue color

        x = list(dic[point][1] for point in dic)
        y = list(dic[point][2] for point in dic)
        print(x)
        print(y)
        coll = current_ax.scatter(x, y, color=["blue"] * len(x), picker=5, s=[30] * len(x))

        print(dir(coll))
        print(coll.get_offsets())
        new_xy = coll.get_offsets()
        new_xy = np.delete(new_xy, 0,0)
        print("new xy is:")
        print(new_xy)
        coll.set_offsets(new_xy)
        fig.canvas.draw_idle()
        plt.pause(1)


        #coll = current_ax.scatter(12, 14, color=["white"], picker=5, s=[30])



        # print(dic_color)
        # print(dic)

def onselect(eclick, erelease):
    "eclick and erelease are matplotlib events at press and release."
    print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
    print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
    print('used button  : ', eclick.button)

    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    if(x1 == x2 and y1 == y2): # select the single poinit
        x_tmp, y_tmp = round(x1), round(y1) # find the likely point
        point = list(p for p in dic if dic[p][1] == x_tmp and dic[p][2] == y_tmp)
        try:
            if dic_color[point[0]] == 'blue':
                dic_color[point[0]] = 'red'
                #coll = current_ax.scatter(dic[point[0]][1], dic[point[0]][2], color=["red"] * 1, picker=5, s=[30] * 1)  # red blue
                print(coll.get_facecolor())
                print(coll.get_offsets())
                of = coll.get_offsets() # get point x,y which has been ploted
                index_x = np.where(of[:,0] == dic[point[0]][1]) # find x row
                index_y = np.where(of[:,1] == dic[point[0]][2])
                print(of)
                print(index_x)
                print(index_y)
                index_use = np.intersect1d(index_x, index_y) # find the special row, index_use is a ndarray
                current_color = coll.get_facecolor()
                current_color[index_use,:] = [1,0,0,1] # change to be red color
                coll.set_color(current_color)
                fig.canvas.draw_idle()
                print(current_color)
                print("index is :")
                print(index_use)
            else:
                dic_color[point[0]] = 'blue'
                current_ax.scatter(dic[point[0]][1], dic[point[0]][2], color=[0, 0, 1, 1], picker=5, s=[30])
        except: # point not excepted
            print("this is not the needed point and it's position is ", x_tmp, y_tmp)
        else:
            print("find the point", point[0], x_tmp, y_tmp)
    else: # select more than one point, like a rectangle
        points = list(p for p in dic if min(x1, x2) < dic[p][1] < max(x1, x2) and min(y1, y2) < dic[p][2] < max(y1, y2))
        # points = list(p for p in all_points if p.x > 0)
        for point in points:
            print(''.join(point), dic[point][1], dic[point][2])
            if dic_color[point] == 'blue':
                dic_color[point] = 'red'
                current_ax.scatter(dic[point][1], dic[point][2], color=["red"]*1, picker = 5, s=[30]*1) # red blue
            else:
                dic_color[point] = 'blue'
                current_ax.scatter(dic[point][1], dic[point][2],color = [0,0,1,1], picker=5, s=[30])

        #print(color_a) # bule : [0. 0. 1. 1.], red : [1,0,0,1]


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print(x1,x2)
    print(y1,y2)

    #if x1 == x2 & y1 == y2:
    #    print("single mouse click...")

    points = list(p for p in dic if min(x1, x2) < dic[p][1] < max(x1, x2) and min(y1, y2) < dic[p][2] < max(y1, y2))
    # points = list(p for p in all_points if p.x > 0)
    for point in points:
        print(''.join(point), dic[point][1], dic[point][2])

def on_pick(event):
    print(event.ind, "clicked")


def toggle_selector(event):
    print(' Key pressed.', event.key)
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

def read_xls_data(data_file): # input a fail path & name
    # To open Workbook
    wb = xlrd.open_workbook(data_file)
    sheet = wb.sheet_by_index(0) # the first sheet
    #dic['head'] = sheet.row_values(0)
    #print(dic['head'])
    for chip in range(1,sheet.nrows):
        dic[sheet.cell_value(chip, 0)] = sheet.row_values(chip)
        print(dic[sheet.cell_value(chip, 0)])
        dic_color[sheet.cell_value(chip, 0)] = 'blue'

def main():
    read_xls_data(loc)
    x = list(dic[point][1] for point in dic)
    y = list(dic[point][2] for point in dic)
    print(x)
    print(y)

    global coll
    coll = current_ax.scatter(x, y, color=["blue"]*len(x), picker = 5, s=[30]*len(x))
    plt.draw()


    #need a button
    bdraw = Button(axes, 'delet')
    callback = Index()
    bdraw.on_clicked(callback.push_button)#

    print("\n      click  -->  release")

    # drawtype is 'box' or 'line' or 'none'
    #toggle_selector.RS = RectangleSelector(current_ax, onselect,
    #                                       drawtype='box', useblit=True,
    #                                       button=[1, 3],  # don't use middle button
    #                                       spancoords='pixels',
    #                                       minspanx=5, minspany=5,
    #                                       interactive=False)
    toggle_selector.RS = RectangleSelector(current_ax, onselect, drawtype='box')

    plt.connect('key_press_event', toggle_selector)

    plt.show()



if __name__ == "__main__":

    main()