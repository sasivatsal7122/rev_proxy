from fastapi import FastAPI, HTTPException, Depends
import httpx

app = FastAPI()

async def get_target_base_url():
    return "https://yts.mx"

@app.get("/proxy")
async def proxy(query: str, target_base_url: str = Depends(get_target_base_url)):
    target_url = f"{target_base_url}{query}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        if "/torrent/" in query:
            return response
        return response.json()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
