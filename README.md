# LOOKOUT Minimal Integration/Interface Illustration
![Screenshot (81)](https://github.com/Ben93kie/LOOKOUT_Minimal_Integration/assets/64975055/0ea60182-1103-401f-a021-8a914ad5714d)
## Overview

This repository contains the code for a server-client setup designed to showcase the integration between LOOKOUT and another system. Video and detected objects are streamed out using websocket and JSON.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or newer.
- A modern web browser (e.g., Chrome, Firefox, Safari).

## Running it

Follow these steps to get your development environment set up:

1. **Clone the Repository**
    ```sh
    git clone https://github.com/Ben93kie/LOOKOUT_Minimal_Integration.git
    ```
2. **Cd into the directory and install the requirements**
   ```sh
    pip install -r requirements.txt
    ```
3. **Run the server**
    ```sh
    python server.py
    ```
4. **Run the video client**

   Open index.html in a browser. Or alternatively serve it on a port of your choice, e.g. on port 8000 via python -m http.server 8000.
   
5. **Alternatively for just the metadata, run the metdata client**
   ```sh
    python client.py
    ```

## Let me know if you need more detailed specifications, then I'll send an Interface Design Definition and API specs
   
   

    

   
