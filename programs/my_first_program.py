import asyncio
import os
import py_nillion_client as nillion
import shutil
import sys
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Blockchain client setup
NODE_URL = os.getenv("NODE_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

client = nillion.Client(node_url=NODE_URL, private_key=PRIVATE_KEY)

# Define the EHR class
class ElectronicHealthRecord:
    def __init__(self, patient_id, patient_name, dob, medical_history):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.dob = dob
        self.medical_history = medical_history

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "dob": self.dob,
            "medical_history": self.medical_history
        }

    @staticmethod
    def from_dict(data):
        return ElectronicHealthRecord(
            patient_id=data["patient_id"],
            patient_name=data["patient_name"],
            dob=data["dob"],
            medical_history=data["medical_history"]
        )

# Blockchain functions
async def add_ehr(record):
    record_data = record.to_dict()
    transaction = await client.create_transaction(data=record_data)
    response = await client.send_transaction(transaction)
    return response

async def get_ehr(patient_id):
    query = {"patient_id": patient_id}
    response = await client.query_transactions(query)
    if response and len(response) > 0:
        return ElectronicHealthRecord.from_dict(response[0]["data"])
    return None

async def main():
    # Example usage
    record = ElectronicHealthRecord(
        patient_id="12345",
        patient_name="John Doe",
        dob="1990-01-01",
        medical_history=["Allergy: Peanuts", "Surgery: Appendectomy"]
    )

    # Add EHR to blockchain
    add_response = await add_ehr(record)
    print("EHR Added:", add_response)

    # Retrieve EHR from blockchain
    retrieved_record = await get_ehr("12345")
    if retrieved_record:
        print("EHR Retrieved:", retrieved_record.to_dict())
    else:
        print("EHR not found.")

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
