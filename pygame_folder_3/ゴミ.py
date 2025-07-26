max_number=100
number=2
warukazu=2
while True:
    if(number>max_number):
        break
    if(number==warukazu):
        print(number,"は素数です")
        number+=1
        warukazu=2
    elif(number%warukazu==0):
        print(number,"は素数ではない")
        number+=1
        warukazu=2
    else:
        warukazu+=1