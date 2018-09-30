import xlwings as xw
import os


def test_unit():
    #连接到excel
    app=xw.App(visible=True,add_book=False)
    if os.path.exists('./path\\myexcel.xlsx') and 0:
        wb=app.books.add()
        wb.save('./path\\myexcel.xlsx')
    workbook = app.books.add()
    #wb.save('./path\\myexcel.xlsx')
    #workbook = app.books.open('./path\\myexcel.xlsx')#连接excel文件
    #连接到指定单元格
    data_range = workbook.sheets('Sheet1')
    #写入数据
    data_range[0,0].value = [1,2,3,4,5,67]

    '''
        for i in range(20):
        for j in range(20):
            data_range[i,j].value = ('%d,'%j) +'%d'%i
    '''

    #保存
    workbook.save()
    #workbook.close()
    #app.quit()

def write_y(filename,result):
    if not os.path.exists('./data\\'+filename):
        os.makedirs('./data\\'+filename)
    filename = './data\\'+filename+'\\'+filename+'.xlsx'
    app = xw.App(visible=True, add_book=False)
    if not os.path.exists(filename):
        workbook=app.books.add()
        workbook.save(filename)
    else:
        workbook = app.books.open(filename)#连接excel文件
    data_range = workbook.sheets('Sheet1')
    colunm = 0
    for i in result:
        data_range[colunm, 0].value = result[i]
        colunm += 1
    # 写入数据
    workbook.save(filename)
    workbook.close()
    app.quit()

def write_pro_y(filename,result):
    if not os.path.exists('./data\\'+filename):
        os.makedirs('./data\\'+filename)
    filename = './data\\'+filename+'\\'+filename+'.xlsx'
    app = xw.App(visible=True, add_book=False)
    if not os.path.exists(filename):
        workbook=app.books.add()
        workbook.save(filename)
    else:
        workbook = app.books.open(filename)#连接excel文件
    data_range = workbook.sheets('Sheet1')
    colunm = 0
    for i in result:
        each_reuslt = result[i].get()
        for each_list in each_reuslt:
            data_range[colunm, 0].value = each_reuslt[each_list]
            colunm += 1
    # 写入数据
    workbook.save(filename)
    workbook.close()
    app.quit()

def read_avg_y(filename, read_range):
    filename = './data\\' + filename + '\\' + filename + '.xlsx'
    app = xw.App(visible=False, add_book=False)
    workbook = app.books.open(filename)
    data_range = workbook.sheets('Sheet1').range(read_range)
    return_list = data_range.value
    app.quit()
    return return_list

def write_by_pickle(X,Y,LogXI,LogYI):
    a= 1

if __name__ == '__main__':
    #write_y('007',2,[1,2,3,4,5,68])
    a = 1
