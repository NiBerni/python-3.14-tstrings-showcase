import sys

from sqlalchemy import Column, Float, Integer, String, create_engine, select, tstring
from sqlalchemy.orm import declarative_base, sessionmaker

# ======================================================================
# FAIL-FAST RUNTIME GUARD (PEP 20 guard for legacy environments)
# ======================================================================
if sys.version_info < (3, 14):
    sys.exit(
        "\n======================================================================\n"
        "❌ RUNTIME ERROR: Python 3.14+ required!\n"
        "======================================================================\n"
        "This project utilizes t-strings (PEP 750) introduced in Python 3.14\n"
        "for native, SQL-injection-safe template processing.\n\n"
        "According to PEP 20 (The Zen of Python): 'Errors should never pass silently.'\n"
        "Therefore, this application strictly refuses to execute on a legacy\n"
        "runtime environment.\n"
        "======================================================================\n"
    )

Base = declarative_base()


class Product(Base):
    """SQLAlchemy model representing the products table."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)


class ProductManager:
    """Class to handle all database operations for Products using t-strings."""

    def __init__(self, session):
        self.session = session

    def add_product(self, name, price):
        """Insert a new product using native t-strings."""
        # Native SQL INSERT via tstring
        self.session.execute(
            tstring(t"INSERT INTO products (name, price) VALUES ({name}, {price})")
        )
        self.session.commit()
        print(f"Product '{name}' added successfully!")

    def get_all_products(self):
        """Fetch and print all products using a t-string raw statement."""
        # Raw SQL query whose result is automatically mapped to Product objects
        stmt = select(Product).from_statement(tstring(t"SELECT * FROM products"))
        products = self.session.scalars(stmt).all()

        if not products:
            print("No products found in the database.")
            return
        for p in products:
            print(f"ID: {p.id} | Name: {p.name} | Price: ${p.price:.2f}")

    def update_product_price(self, product_id, new_price):
        """Update a product's price securely using t-strings."""
        # First check if the product exists (mimics legacy session.get behavior)
        stmt = select(Product).from_statement(
            tstring(t"SELECT * FROM products WHERE id = {product_id}")
        )
        product = self.session.scalars(stmt).first()

        if product:
            # Native SQL UPDATE command via tstring
            self.session.execute(
                tstring(
                    t"UPDATE products SET price = {new_price} WHERE id = {product_id}"
                )
            )
            self.session.commit()
            print(f"Price for '{product.name}' updated to ${new_price:.2f}")
        else:
            print(f"Product with ID {product_id} not found.")

    def delete_product(self, product_id):
        """Delete a product by ID using t-strings."""
        # First fetch the product via tstring to get its name for the print statement
        stmt = select(Product).from_statement(
            tstring(t"SELECT * FROM products WHERE id = {product_id}")
        )
        product = self.session.scalars(stmt).first()

        if product:
            # Native SQL DELETE via tstring
            self.session.execute(
                tstring(t"DELETE FROM products WHERE id = {product_id}")
            )
            self.session.commit()
            print(f"Product '{product.name}' deleted successfully.")
        else:
            print(f"Product with ID {product_id} not found.")


def main():
    """Main application entry point initializing the database and starting the CLI loop."""
    # Setup the SQLite database
    engine = create_engine("sqlite:///products.db", echo=False)
    Base.metadata.create_all(engine)

    # Session-handling with sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    manager = ProductManager(session)

    # CLI Loop for human interaction stays the same
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
