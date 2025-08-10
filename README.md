# diffdrive

A Flask-based server for simulating multiple differential drive robots, extended through a 3D visualization environment, and tested with traditional and browser based programming environments (JupyterLite and Snap!). The system's core functionality involves applying control inputs to modify the dynamical equations of motion for the simulated robots.

---

### **Key Features**

* **Extensible Simulation:** The backend uses matrix-based equations of motion, allowing the system to scale and simulate multiple robot "plants" at runtime. The number of plants is configured via the `NUM_PLANTS` environment variable.
* **Multiple Control Interfaces:** Control robots using a 3D environment with on-screen joysticks (nipplejs), keyboard arrow keys, or programmatically via HTTP requests from any language.
* **Web-Based Development:** Integrated **JupyterLite** environment for Python coding and experimentation directly in the browser.
* **Object Detection (Frontend):** Object detection is currently performed within the 3D visualization environment (frontend) using TensorFlow.js with the COCO SSD model. Detected objects are published to the backend at a fixed rate.
* **API Documentation:** An integrated Swagger interface provides a clear and comprehensive view of the server's API endpoints.

---

### **Technologies Used**

#### **Backend**

* **Python:** The core language for the server logic.
* **Flask:** The web framework handling the server and API endpoints.

#### **Frontend**

* **HTML5:** The foundation for the web-based interfaces.
* **three.js:** Renders the 3D simulation environment.
* **tensorflow.js:** Powers real-time object detection using the COCO SSD model.
* **nipplejs:** Enables the on-screen joystick for mobile and touch-based control.
* **JupyterLite:** Provides an in-browser Python environment that acts as a frontend for the user to interact with the project.

#### **Communication & Control**

* **HTTP:** The standard communication protocol for all interactions.
* **requests (Python):** A library used to send HTTP requests from a Python environment.

---

### **Installation and Setup**

To get the simulation running, you have three primary options:

#### **Option 1: Manual Installation**

1.  **Clone the repository:**
```bash
git clone https://github.com/hazrobotz/diffdrive
```

2.  **Navigate to the project directory:**
```bash
cd diffdrive
```

3.  **Install the required Python packages:**
```bash
pip install -r requirements.txt
```

4.  **Start the server, specifying the number of robots:**
```bash
cd code
NUM_PLANTS=3 python webservice.py
```
*Note: Replace `3` with the desired number of robots you wish to simulate. You can also set `PORT` and `SAMPLE_PERIOD` environment variables here if needed.*

#### **Option 2: Running with Docker (Prebuilt Image)**

To quickly get started using a prebuilt Docker image:

```bash
docker run --rm -p 8080:8080 -v /tmp:/app/saved -e PORT=8080 -e NUM_PLANTS=3 ghcr.io/hazrobotz/diffdrive:main
```

#### Option 3: Building and Running Docker Locally

If you prefer to build the Docker image yourself, here's how to do it.

##### Building the Docker Image

1.  **Clone the repository:**
    
```bash
git clone https://github.com/hazrobotz/diffdrive.git
```
    
2.  **Navigate into the cloned directory:**
    
```bash
cd diffdrive
```
    
3.  **Build the Docker image:**
    
```bash
docker build -t testdiffdrive .
```

##### Running the Docker Container

To run the Docker container with a few default settings, use the following command:

```bash
docker run --rm -p 8000:8000 -v /tmp:/app/saved -e PORT=8000 -e NUM_PLANTS=2 -e SAMPLE_PERIOD=0.02 testdiffdrive
```
*Note: This example uses `PORT=8000`, `NUM_PLANTS=2`, and `SAMPLE_PERIOD=0.02` for demonstration. You can adjust these values as needed to fit your specific use case.*

## Accessing the Resources

Once the server (either manual or Docker) is running, you can access the various components in your web browser. Note that the simulation environment URLs are specific to each robot.

* **2D Simulation Environment (for robot 0):** `http://127.0.0.1:8080/0`
* **3D Simulation Environment (for robot 0):** `http://127.0.0.1:8080/0/3`

To view other robots, just change the robot ID in the URL (e.g., `/1` or `/1/3` for robot 1).

* **JupyterLite Python Environment:** `http://127.0.0.1:8080/jupyter/index.html`
* **Admin Swagger Interface:** `http://127.0.0.1:8080/ui`

---

## Known Issues & Performance

The system relies on constant polling from the frontend. Both the visualization and control loops generate around **20 requests per second per robot**, which can impact performance on less powerful machines or networks. When scaling the number of simulated robots, it's important to be mindful of the significant polling rate and request volume on the backend.

---

## Future Extensions

* **Motion JPEG (mjpeg) Endpoint:** We plan to integrate with **OpenCV-Python** to create an mjpeg endpoint for streaming video from the simulation.
* **OpenCV in JupyterLite for Object Detection:** This will enable OpenCV within the JupyterLite environment to process the future mjpeg stream, providing a new source for object detection.
* **LIDAR Simulation:** Implementation of **LIDAR** (Light Detection and Ranging) sensor simulation within the 3D environment.
