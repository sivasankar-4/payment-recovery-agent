from pydantic import BaseModel
 

class Customer(BaseModel):
    name : str
    email : str

class PaymentEvent(BaseModel):
    event_id : str
    payment_id : str
    status : str
    failure_reason : str
    amount : float
    customer : Customer

