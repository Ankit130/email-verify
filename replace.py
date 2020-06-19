with open('emails.txt','r') as f:
    data=f.read()

with open('emails.txt','w') as f:
    data=data.replace('\x92','\x27')
    f.write(data)

with open('companies.txt','r') as f:
    data=f.read()

with open('companies.txt','w') as f:
    data=data.replace('\x92','\x27')
    f.write(data)

