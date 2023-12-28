num = int(input("How many characters long password do you want"))
list = [' ','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
count = 0
password = []
while count < num:
    import random
    a = random.randint (0,61)
    char = list[a]
    password.append(char)
    count = count + 1
y = "".join(password)
print (y)
t = 20**num
print ("It would take someone", t , "seconds to hack into your account")
