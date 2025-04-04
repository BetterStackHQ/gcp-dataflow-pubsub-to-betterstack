# GCP Dataflow PubSub to Better Stack

A Google Cloud Dataflow Flex template that reads messages from PubSub and sends them to Better Stack.

## Overview

This template provides a scalable solution for streaming data from Google Cloud PubSub to Better Stack. It uses Apache Beam's Python SDK and can be deployed as a Dataflow Flex template.

## Prerequisites

- Google Cloud Platform account with Dataflow and PubSub enabled
- Better Stack account with a source token
- Docker installed (for building the template)
- Google Cloud SDK installed

## Environment Variables

The template requires two environment variables:

- `BETTER_STACK_SOURCE_TOKEN`: Your Better Stack source token
- `BETTER_STACK_INGESTING_HOST`: The Better Stack ingest host URL

## Building and Deploying the Template

1. Clone this repository:
```bash
git clone https://github.com/your-org/gcp-dataflow-pubsub-to-telemetry.git
cd gcp-dataflow-pubsub-to-telemetry
```

2. Choose Google Cloud Platform project to use
```bash
# See currently selected project
gcloud config get-value project
# You can switch to a different project using
gcloud projects list
gcloud config set project PROJECT_ID
```

3. Build the Docker image:
```bash
docker build -t gcr.io/$(gcloud config get-value project)/pubsub-to-betterstack .
```

4. Push the image to Google Container Registry:
```bash
gcloud auth configure-docker
docker push gcr.io/$(gcloud config get-value project)/pubsub-to-betterstack
```

5. Create a Cloud Storage bucket for the template (if you don't have one):
```bash
BUCKET_NAME="dataflow-templates-$(gcloud config get-value project)"
gsutil mb -l us-central1 gs://${BUCKET_NAME}
```

6. Update the template specification with your project ID:
```bash
sed -i "s/PROJECT_ID/$(gcloud config get-value project)/g" pubsub-to-betterstack.json
```

7. Upload the template specification to Cloud Storage:
```bash
gsutil cp pubsub-to-betterstack.json gs://${BUCKET_NAME}/templates/
```

8. Deploy the template using gcloud CLI:
```bash
gcloud dataflow flex-template run "pubsub-to-betterstack-$(date +%Y%m%d-%H%M%S)" \
    --template-file-gcs-location=gs://${BUCKET_NAME}/templates/pubsub-to-betterstack.json \
    --parameters input_subscription=projects/$(gcloud config get-value project)/subscriptions/YOUR_SUBSCRIPTION \
    --parameters better_stack_source_token=YOUR_SOURCE_TOKEN \
    --parameters better_stack_ingesting_host=YOUR_INGESTING_HOST \
    --region=$(gcloud config get-value compute/region) \
    --additional-experiments=use_runner_v2
```

### Using Google Cloud Console

1. Go to the Dataflow section in the Google Cloud Console
2. Click "Create Job from Template"
3. Select "Custom Template"
4. Enter the path to your template in Cloud Storage: `gs://${BUCKET_NAME}/templates/pubsub-to-betterstack.json`
5. Fill in the required parameters:
   - `input_subscription`: Your PubSub subscription to read from
   - `better_stack_source_token`: Your Better Stack source token
   - `better_stack_ingesting_host`: The Better Stack ingest host URL
6. Click "Run Job"

## Message Format

The template expects messages in JSON format. Each message will be sent to Better Stack as-is. For example:

```json
{
  "message": "Hello from PubSub",
  "timestamp": "2024-02-11T12:00:00Z",
  "severity": "INFO"
}
```

## Error Handling

The template includes error handling that:
- Logs errors but continues processing
- Retries failed requests to Better Stack
- Maintains message ordering

## License

ISC License. See [LICENSE.md](LICENSE.md) for details.
