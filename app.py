from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from face_finder import FaceFinder
from PIL import Image
from io import BytesIO
from fastapi.responses import FileResponse

faceFinder = FaceFinder()
app = FastAPI()


class Item(BaseModel):
    item_id: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')


@app.post("/face_find/")
async def find_face(file: UploadFile = File(...)):

     # Check if the uploaded file is an image (you can add more validation as needed)
    if not file.content_type.startswith('image/'):
        return {"message": "Uploaded file is not an image"}

    # Read the contents of the uploaded file
    file_content = await file.read()
    # Create a BytesIO stream from the file content
    image_stream = BytesIO(file_content)

    result = faceFinder.recognise_face(image_stream)
    if result is False:
        return JSONResponse(content={"success": "false"})
    return JSONResponse(content={"success": "True", "person": result})
    # return {"success": result}

@app.post("/face_save/")
async def save_face(file: UploadFile = File(...), name:str = Form(...)):

     # Check if the uploaded file is an image (you can add more validation as needed)
    if not file.content_type.startswith('image/'):
        return {"message": "Uploaded file is not an image"}

    # Read the contents of the uploaded file
    file_content = await file.read()
    # Create a BytesIO stream from the file content
    image_stream = BytesIO(file_content)

    result = faceFinder.save_face(image_stream, name)
    if result is False:
        return JSONResponse(content={"success": "false"})
    return JSONResponse(content={"success": "True", "person": name})
    # return {"success": result}

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/")
async def list_items():
    return [{"item_id": 1, "name": "Foo"}, {"item_id": 2, "name": "Bar"}]


@app.post("/items/")
async def create_item(item: Item):
    return item
