import os 
from pathlib import Path 
import logging

#Tạo cấu trúc folder nhanh gọn


logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:') #notifi log


#__init__.py nằm ở thư mục src -> src là package -> from src import helper.py (Trc python 3.3 thì cần)

list_of_files = [
    "src/__init__.py",
    "src/helper.py", #Có chức năng nhập , xuất thông tin , huggingface
    "src/prompt.py", #Viết promt điều khiển hệ thống
    ".env",
    "setup.py",  
    "app.py",
    "research/trials.ipynb", 
   " test.py"
]


for filepath in list_of_files:
    filepath = Path(filepath) #Path sẽ đưa đc đg dẫn cho windows , linux ,mac...  -> kiểu đường dẫn tuyệt đối
    filedir , filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Đang tạo thư mục:{filedir} với các file: {filename}")

    if (not os.path.exists(filepath) or (os.path.getsize(filepath)==0)):
        with open(filepath , "w") as f:
            pass
            logging.info(f'Đang tạo file {filename}')

    else:
        logging.info(f"{filename} đã tồn tại" )

    
