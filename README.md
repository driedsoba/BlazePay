# BlazePay

We are implementing an e-wallet payment system with a robust 3-tier architecture featuring React, Flask, Stripe and Firebase.

# Blazepay - Payment Application Documentation

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contribution](#contribution)
- [License](#license)

## Introduction

Blazepay is a modern and secure payment application designed to simplify financial transactions. It allows users to send and receive payments, split bills, and manage multi-currency transactions. Blazepay integrates with Stripe for secure payment processing and utilizes a React frontend, Flask backend, and Firestore database for seamless communication and data storage.

## Features

Blazepay offers the following key features:

1. **Multi-Currency Support**: Users can perform transactions in multiple currencies, making it suitable for international transactions.

2. **Peer-to-Peer (P2P) Transactions**: Users can send money to their contacts securely through the app.

3. **Group Transactions**: Users can split bills and expenses with friends or colleagues, making group payments hassle-free.

4. **Stripe Payment Integration**: Blazepay integrates with Stripe's payment gateway for safe and secure payment processing.

5. **Top-Up Functionality**: Users can easily top up their Blazepay account using Stripe API.

## Technology Stack

Blazepay utilizes the following technology stack:

- **Frontend**: React
- **Backend**: Flask
- **Database**: Firestore
- **Payment Integration**: Stripe

## Getting Started

### Prerequisites

Before setting up Blazepay, ensure you have the following prerequisites installed:

- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)
- [Firestore](https://firebase.google.com/docs/firestore)
- [Stripe API Keys](https://stripe.com/docs/api)


## API Documentation
### Authentication

The API uses JSON Web Tokens (JWT) for authentication. To access protected routes, include a valid JWT token in the request headers.

### Base URL

The base URL for the API is `http://localhost:8000`.

### Endpoints

#### 1. Get Data

- **Endpoint:** `/data`
- **Method:** `POST`
- **Description:** Retrieve user data.
- **Authentication:** JWT required.
- **Request Body:** None
- **Response:**
  - Success (200 OK):
    ```json
    {
      "message": "PIN matches, data returned",
      "user_data": {
        // User data fields
      }
    }
    ```
  - Error (500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 2. Get Profile

- **Endpoint:** `/profile`
- **Method:** `POST`
- **Description:** Retrieve user profile data.
- **Authentication:** JWT required.
- **Request Body:**
  - `phone` (string): User phone number
  - `pin` (string): User PIN
- **Response:**
  - Success (200 OK):
    ```json
    {
      "message": "PIN matches, data returned",
      "user_data": {
        // User data fields (excluding PIN and salt)
      },
      "access_token": "JWT access token"
    }
    ```
  - Error (500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 3. Create Transaction (P2P)

- **Endpoint:** `/payment`
- **Method:** `POST`
- **Description:** Create a peer-to-peer (P2P) transaction.
- **Authentication:** JWT required.
- **Request Body:**
  - `receiver` (string): Receiver's username
  - `amount` (float): Transaction amount
  - `currency` (string): Currency code (e.g., USD)
- **Response:**
  - Success (200 OK):
    ```json
    {
      "message": "Transfer transaction created successfully"
    }
    ```
  - Error (500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 4. Create User

- **Endpoint:** `/newUser`
- **Method:** `POST`
- **Description:** Create a new user account.
- **Authentication:** None
- **Request Body:**
  - `email` (string): User email address
  - `name` (string): User name
  - `phone` (string): User phone number
  - `pin` (string): User PIN
  - `currency` (array of strings): Supported currencies
- **Response:**
  - Success (200 OK):
    ```json
    {
      "message": "User registered successfully"
    }
    ```
  - Error (400 Bad Request or 500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 5. Top-Up Account

- **Endpoint:** `/topUp`
- **Method:** `POST`
- **Description:** Top up a user's account balance.
- **Authentication:** JWT required.
- **Request Body:**
  - `amount` (float): Top-up amount
  - `currency` (string): Currency code (e.g., USD)
- **Response:**
  - Success (200 OK):
    ```json
    {
      "stripe_url": "Stripe checkout URL",
      "sessionId": "Stripe session ID"
    }
    ```
  - Error (500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 6. Create Group Transaction

- **Endpoint:** `/group`
- **Method:** `POST`
- **Description:** Create a group transaction.
- **Authentication:** JWT required.
- **Request Body:**
  - `name` (string): Group name
  - `members` (array of strings): Usernames of group members
  - `amount` (float): Transaction amount
  - `currency` (string): Currency code (e.g., USD)
- **Response:**
  - Success (200 OK):
    ```json
    {
      "message": "Group Payment has been created successfully"
    }
    ```
  - Error (400 Bad Request or 500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 7. Check Group Transaction

- **Endpoint:** `/group/check`
- **Method:** `POST`
- **Description:** Check and modify group payment distribution (for the group requestor).
- **Authentication:** JWT required.
- **Request Body:**
  - `group_id` (string): Group transaction ID
  - `distribution` (object): New distribution of payments
- **Response:**
  - Success (200 OK):
    ```json
    {
      "message": "Group Payment has been updated successfully"
    }
    ```
  - Error (400 Bad Request or 500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 8. Process Group Payment

- **Endpoint:** `/group/payment`
- **Method:** `POST`
- **Description:** Process group payments (for group members).
- **Authentication:** JWT required.
- **Request Body:**
  - `group_id` (string): Group transaction ID
- **Response:**
  - Success (200 OK):
    ```json
    {
      "message": "I paid my part, thank you"
    }
    ```
  - Error (400 Bad Request or 500 Internal Server Error):
    ```json
    {
      "error": "Error message"
    }
    ```

#### 9. Stripe Webhook

- **Endpoint:** `/webhook`
- **Method:** `POST`
- **Description:** Handle Stripe webhook events (e.g., successful payments).
- **Authentication:** None
- **Request Body:** Stripe webhook payload
- **Response:**
  - Success (200 OK): Acknowledgment of successful processing.
  - Error (400 Bad Request or 500 Internal Server Error): Error messages.

### Error Responses

In case of an error, the response JSON will include an `error` field with an error message.

## Contribution
The project was contributed by Victor, Ricky, JunLe, and YinYu

## License
This project is licensed under the MIT License. See the LICENSE file for details.
