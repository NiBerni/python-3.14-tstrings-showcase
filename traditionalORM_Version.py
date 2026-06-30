from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Set up the Base class for our ORM models
Base = declarative_base()


# Define the Products table
class Product(Base):
    """SQLAlchemy model representing the products table (Traditional ORM)."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)


class ProductManager:
    """Class to handle all database operations for Products."""

    def __init__(self, session):
        self.session = session

    def add_product(self, name, price):
        """Add a new product using standard ORM state tracking."""
        product = Product(name=name, price=price)
        self.session.add(product)
        self.session.commit()
        print(f"Product '{name}' added successfully!")

    def get_all_products(self):
        """Retrieve all products using standard ORM query filtering."""
        products = self.session.query(Product).all()
        if not products:
            print("No products found in the database.")
            return
        for p in products:
            print(f"ID: {p.id} | Name: {p.name} | Price: ${p.price:.2f}")

    def update_product_price(self, product_id, new_price):
        """Update a product's price using built-in ORM session methods."""
        product = self.session.get(Product, product_id)
        if product:
            product.price = new_price
            self.session.commit()
            print(f"Price for '{product.name}' updated to ${new_price:.2f}")
        else:
            print(f"Product with ID {product_id} not found.")

    def delete_product(self, product_id):
        """Delete a product using built-in ORM session methods."""
        product = self.session.get(Product, product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
            print(f"Product '{product.name}' deleted successfully.")
        else:
            print(f"Product with ID {product_id} not found.")


def main():
    """Main application entry point for the traditional ORM version."""
    # Setup the SQLite database
    engine = create_engine("sqlite:///products.db", echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Initialize our manager to handle the operations
    manager = ProductManager(session)

    # Infinite loop to handle interactive human input
    while True:
        print("\n--- Product Manager CLI ---")
        print("1. Add a Product")
        print("2. View All Products")
        print("3. Update a Product's Price")
        print("4. Delete a Product")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            name = input("Enter product name: ")
            try:
                price = float(input("Enter product price: "))
                manager.add_product(name, price)
            except ValueError:
                print("Invalid input! Price must be a number.")

        elif choice == "2":
            manager.get_all_products()

        elif choice == "3":
            try:
                prod_id = int(input("Enter product ID to update: "))
                new_price = float(input("Enter new price: "))
                manager.update_product_price(prod_id, new_price)
            except ValueError:
                print(
                    "Invalid input! ID must be an integer and price must be a number."
                )

        elif choice == "4":
            try:
                prod_id = int(input("Enter product ID to delete: "))
                manager.delete_product(prod_id)
            except ValueError:
                print("Invalid input! ID must be an integer.")

        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select a valid option.")


if __name__ == "__main__":
    main()
