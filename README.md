# Number Guesser - A DevOps Project

This repository contains a simple yet feature-rich "Guess the Number" web application. It serves as a comprehensive example of a full DevOps lifecycle, including containerization with Docker and CI/CD automation with both GitHub Actions and Jenkins.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running with Docker](#running-with-docker)
- [CI/CD Pipelines](#cicd-pipelines)
  - [GitHub Actions](#github-actions)
  - [Jenkins](#jenkins)
- [Codebase Structure](#codebase-structure)

## Project Overview

The application challenges players to guess a randomly generated number within a certain range and number of attempts. It includes multiple difficulty levels and a persistent leaderboard to track top scores.

The primary goal of this project is to demonstrate a modern software development workflow, from coding to automated deployment.

## Features

- **Multiple Difficulty Levels**: Easy, Medium, and Hard, each with different number ranges and attempt limits.
- **Persistent Leaderboard**: Saves the top 10 scores in a `leaderboard.json` file.
- **Guess History**: Shows the player their previous guesses during the current game.
- **Hints**: Provides a hint (even or odd) after three guesses.
- **Responsive UI**: Clean and simple interface that provides clear feedback.

## Technology Stack

- **Backend**: Python with Flask
- **Containerization**: Docker
- **CI/CD**: GitHub Actions, Jenkins

## Getting Started

You can run this application locally using Docker.

### Prerequisites

- [Docker](https://www.docker.com/get-started) must be installed on your machine.

### Running with Docker

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>/game
    ```

2.  **Build the Docker image:**
    From the `game` directory, run the following command. This will build the image using the provided `dockerfile`.
    ```bash
    docker build -t number-guesser .
    ```

3.  **Run the Docker container:**
    This command starts the application and maps your local port 5000 to the container's port 5000.
    ```bash
    docker run -p 5000:5000 number-guesser
    ```

4.  **Access the application:**
    Open your web browser and navigate to **http://localhost:5000**.

## CI/CD Pipelines

This project includes two distinct CI/CD pipelines to demonstrate different automation approaches.

### GitHub Actions

The workflow is defined in `.github/workflows/dockerhub-deployment.yml`.

- **Trigger**: Automatically runs on every push to the `master` branch.
- **Workflow**:
    1.  **Build**: Builds the Docker image.
    2.  **Test**: Runs the container and sends a test request to ensure the application is working.
    3.  **Push**: If the test is successful, it pushes the Docker image to Docker Hub.

### Jenkins

A `jenkinsfile` is provided in the `CICD` directory for use with a Jenkins server.

- **Stages**:
    - **Build**: Builds the Docker image.
    - **Test**: A placeholder for running automated tests.
    - **Deploy**: A placeholder for deployment steps.

## Codebase Structure

```
game/
├── .github/
│   └── workflows/
│       └── dockerhub-deployment.yml  # GitHub Actions workflow
├── CICD/
│   └── jenkinsfile                   # Jenkins pipeline definition
├── templates/
│   ├── index.html                    # Main game page
│   └── leaderboard.html              # Leaderboard display
├── app.py                            # Core Flask application logic
├── dockerfile                        # Docker build instructions
├── leaderboard.json                  # Stores top scores
└── requirements.txt                  # Python dependencies
```
