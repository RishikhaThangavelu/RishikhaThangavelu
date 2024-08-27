from fastapi import FastAPI, File, UploadFile
import requests
import json
#file validation
#try except

app = FastAPI()

receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'
item_list = []

@app.post("/upload/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"data/{uploaded_file.filename}" #get location to store uploaded image
    with open(file_location, "wb+") as file_object: 
        file_object.write(await uploaded_file.read()) #save the image

    with open(file_location, "rb") as file_object:
        r = requests.post(receiptOcrEndpoint, data={
            'client_id': 'TEST',
            'recognizer': 'auto',
            'ref_no': 'ocr_python_123',
        }, files={"file": file_object})
        
        data = json.loads(r.text) #the receipt info as text

        if 'receipts' in data and len(data['receipts']) > 0 and 'items' in data['receipts'][0]:
            items = data['receipts'][0]['items']
            for item in items:
                item_list.append(item['description']) #ge tthe product name 
    #print(item_list)
    return {"item_list": item_list}