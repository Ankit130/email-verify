with open('emails.csv','r') as f:
    data=f.read()

with open('emails.csv','w') as f:
    data=data.replace('\x92','\x27')
    f.write(data)

with open('companies.csv','r') as f:
    data=f.read()

with open('companies.csv','w') as f:
    data=data.replace('\x92','\x27')
    f.write(data)

