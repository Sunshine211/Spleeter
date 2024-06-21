

# from typing import Annotated
import os
import shutil
import time
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/music", StaticFiles(directory="./output"), name="static")

@app.post("/uploadai")
async def create_upload_file(file: UploadFile):
    Fname=f"temp-{time.time()}"
    fname=f"{Fname}.{file.filename.split('.')[-1]}"
    
    with open(fname, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    a = os.popen("python -m spleeter separate -o ./output/ -p spleeter:2stems ./"+fname) 
    print(a.read())

    os.remove(fname)
    return {"accompaniment": f'/music/{Fname}/accompaniment.wav',
            "vocals": f'/music/{Fname}/vocals.wav',}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=12222, log_level="info")