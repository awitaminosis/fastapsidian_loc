from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from os import listdir
from os.path import isfile, join

app = FastAPI()


@app.get("/")
@app.get("/items/")
def list_items():
    only_files = [f for f in listdir('./vault/') if isfile(join('./vault/', f))]
    html_content = '<html><body>'
    for f in only_files:
        html_content += f'<a href="/items/{f}/">{f}</a></br>'
    html_content += '</body></html>'
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/items/{item}")
def list_item(item: str):
    with open('./vault/'+item, 'r') as f:
        file = f.read()

    html_response = '<form method="get" action="/mds/">'
    html_response += f'<input type="hidden" id="folder" name="folder" value={item.replace('.md', '')}>'
    html_response += '<textarea id="tex" name="tex" style="width:95%;height:95%">'
    html_response += file
    html_response += '</textarea>'
    html_response += '</form>'
    html_response += '<span style="background-color:gray;padding:10px;cursor:pointer;border-radius:30%" id="submit" onclick="fetch(\'/mds/?folder=\' + folder.value + \'&tex=\'+tex.value);location.reload()">submit</span>'

    html_response += ''
    return HTMLResponse(content=html_response, status_code=200)


@app.get("/mds/")
def write_item(folder: Union[str, None] = None, tex: Union[str, None] = None):
    if folder and tex:
        with open('./vault/' + folder + '.md', 'w') as f:
            f.write(tex)
        return 'added'
    else:
        return 'missing'
