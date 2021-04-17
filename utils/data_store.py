import csv
import codecs

# def write_to_csv(datalist, header):
#     pass
def write_data(datalist, header, file_name='data.csv'):

    # 指定编码为 utf-8, 避免写 csv 文件出现中文乱码
    with codecs.open(file_name, 'w+', 'utf-8') as csvfile:
        # filednames = ['书名', '页面地址', '图片地址']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for data in datalist:
            print(data)

            try:
                writer.writerow({'书名':data, '页面地址':data, '图片地址': data})
            except UnicodeEncodeError:
                print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

    print('将数据写到 ' + file_name + '成功！')
