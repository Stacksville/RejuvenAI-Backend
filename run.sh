#!/bin/sh

export OPENAI_API_KEY=''
export GEMINI_API_KEY=''
export DEEPSEEK_API_KEY=''

export JWT_PUBLIC_KEY=''
export JWT_PRIVATE_KEY=''

export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''

export DATASET=MOCK

uvicorn app:app --reload
