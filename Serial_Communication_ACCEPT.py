# -*- coding: utf-8 -*

"""GUI模块"""
import tkinter
import tkinter.ttk as ttk
"""串口操作模块"""
import serial
import serial.tools.list_ports
"""多线程操作"""
from multiprocessing import Process, Queue


def Serial_Communication_Control_GUI(queue_to_control, queue_comname, queue_baud, queue_databits, queue_oddeven, queue_stopbits):
    """线程调用1函数 GUI界面（懒得面向对象，改天改成面向对象）"""

    
    def open_serial(index):
        if index:
            queue_to_control.put('2')
        else:
            plist = serial.tools.list_ports.comports()
            if len(plist) != 0:
                queue_to_control.put('1')
                plist = list(plist[0])[0]
                print(plist, 'is available.')
                boxchoice['value'] = plist
                boxchoice.current(0)
                queue_comname.put(plist)
                queue_baud.put(box_choice_baud_value.get())
                queue_databits.put(box_choice_data_value.get())
                queue_oddeven.put(box_choice_oddeven_value.get())
                queue_stopbits.put(box_choice_stop_value.get())
            else:
                print('No serial to open.')


    root = tkinter.Tk()
    root.title("Serial Communication")
    #root.geometry('500x300')

    label_com_name = tkinter.Label(root, text='Available COM name:')
    label_com_name.grid(row=0, column=0)

    label_baud = tkinter.Label(root, text='Baud:')
    label_baud.grid(row=1, column=0)

    label_data = tkinter.Label(root, text='Data bits:')
    label_data.grid(row=2, column=0)

    label_oddeven = tkinter.Label(root, text='Odd/Even:')
    label_oddeven.grid(row=3, column=0)

    label_stop = tkinter.Label(root, text='Stop bit:')
    label_stop.grid(row=4, column=0)

    box_choice_value = tkinter.StringVar()
    boxchoice = ttk.Combobox(root, textvariable=box_choice_value, state='readonly')
    boxchoice['value'] = ('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6')
    boxchoice.current(0)
    boxchoice.bind('<<ComboboxSelected>>')
    boxchoice.grid(row=0, column=1, sticky='W')

    box_choice_baud_value = tkinter.StringVar()
    box_baud = ttk.Combobox(root, textvariable=box_choice_baud_value, state='readonly')
    box_baud['value'] = (100, 300, 600,1200,2400,4800,9600,14400,19200,38400,56000,57600,15200,128000,256000)
    box_baud.current(6)
    box_baud.bind('<<ComboboxSelected>>')
    box_baud.grid(row=1, column=1, sticky='w')

    box_choice_data_value = tkinter.StringVar()
    box_data = ttk.Combobox(root, textvariable=box_choice_data_value)
    box_data['value'] = (5, 6, 7, 8)
    box_data.current(3)
    box_data.bind('<<ComcoboxSelected>>')
    box_data.grid(row=2, column=1, sticky='w')

    box_choice_oddeven_value = tkinter.StringVar()
    box_oddeven = ttk.Combobox(root, textvariable=box_choice_oddeven_value)
    box_oddeven['value'] = ('NONE', 'EVEN', 'ODD', 'MARK','SPACE')
    box_oddeven.current(0)
    box_oddeven.bind('<<ComcoboxSelected>>')
    box_oddeven.grid(row=3, column=1, sticky='w')

    box_choice_stop_value = tkinter.StringVar()
    box_stop = ttk.Combobox(root, textvariable=box_choice_stop_value)
    box_stop['value'] = (1, 1.5, 2)
    box_stop.current(0)
    box_stop.bind('<<ComcoboxSelected>>')
    box_stop.grid(row=4, column=1, sticky='w')

    button_open_serial = tkinter.Button(root, text='Open Serial', command=lambda: open_serial(0))
    button_open_serial.grid(row=5, column=0, sticky='w')

    button_stop_serial = tkinter.Button(root, text='Close Serial', command=lambda: open_serial(1))
    button_stop_serial.grid(row=5, column=1, sticky='w')

    root.mainloop()


def Serial_Communication_off_on(queue_GUI_to_display, queue_comname, queue_baud, queue_databits, queue_oddeven, queue_stopbits):
    while True:
        while True:
            if queue_GUI_to_display.get(True) == '1':
                break
        parity_ch = [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK, serial.PARITY_SPACE]
        parity_chi = ('NONE', 'EVEN', 'ODD', 'MARK','SPACE')
        k = 0
        com_name = queue_comname.get()
        baud = int(queue_baud.get())
        data_bits = int(queue_databits.get())
        odd_even = queue_oddeven.get()
        stop_bits = float(queue_stopbits.get()) 
        while 1:
            if odd_even == parity_chi[k]:
                break
            else:
                k += 1   
        ser = serial.Serial(com_name, baud, timeout=0.5)
        ser.bytesize = data_bits
        ser.stopbits = stop_bits
        ser.parity = parity_ch[k]

        while True:
            s = ser.read(55).decode('utf-8')
            if s != '':
                print(s)
            queue_GUI_to_display.put('1')
            if queue_GUI_to_display.get() == '2':
                ser.close()
                # while True:
                #     try:
                #         self.Queue.get(timeout=1)
                #     except Queue.Empty:
                #         break
                #     except:
                #         raise
                queue_GUI_to_display.get(True)
                break


if __name__ == '__main__':
    queue_GUI_to_display = Queue()
    queue_GUI_to_display.put('0')
    queue_comname = Queue()
    queue_baud = Queue()
    queue_databits = Queue()
    queue_oddeven = Queue()
    queue_stopbits = Queue()

    p_GUI = Process(target=Serial_Communication_Control_GUI, args=(queue_GUI_to_display, queue_comname, queue_baud, queue_databits, queue_oddeven, queue_stopbits))
    p_serial = Process(target=Serial_Communication_off_on, args=(queue_GUI_to_display, queue_comname, queue_baud, queue_databits, queue_oddeven, queue_stopbits))

    p_GUI.start()
    p_serial.start()
    p_GUI.join()
    p_serial.terminate()
    print('The end')
