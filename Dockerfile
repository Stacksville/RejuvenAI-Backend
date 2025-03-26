FROM python:3.11
RUN useradd -m -u 1000 user
USER user
RUN mkdir -p /home/user/app/.files && chown -R user:user /home/user/app/.files
ENV HOME=/home/user \
  PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY --chown=user . $HOME/app
COPY ./requirements.txt ~/app/requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app","--host","0.0.0.0", "--port", "8000"]
