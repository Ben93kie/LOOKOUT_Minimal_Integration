import asyncio
import websockets
import json

async def connect_and_receive_metadata():
    """ Connects to the metadata stream, receives, and prints metadata."""
    async with websockets.connect("ws://localhost:5679") as websocket:
        while True:
            metadata_bytes = await websocket.recv()
            metadata_json = metadata_bytes.decode('utf-8')
            metadata = json.loads(metadata_json)

            # Print the received metadata neatly
            print("------ Received Metadata ------")
            print(metadata)  # Prints the entire JSON data neatly

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect_and_receive_metadata())
