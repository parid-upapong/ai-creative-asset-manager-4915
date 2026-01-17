import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from models.tagging_engine import AutoTagger

app = FastAPI(title="CreatorNexus AI - CV Tagging Service")

# Initialize the model on startup
tagger = AutoTagger()

@app.get("/health")
async def health_check():
    return {"status": "active", "model": "clip-vit-base-patch32"}

@app.post("/v1/predict/tags")
async def predict_tags(file: UploadFile = File(...)):
    """
    Endpoint for CreatorNexus core backend to request auto-tagging.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Load image from stream
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Run inference
        tags = tagger.generate_tags(image)
        embeddings = tagger.get_image_features(image)
        
        return {
            "filename": file.filename,
            "suggested_tags": tags,
            "vector_embedding_preview": embeddings[0][:5], # Send partial for validation
            "metadata_version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)