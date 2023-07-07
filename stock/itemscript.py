file = open("D:\INVENTORY_MANAGER_V2-main\stock\pricelist.csv",'r',encoding='latin-1')
content = file.readlines()
for line in content:
    print("line content:",line)
    values = line.split(',')

    print(float(values[2]))
    print("********\n")
