from fastapi import FastAPI, HTTPException, Depends
import httpx

app = FastAPI()


async def get_target_base_url():
    # Update with the desired base URL of the target server
    return "http://yts.mx"


@app.get("/proxy")
async def proxy(query: str, target_base_url: str = Depends(get_target_base_url)):
    target_url = f"{target_base_url}{query}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, allow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

        return response.text


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
