class Dog():
    name="i am a dog"
    age = '12'


tim=Dog()

somelist=['name','age']
x=somelist[0]
print(getattr(tim, x))