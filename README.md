# XDel Singapore - API

API for XDel Singapore.

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

- Open your web browser and navigate to http://localhost:5000 to interact with the model through the web interface.

4. **Build the Docker Container for production**
   ```bash
   docker-compose -f production.yml up --build

5. **Access the Web Interface in production environment**

- Open your web browser and navigate to http://your_ip to interact with the model through the web interface.