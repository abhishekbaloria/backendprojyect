
import json
from tinythreads_backend import db, app, Product  

with app.app_context():
    with open("image.json", "r") as file:
        items = json.load(file)
        for item in items:
            product = Product(
                id=str(item["id"]),
                name=item["name"],
                desc=item["desc"],
                price=float(item["price"]),
                image=item["image"]
            )
            db.session.add(product)
        db.session.commit()
        print("✅ Products loaded into the database!")
