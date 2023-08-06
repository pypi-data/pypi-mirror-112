# Caldron AI platform

version 0.1.13


## How to run hello world demo
##### 1. pip install dg-ai-platform.
##### 2. Login to Caldron AI platform website.
##### 3. You will see a HelloWorld app with PID and public key.
##### 4. Paste following code to a blank python file and change #pid# to your demo PID.
##### 5. run this python file.
```bash 
from dg_ai_platform.example import HelloWorld
from dg_ai_platform.dg_platform import CaldronAI

ca = CaldronAI(HelloWorld, pid="xxxx", public_key="xxxx")
ca.run()
```
##### 6. Create your task in HelloWorld task page.
##### 7. Your local python process will fetch a task and process it.
##### 8. When the task finished, result will show on the page 

## Run your own App
##### 1. Create a app then setup inputs and outputs on website.
##### 2. Create yourself class must be implementing ITaskProcess(see below code).
```bash
from dg_ai_platform.dg_platform import ITaskProcess

class CustomTask(ITaskProcess):
    def __init__(self):
        super().__init__()

    def inference(self, input_list, output_list, options=None):
        #your logic
        
```
##### 3.You should be let your logic into function inference(self, input_list, output_list, options=None)
* param input_list: all inputs local path in this array. You should be load your all inputs then put it to your model.
* param output_list: all outputs local path in this array. You should be save your outputs to these outputs path.
* param options: This is a json data. 
##### 4. Run your app with CustomTask
```bash 
from your_python_file import CustomTask
from dg_ai_platform.dg_platform import CaldronAI

ca = CaldronAI(CustomTask, pid="xxxx", public_key="xxxx")
ca.run()
```
##### 5. Create your custom task on website.
##### 6. You will see a result on result page.