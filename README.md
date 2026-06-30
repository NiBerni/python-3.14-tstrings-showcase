# Product Manager CLI: Python 3.14 `t-strings` Showcase

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/)
[![SQLAlchemy Version](https://img.shields.io/badge/sqlalchemy-2.1%2B-red.svg)](https://www.sqlalchemy.org/)
[![Security: Defensive](https://img.shields.io/badge/Security-Defensive%20Architecture-success.svg)](https://owasp.org/)

A production-grade CLI showcase demonstrating the shift in Developer Experience (DX) and native data security introduced
by **Python 3.14 `t-strings` (PEP 750)**.

This repository provides a direct architectural comparison between traditional SQLAlchemy ORM state tracking and the
brand-new, injection-proof `tstring()` expression engine in **SQLAlchemy 2.1**.

---

## 🎯 Architectural Motivation

### The Problem: Untrusted External APIs & Second-Order Vulnerabilities

In modern applications, data is frequently consumed from external third-party APIs. Under a **Zero-Trust Architecture**,
any incoming data payload must be treated as unsafe.

Traditional `f-strings` blindly blend executable SQL logic with raw data variables, exposing applications to severe
**Second-Order SQL Injections** if an upstream API has been compromised.

### The Solution: Native Boundary Separation

`t-strings` (Template Strings) do not evaluate to flat strings. Instead, they compile into an immutable `Template`
object that strictly segregates static code structure from dynamic user inputs at the interpreter level.

By using SQLAlchemy 2.1's native `tstring()` handler, this project leverages **Security by Design**—combining the
clean inline readability of an f-string with the absolute runtime safety of compiled Prepared Statements.

---

## 📊 Direct CRUD Transformation Comparison

The `ProductManager` class highlights how queries shift from high-abstraction ORM state management to explicit, highly
legible, and secure raw SQL templates:

| Operation  | Traditional ORM (State-Tracked)                               | Modern `t-string` Paradigm (Explicit)                                                                        |
|:-----------|:--------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
| **Create** | `product = Product(name=name, ...)`<br>`session.add(product)` | `session.execute(tstring(t"INSERT INTO products (name) VALUES ({name})"))`                                   |
| **Read**   | `session.query(Product).all()`                                | `stmt = select(Product).from_statement(tstring(t"SELECT * FROM products"))`<br>`session.scalars(stmt).all()` |
| **Update** | `product.price = new_price`                                   | `session.execute(tstring(t"UPDATE products SET price = {new_price} WHERE id = {product_id}"))`               |
| **Delete** | `session.delete(product)`                                     | `session.execute(tstring(t"DELETE FROM products WHERE id = {product_id}"))`                                  |

### Key Developer Experience (DX) Benefits:

1. **Zero Cognitive Overhead:** No disconnected parameter dictionaries or named placeholder mappings (`:param_name`).
   The code reads sequentially from left to right.
2. **IDE Language Injection:** PyCharm natively recognizes the `t`-prefix, unlocking flawless SQL syntax highlighting
   and autocompletion while preserving standard Python variable introspection within the curly braces `{}`.

---

## 🛠️ System Requirements & Fail-Fast Guard

Due to the bleeding-edge language features utilized, this repository strictly enforces runtime environment constraints.

A custom **Fail-Fast Runtime Guard** is implemented at the application entry point. Adhering to *PEP 20 (The Zen of
Python)*—*"Errors should never pass silently"*—the application will gracefully abort execution if a legacy Python
environment is detected, preventing obscure downstream syntax failures.

### `pyproject.toml` Standard Configuration

```toml
[project]
name = "product-manager-tstrings"
version = "1.0.0"
description = "A Python 3.14 showcase for PEP 750 template strings with SQLAlchemy 2.1"
requires-python = ">=3.14"
dependencies = [
    "sqlalchemy>=2.1.0b1",
]
```

---

## 📂 Quick Start & Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/NiBerni/python-3.14-tstrings-showcase.git
   cd python-3.14-tstrings-showcase
   ```

2. **Verify Environment Requirements:**
   Ensure your local interpreter or virtual environment meets the minimum version constraints:
   ```bash
   python --version  # Must output Python 3.14.0 or higher
   ```

3. **Execute the Application:**
   Run the modern showcase demonstrating native `t-strings` and secure raw SQL:
   ```bash
   python explicit_sql_templates.py
   ```

   *(Optional) To see the traditional ORM state-tracked version for comparison, you can run:*
   ```bash
   python traditional_state_tracking.py
   ```

---

## 📚 References & Official Specifications

* **PEP 750 – Rich String Literals (t-strings):** [https://peps.python.org/pep-0750/](https://peps.python.org/pep-0750/)
* **SQLAlchemy 2.1 – `tstring()` Expression Core API:
  ** [http://docs.sqlalchemy.org/en/latest/core/expression_api.html#sqlalchemy.sql.expression.tstring](http://docs.sqlalchemy.org/en/latest/core/expression_api.html#sqlalchemy.sql.expression.tstring)
* **OWASP Top 10 – Injection Mitigation Cheat Sheet:
  ** [https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
* **PEP 20 – The Zen of Python:** [https://peps.python.org/pep-0020/](https://peps.python.org/pep-0020/)