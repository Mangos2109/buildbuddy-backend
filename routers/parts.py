from fastapi import APIRouter

router = APIRouter()

@router.get("/parts")
def get_parts():
    return {
        "processors": [
            {"name": "Intel Core i9", "price": 500},
            {"name": "AMD Ryzen 9", "price": 480},
            {"name": "Intel Core i7", "price": 350},
            {"name": "AMD Ryzen 7", "price": 330}
        ],
        "gpus": [
            {"name": "NVIDIA RTX 4090", "price": 1600},
            {"name": "AMD Radeon RX 7900 XTX", "price": 1100}
        ],
        "ram": [
            {"name": "16GB DDR5", "price": 80},
            {"name": "32GB DDR5", "price": 150},
            {"name": "64GB DDR4", "price": 120}
        ],
        "motherboards": [
            {"name": "ASUS ROG STRIX Z790", "price": 400},
            {"name": "MSI MAG B650", "price": 280},
            {"name": "Gigabyte B450", "price": 150}
        ],
        "storage": [
            {"name": "1TB NVMe SSD", "price": 120},
            {"name": "2TB NVMe SSD", "price": 200}
        ],
        "psu": [
            {"name": "Corsair RM1000x 1000W", "price": 200},
            {"name": "EVGA SuperNOVA 850W", "price": 150}
        ]
    }
