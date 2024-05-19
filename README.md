# XDel Singapore - API

API for XDel Singapore. XDel Singapore specializes in express courier and delivery services, including e-commerce logistics, international and cross-border deliveries, as well as postal and logistics activities. This API is being developed as a university project for a cloud computing course using AWS infrastructure, leveraging services such as AWS EC2, RDS, ELB, and Docker containers.

## Quick Start

To get the application running locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/JoseGarayar/api_xdel.git
   cd api_xdel

2. **Build the Docker Container for development**
   ```bash
   docker-compose -f local.yml up --build

3. **Access the Web Interface in development environment**

- Open your web browser and navigate to 

   * http://localhost:5001 App1 Security
   * http://localhost:5002 App2 Clients
   * http://localhost:5003 App3 Orders
   * http://localhost:5004 App4 Shipment

   to interact with the model through the web interface.

3. **Create env file for production**
- Create a new folder `.envs/.production` with env files similar to files in `.envs/.local`

   ```bash
   # Flask
   # .envs/.production/.flask.env
   FLASK_ENV=production
   SECRET_KEY=
   JWT_SECRET_KEY=
   ```
   ```bash
   # PostgreSQL
   # .envs/.production/.postgres.env
   POSTGRES_HOST=
   POSTGRES_PORT=
   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   ```

4. **Build the Docker Container for production**
   ```bash
   docker-compose -f production.yml up --build

5. **Access the Web Interface in production environment**

- Open your web browser and navigate to 

   * http://your_ip:8080 App1 Security
   * http://your_ip:8081 App2 Clients
   * http://your_ip:8082 App3 Orders
   * http://your_ip:8083 App4 Shipment

   to interact with the model through the web interface.