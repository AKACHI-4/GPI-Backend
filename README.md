# To activate virtual environment

- For Windows

```md
    .\venv\Scripts\activate
```

- For Mac

```md
    source venv/bin/activate
```

## To Run Flask Server

```md
    python app.py
```

## To run on waitress-server

```md
    waitress-serve --host=0.0.0.0 --port=8080 main:app
```
