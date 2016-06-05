# -*- coding: cp1251 -*-

from ants_alg import *
import wx

graph = new_graph()
count = 0
steps = 0
mode = 0 ## add nodes

class Link(wx.Panel):
        def __init__(self, parent):
                wx.Panel.__init__(self, parent)
                self.params = wx.BoxSizer(wx.HORIZONTAL)
                self.with_text = wx.StaticText(self, label='With: ')
                self.linked_node = wx.TextCtrl(self)
                self.length_text =  wx.StaticText(self, label='Length: ')
                self.length = wx.TextCtrl(self)
                self.delete_button = wx.Button(self, wx.NewId(), "Delete")
                self.params.AddMany([(self.with_text, 1), (self.linked_node, 1),\
                                     (self.length_text, 1), (self.length, 2), \
                                     (self.delete_button, 2, wx.EXPAND)])
                self.SetSizer(self.params)
                self.Show(True)

        def get_link_id(self):
                print(int(self.linked_node.GetValue()))
                return int(self.linked_node.GetValue())
        def get_link_length(self):
                print(int(self.length.GetValue()))
                return int(self.length.GetValue())

class Links_window(wx.Frame):
	def __init__(self, parent, node_id):
                self.node_id = node_id
                self.n_id = "Links for node %d" % node_id
        	wx.Frame.__init__(self, parent, -1, self.n_id, size=(300, 100))
	        self.Bind(wx.EVT_CLOSE, self.onClose)
                
                self.AddBind_button = wx.Button(self, wx.NewId(), "Add new link")
                self.list_links = wx.BoxSizer(wx.VERTICAL)
                self.links = []

                self.Bind(wx.EVT_BUTTON, self.addLink, self.AddBind_button)
                self.Ok_button = wx.Button(self, wx.NewId(), "Ok")
                self.Bind(wx.EVT_BUTTON, self.OnSet, self.Ok_button)

                self.list_links.AddMany([(self.AddBind_button, 1, wx.EXPAND),\
                                         (self.Ok_button, 1, wx.EXPAND) ])

                self.SetSizer(self.list_links)

	def onClose(self, evt):
		self.Show(False)
        def Destroy(self):
		pass
        def addLink(self, evt):
                new_field = Link(self)
                self.links.append(new_field)
                self.list_links.Insert(1, new_field, 1, wx.EXPAND)
                self.list_links.Layout()
                size = self.GetSize()
                self.SetSize((size[0], size[1] + 40))
        def OnSet(self, evt):
                global graph
                for link in self.links:
	                add_nodes_link(graph, self.node_id, link.get_link_id(), \
                                       link.get_link_length(), 1)
                print(graph)
                self.GetParent().InitBuffer()
                dc = wx.BufferedDC(wx.ClientDC(self.GetParent()), self.GetParent().buffer)
                

class SketchWindow(wx.Window):
    def __init__(self, parent, ID, field_size):

        wx.Window.__init__(self, parent, ID, size=field_size)
        self.SetBackgroundColour("White")
        self.color = "blue"
        self.thickness = 2
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID) # (1) Создание объекта wx.Pen
        self.nodes = []
        self.result = ()
        self.beg_pos = ()
        self.end_pos = ()                                  
        self.InitBuffer()                                   
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)            # (2) Присоединение событий
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.Bind(wx.EVT_LEFT_DCLICK, self.OnDCClick)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKbd)

    def OnKbd(self, event):
        keycode = event.GetKeyCode()
        print("ok")
        if keycode == wx.WXK_DELETE:
            for i in self.nodes:
                if i[2] == 1:
                    self.nodes.pop(self.nodes.index(i))

    def OnRightClick(self, event):
	global graph
        pos = event.GetPositionTuple()
        for i in self.nodes:
            if pow(pos[0] - i[0], 2) + pow(pos[1] - i[1], 2) <= pow(15, 2):
                if i[2] == 1:
                    isSelected = 0
                    self.nodes[self.nodes.index(i)] = (i[0], i[1], isSelected, i[3], i[4])
                    i[4].Show(False)
                else:
                    isSelected = 1
                    if i[4] == None:
                        links = Links_window(self, i[3])
                        self.nodes[self.nodes.index(i)] = (i[0], i[1], isSelected, i[3], links)
                    else:
                        links = i[4]
                        self.nodes[self.nodes.index(i)] = (i[0], i[1], isSelected, i[3], links)
                    links.Show(True)
		

                print(self.nodes)
                self.InitBuffer()
                dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		
		

    def InitBuffer(self):                                       # (3) Создание контекста устройства с буферизацией 
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))  # (4) Использование контекста устройства
        dc.Clear()
        self.DrawScene(dc)
        self.reInitBuffer = False                                  

    def OnLeftDown(self, event):
        self.beg_pos = event.GetPositionTuple()
        self.CaptureMouse()
        print(self.beg_pos)
	return

    def OnLeftUp(self, event):
	global graph, count
        if not self.HasCapture():
            self.pos = event.GetPositionTuple()                     # (5) Получение позиции мыши
            self.nodes.append((self.pos[0], self.pos[1], 0, count, None))
            add_node(count, graph)
            print(graph)
            count = count + 1
            self.InitBuffer()
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        else:
           self.ReleaseMouse()

    def OnMotion(self, event):                         
        if event.LeftIsDown():
            self.end_pos = self.GetPositionTuple()
            print(self.end_pos)
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)  # (9) Создание другого контекста с буферизацией
            self.drawMotion(dc, event)
        event.Skip()                                   
                                                      
    def drawMotion(self, dc, event):                            # (10) Рисование в контексте устройства 
        if mode == 1:
            print(self.beg_pos, self.end_pos)
            dc.DrawLine(self.beg_pos[0], self.beg_pos[1], self.end_pos[0], self.end_pos[1])
        else:
            pass

    def OnSize(self, event):                                   # (11) Обработка события изменения размера
	self.reInitBuffer = True
 
    def OnIdle(self, event):                                   # (12) Обработка простоя
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)

    def del_elems(self):

        global graph

	for i in self.nodes:
            if i[2] == 1:
                del_index = self.nodes.index(i)
                self.nodes.pop(del_index)
                rm_node(del_index, graph)
                self.del_elems()
        self.InitBuffer()
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
 

    def OnPaint(self, event):                                  # (13) Обработка запроса на прорисовку
       return#dc = wx.BufferedPaintDC(self, self.buffer)

    def DrawScene(self, dc):                                 # (14) Рисование всех линий
        for node in self.nodes:
            if node[2] == 1:
                self.color = "red"
            else:
                self.color = "blue"
            pen = wx.Pen(self.color, self.thickness, wx.SOLID)
            dc.SetPen(pen)
            dc.DrawCircle(node[0], node[1], 15)
            dc.DrawText(str(node[3]), node[0] - 8, node[1] - 8)
           
            self.DrawLinks(dc)

    def DrawLinks(self, dc):
        global graph
        beg = ()
        end = ()
        is_path = []
        for node in graph:
            for n in self.nodes:
                if node == n[3]:
                    beg = (n[0], n[1])
                    node1 = node
            for link in graph[node]:
               for n in self.nodes:
                   if link == n[3]:
                       end = (n[0], n[1])
                       node2 = link
                       if beg != () and end != ():
                           if self.GetParent().result != (): 
                              is_path = self.GetParent().result[0]
                           if is_path != [] and node1 in is_path and node2 in is_path:
                               pen = wx.Pen("red", 4, wx.SOLID)
                           else:
                               pen = wx.Pen("black", self.thickness, wx.SOLID)
                           dc.SetPen(pen)
                           dc.DrawLine(beg[0], beg[1], end[0], end[1])

