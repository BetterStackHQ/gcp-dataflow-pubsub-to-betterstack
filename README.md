# Google Cloud Pub/Sub to Better Stack

A Dataflow Flex template that reads messages from Pub/Sub and sends them to Better Stack Telemetry.

## Building and Deploying the Template

1. Clone this repository:
```bash
git clone https://github.com/your-org/gcp-dataflow-pubsub-to-betterstack.git
cd gcp-dataflow-pubsub-to-betterstack
```

2. Choose Google Cloud Platform project to use
```bash
# See currently selected project
gcloud config get-value project
# You can switch to a different project using
gcloud projects list
gcloud config set project PROJECT_ID
```

3. Choose Google Cloud Platform region to use
```bash
# See currently selected region
gcloud config get-value compute/region
# You can switch to a different region using
gcloud app regions list
gcloud config set compute/region PROJECT_ID
```

4. Create a Cloud Storage bucket for the template (if you don't have one):
```bash
BUCKET_NAME="dataflow-templates-$(gcloud config get-value project)"
gsutil mb -l $(gcloud config get-value compute/region) gs://${BUCKET_NAME}
```

5. Set parameters based on your Google Cloud Pub/Sub Subscription and Better Stack Telemetry source
```bash
INPUT_SUBSCRIPTION=projects/$(gcloud config get-value project)/subscriptions/<your-pubsub-subscription-name>
SOURCE_TOKEN=<your-better-stack-source-token>
INGESTING_HOST=<your-better-stack-ingesting-host>
```

6. Build, deploy and run the template
```bash
gcloud builds submit --tag "gcr.io/$(gcloud config get-value project)/pubsub-to-betterstack" .
gcloud dataflow flex-template build gs://$BUCKET_NAME/pubsub-to-betterstack.json \
    --image "gcr.io/$(gcloud config get-value project)/pubsub-to-betterstack" \
    --sdk-language "PYTHON" \
    --metadata-file "metadata.json"
gcloud dataflow flex-template run "pubsub-to-betterstack-$(date +%Y%m%d-%H%M%S)" \
    --template-file-gcs-location=gs://$BUCKET_NAME/pubsub-to-betterstack.json \
    --parameters input_subscription=$INPUT_SUBSCRIPTION \
    --parameters better_stack_source_token=$SOURCE_TOKEN \
    --parameters better_stack_ingesting_host=$INGESTING_HOST \
    --region=$(gcloud config get-value compute/region)
```

## Optional parameters

The template supports the following optional parameters:

- `batch_size`: Number of messages to batch before sending to Better Stack. Default: 100
- `window_size`: Window size in seconds for batching messages. Default: 10

You can include these parameters in your Dataflow job by adding them to the run command, e.g. `gcloud dataflow flex-template run ... --parameters window_size=30`.

## License

ISC License. See [LICENSE.md](LICENSE.md) for details.
