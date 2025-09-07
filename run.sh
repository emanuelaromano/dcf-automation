#!/bin/bash

if [ "$1" == "-b" ]; then
    cd backend
    uvicorn main:app --reload
elif [ "$1" == "-f" ]; then
    cd frontend
    npm run dev
elif [ "$1" == "-g" ]; then
    git add .
    git commit -m "update"
    git push
else
    echo "Usage: ./run.sh -b (backend) or -f (frontend) or -g (git)"
    exit 1
fi
