import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8070, reload=True)




# https://www.kaggle.com/competitions/competitive-data-science-predict-future-sales/data