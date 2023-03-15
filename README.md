# Beating Heart of Art

## Description

This project involves the analysis of artworks from the API of the Metropolitan Museum of Art using CNNs and mapping the results on the world map to visualize the circulation of artistic styles across continents and centuries.

## Docker build instructions
### Step 1. Build our Image for Container Registry (locally)
  docker build -t $GCR_MULTI_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME .

### Step 2. Run Image (locally)
  docker run -e PORT=8000 -p 8080:8000 $GCR_MULTI_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME
Note: In the above command, -e PORT = 8000 defines the $PORT variable

👉 Let's verify that everything is OK on http://localhost:8080/
As I understand it, 8080 is the default port that GCR uses

### Step 3. Push our Image to Container Registry
  docker push $GCR_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME
$GCR_REGION = eu.gcr.io
$GCP_PROJECT_ID is the ID of your Google console project
$DOCKER_IMAGE_NAME is the name of the folder that would created in Google Container Registry. Pick one that makes sense to you.

### Step 4. Deploy our Image on Container Registry to Cloud Run
  gcloud run deploy --image $GCR_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME --region $GCP_REGION
The GCP region specified by --region is optional. If this is not provided, you will be
prompted to pick one from a list.
