import Bilibili_Requ
import tkinter
root = tkinter.Tk()
root.geometry("600x450+374+182")
root.title("bilibili视频爬取")
label = tkinter.Label(root, text='视频url:', font=('宋体', 20), fg='red')
label.grid()
entry = tkinter.Entry(root, font=("宋体", 30))
entry.grid(row=0, column=1)
def requ():
    try:
        url = entry.get()
        b = Bilibili_Requ.Bilibili_Requ(url=url)
        requ_str = b.Download()
        text.insert('insert', requ_str)
    except:
        text.insert('insert', '下载失败')
button = tkinter.Button(root, text='开始', font=('宋体', 30), command=requ)
button.grid(row=3, column=1)
text = tkinter.Text(root, font=("宋体", 20), height=5, width=20)
text.grid(row=4, column=1)
root.mainloop()