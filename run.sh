#!/bin/bash

if [ "$1" == "-b" ]; then
    cd backend
    uvicorn main:app --reload
elif [ "$1" == "-f" ]; then
    cd frontend
    npm run dev
else
    echo "Usage: ./run.sh -b (backend) or -f (frontend)"
    exit 1
fi
