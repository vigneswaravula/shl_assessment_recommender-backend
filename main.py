from fastapi import FastAPI
from pydantic import BaseModel
from app.recommender import recommend_assessments  # Ensure this function is correctly implemented

app = FastAPI()

# Health check route to verify that the API is working
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Define the input data structure
class RecommendRequest(BaseModel):
    query: str

# POST route to receive the recommendation request and respond with recommendations
@app.post("/recommend")
async def recommend(request: RecommendRequest):
    query = request.query
    try:
        # Call your recommendation function here
        results = recommend_assessments(query)
        # Return recommendations in the response
        return {"recommendations": results}
    except Exception as e:
        # Handle any errors that occur during the recommendation process
        return {"error": str(e)}
