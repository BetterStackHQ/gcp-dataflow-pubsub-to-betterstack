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
- `BETTER_STACK_INGEST_HOST`: The Better Stack ingest host URL

## Building the Template

1. Clone this repository:
```bash
git clone https://github.com/your-org/gcp-dataflow-pubsub-to-telemetry.git
cd gcp-dataflow-pubsub-to-telemetry
```

2. Build the Docker image:
```bash
docker build -t gcr.io/YOUR_PROJECT/pubsub-to-betterstack .
```

3. Push the image to Google Container Registry:
```bash
docker push gcr.io/YOUR_PROJECT/pubsub-to-betterstack
```

## Deploying the Template

You can deploy the template using the Google Cloud Console or the gcloud CLI:

### Using gcloud CLI

```bash
gcloud dataflow flex-template run "pubsub-to-betterstack-$(date +%Y%m%d-%H%M%S)" \
    --template-file-gcs-location=gs://YOUR_BUCKET/templates/pubsub-to-betterstack.json \
    --parameters input_subscription=projects/YOUR_PROJECT/subscriptions/YOUR_SUBSCRIPTION \
    --region=YOUR_REGION \
    --additional-experiments=use_runner_v2
```

### Using Google Cloud Console

1. Go to the Dataflow section in the Google Cloud Console
2. Click "Create Job from Template"
3. Select "Custom Template"
4. Enter the path to your template in Cloud Storage
5. Fill in the required parameters:
   - `input_subscription`: Your PubSub subscription to read from
6. Set the environment variables:
   - `BETTER_STACK_SOURCE_TOKEN`
   - `BETTER_STACK_INGEST_HOST`
7. Click "Run Job"

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
