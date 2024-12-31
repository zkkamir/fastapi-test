from fastapi import FastAPI

import models
from database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def main():
    print("Hello from todo!")


if __name__ == "__main__":
    main()
