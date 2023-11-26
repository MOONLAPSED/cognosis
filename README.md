# cognosis ©MIT License

Application in this repository is developed using the [`FastStream`](https://github.com/airtai/faststream) framework. Below, you'll find a guide on how to get started, develop new features or bug fixes, and ensure the quality of your code through testing and linting, run the [`FastStream`](https://github.com/airtai/faststream) application locally, and view [`AsyncAPI`](https://www.asyncapi.com/) documentation.

## Getting Started

To set up your development environment, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/MOONLAPSED/cognosis.git
   cd cognosis
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   ```

## Running FastStream Application Locally

To run the [`FastStream`](https://github.com/airtai/faststream) application locally, follow these steps:

1. Start the Kafka Docker container locally using the provided script:

2. Start the [`FastStream`](https://github.com/airtai/faststream) application with the following command:

3. You can now send messages to the Kafka and can test the application. Optionally, if you want to view messages in it, you can subscribe to it using the provided script:

   ```bash
   ./scripts/start_kafka_broker_locally.sh
   faststream run cognosis.application:app --workers 1
   ./scripts/subscribe_to_kafka_broker_locally.sh <topic_name>
   ```
4. To stop the [`FastStream`](https://github.com/airtai/faststream) application, press `Ctrl+C`.

5. Finally, stop the Kafka Docker container by running the script:
   ```
   ./scripts/stop_kafka_broker_locally.sh
   ```

## Code Linting

```bash
./scripts/lint.sh
```

## Static Analysis

```bash
./scripts/static-analysis.sh
```

## Viewing AsyncAPI Documentation

[`FastStream`](https://github.com/airtai/faststream) framework supports [`AsyncAPI`](https://www.asyncapi.com/) documentation. To ensure that your changes are reflected in the [`AsyncAPI`](https://www.asyncapi.com/) documentation, follow these steps:

1. Run the following command to view the [`AsyncAPI`](https://www.asyncapi.com/) documentation:

   ```bash
   faststream docs serve cognosis.application:app
   ```

   This command builds the [`AsyncAPI`](https://www.asyncapi.com/) specification file, generates [`AsyncAPI`](https://www.asyncapi.com/) documentation based on the specification, and serves it at `localhost:8000`.

2. Open your web browser and navigate to <http://localhost:8000> to view the [`AsyncAPI`](https://www.asyncapi.com/) documentation reflecting your changes.

3. To stop the [`AsyncAPI`](https://www.asyncapi.com/) documentation server, press `Ctrl+C`.


## Continuous Integration (CI)

This repository is equipped with GitHub Actions that automate static analysis and pytest in the CI pipeline. Even if you forget to perform any of the required steps, CI will catch any issues before merging your changes. This repository has three workflows, each triggered when code is pushed:

1. **Tests Workflow**: This workflow is named "Tests" and consists of two jobs. The first job runs static analysis tools [`mypy`](https://mypy.readthedocs.io/en/stable/) and [`bandit`](https://bandit.readthedocs.io/en/latest/) to identify potential issues in the codebase. The second job runs tests using [`pytest`](https://pytest.org/) to ensure the functionality of the application. Both jobs run simultaneously to expedite the `CI` process.

2. **Build Docker Image Workflow**: This workflow is named "Build Docker Image" and has one job. In this job, a [`Docker`](https://www.docker.com/) image is built based on the provided Dockerfile. The built image is then pushed to the [**GitHub Container Registry**](https://ghcr.io), making it available for deployment or other purposes.

3. **Deploy FastStream AsyncAPI Docs Workflow**: The final workflow is named "Deploy FastStream AsyncAPI Docs" and also consists of a single job. In this job, the [`AsyncAPI`](https://www.asyncapi.com/) documentation is built from the specification, and the resulting documentation is deployed to [**GitHub Pages**](https://pages.github.com/). This allows for easy access and sharing of the [`AsyncAPI`](https://www.asyncapi.com/) documentation with the project's stakeholders.

## Building and Testing Docker Image Locally

If you'd like to build and test the [`Docker`](https://www.docker.com/) image locally, follow these steps:

1. Run the provided script to build the [`Docker`](https://www.docker.com/) image locally. Use the following command:

2. Before starting the [`Docker`](https://www.docker.com/) container, ensure that a Kafka [`Docker`](https://www.docker.com/) container is running locally. You can start it using the provided script:

3. Once Kafka is up and running, you can start the local [`Docker`](https://www.docker.com/) container using the following command:

   * `--rm`: This flag removes the container once it stops running, ensuring that it doesn't clutter your system with unused containers.

   * `--name faststream-app`: Assigns a name to the running container, in this case, "faststream-app".

   * `--net=host`: This flag allows the [`Docker`](https://www.docker.com/) container to share the host's network namespace.


   This script will build the [`Docker`](https://www.docker.com/) image locally with the same name as the one built in `CI`.

   ```bash
   ./scripts/build_docker.sh
   ./scripts/start_kafka_broker_locally.sh
   docker run --rm --name faststream-app --net=host cognosis:latest

4. To stop the local [`Docker`](https://www.docker.com/) container, simply press `Ctrl+C` in your terminal.

5. Finally, stop the Kafka [`Docker`](https://www.docker.com/) container by running the provided script:

   ```bash
   ./scripts/stop_kafka_broker_locally.sh
   ```

### cognosis ©MIT License - MOONLAPSED@gmail.com ~ github.com/MOONLAPSED