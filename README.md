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
```
