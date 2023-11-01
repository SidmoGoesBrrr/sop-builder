import razorpay
client = razorpay.Client(auth=("YOUR_ID", "rzp_live_fm0FMMJvVyz1dV"))

data = {
    "amount": 99,
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "generate new sop",
        "key2": "value2"
    }
}
client.order.create(data=data)
