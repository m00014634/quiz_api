from pydantic import BaseModel,validator
import re

# Registration Model
class Register(BaseModel):
    name: str
    phone_number: str

    @validator('phone_number')
    def check_number(cls,phone_number):
        match = re.match(r'\+*998\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}', phone_number)

        if not match:
            raise AttributeError('Wrong formating')


        return  match.group()

m = Register(name='Pavel',phone_number = '998915551782')
print(m)