class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Ants",
            size=(900,600))
        self.result = ()
        self.tools_elements = wx.BoxSizer(wx.HORIZONTAL)
        self.all_elements = wx.BoxSizer(wx.VERTICAL)

        self.Modes_button = wx.Button(self, wx.NewId(), "New nodes mode")
        self.Bind(wx.EVT_BUTTON, self.OnModesClick, self.Modes_button)
        self.Text_ants = wx.StaticText(self, label='Count of ants: ')
        self.Ctrl_ants = wx.TextCtrl(self)
        self.Text_time = wx.StaticText(self, label='Steps: ')
        self.Ctrl_time = wx.TextCtrl(self)
        self.Delete_button = wx.Button(self, wx.NewId(), "Delete selected nodes")
        self.Bind(wx.EVT_BUTTON, self.OnDel, self.Delete_button)
        self.Exit_button = wx.Button(self, wx.NewId(), "Exit")
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.Exit_button)
        self.Run_button = wx.Button(self, wx.NewId(), "Run")
        self.Bind(wx.EVT_BUTTON, self.OnRun, self.Run_button)

        self.tools_elements.AddMany([(self.Modes_button, wx.EXPAND), self.Text_ants, \
                                self.Ctrl_ants, \
                                self.Text_time, self.Ctrl_time, self.Run_button,  \
                                self.Delete_button, \
                                (self.Exit_button, wx.EXPAND)])
        
        self.targets = wx.BoxSizer(wx.HORIZONTAL)
        self.Text_start = wx.StaticText(self, label='Starts with: ')
        self.Ctrl_start = wx.TextCtrl(self)
        self.Text_target = wx.StaticText(self, label='Target: ')
        self.Ctrl_target = wx.TextCtrl(self)
        self.CleanAll = wx.Button(self, wx.NewId(), "Clean All")
        self.Bind(wx.EVT_BUTTON, self.OnCleanAll, self.CleanAll)
        self.targets.AddMany([self.Text_start, self.Ctrl_start, \
                              self.Text_target, self.Ctrl_target, \
                              self.CleanAll])        

        self.sketch = SketchWindow(self, -1, (800, 600))

        self.all_elements.AddMany([(self.tools_elements,1, wx.EXPAND), \
                                   (self.targets, 1, wx.EXPAND), \
                                   (self.sketch, 9, wx.EXPAND)])
        self.SetSizer(self.all_elements)

    def OnCleanAll(self, evt):
        global graph, count
        count = 0
        graph = clean_graph(graph)
        self.sketch.nodes = []
        self.sketch.result = ()
        self.result = ()
        self.sketch.InitBuffer()
        wx.BufferedDC(wx.ClientDC(self.sketch), self.sketch.buffer)

    def OnDel(self, event):
        self.sketch.del_elems()

    def OnModesClick(self, event):
        global mode
        if mode == 0:
            mode = 1
            self.Modes_button.SetLabel("Bind mode")
        else:
            mode = 0
            self.Modes_button.SetLabel("New nodes mode")

    def OnExit(self, event):
        self.Close()

    def OnRun(self, event):
        #print("run!")
        global graph
        set_ant_pheromone(10.0)
        set_al_be_params(0.1, 0.2)
        set_evaporate(0.2)
        cnt = int(self.Ctrl_ants.GetValue())
        steps = int(self.Ctrl_time.GetValue())
        beg = int(self.Ctrl_start.GetValue())
        target = int(self.Ctrl_target.GetValue())
        self.result = do_ants_alg(cnt, steps, graph, beg, target)
        self.sketch.InitBuffer()
        wx.BufferedDC(wx.ClientDC(self.sketch), self.sketch.buffer)
        print(self.result)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = SketchFrame(None)
    frame.Show(True)
    app.MainLoop()
