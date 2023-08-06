# JSONViewer

The JSONViewer allows Jupyter Notebook users to quickly view JSONs as if they were 
tables. They are able to display images, audio files and even highlight fields 
all in 1 function call. 

## How to install 

You can clone and install the repository using:

```
git clone https://github.com/RelevanceAI/jsonviewer.git
pip install -e jsonviewer/.
```

## How to use

```
from jsonviewer import show_json

docs = [
    {
        "images.image_url": "https://imgs.xkcd.com/comics/voting.png",
        "key": "This is strange",
        "value": "strange"
    },
    {
        "images.image_url": "https://imgs.xkcd.com/comics/animal_songs.png"
    }
]

show_json(
    docs, 
    image_fields=["images.image_url"], # Image fields
    audio_fields=[], # Audio fields,
    text_fields=[], # Text fields
    chunk_image_fields=[],# Images to display in the same row
    highlight_fields={"key": ["value"]}, # Fields to highlight.
    image_width=200, # Adjust the image width
)
```

Note: The fields also support indexing (for example - if you write 'images.image_url.0', it will get the first element of the array if it is there)

![image](example.png)




