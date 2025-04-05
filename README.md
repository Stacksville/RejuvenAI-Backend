# RejuvenAI-Backend

## Install

1. Build a container image:

```bash 
docker build -t rejuvenai .
```

2. Add a `.env` file with secrets (see [example_env](./example_env))
3. Run the image:

```bash
docker run -it -p 8000:8000 rejuvenai
```

### Debug Model Setup

Script: `app.py` </br>
Root: `RejuvenAI-Backend`

### FastAPI

### Endpoints:

Chat: http://127.0.0.1:8000/chat/</br>
Backend: http://127.0.0.1:8000/docs/

### Setup

1. Pull latest `main`
2. Install requirements (in environment as optional) `pip install -r requirements.txt`
3. Set environment variables (see example_env)
4. Run: `uvicorn app:app --reload`
5. See Docs at: `app-endpoint/docs`
6. See chainlit: `app-endpoint/chat`

### DB Setup

1. Install postgresql: `sudo apt install postgresql`
    1. See: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04
2. Setup database
    ```database
    CREATE DATABASE chainlit_db;
    CREATE USER chainlit_user WITH ENCRYPTED PASSWORD 'password@1234';
    GRANT ALL PRIVILEGES ON DATABASE chainlit_db TO chainlit_user;
    ```
