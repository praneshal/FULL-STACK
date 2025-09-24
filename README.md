# BIT-FULL-STACK-Code 🚀

Welcome to **BIT-FULL-STACK-Code**, a full-stack assessment platform designed to streamline online exams, question paper management, and results tracking. This repository contains a well-structured workflow for the project, including a Flask backend and HTML-based frontend, making it an ideal foundation for building and deploying modern assessment solutions.

## 📖 Introduction

This project is a comprehensive demonstration of a full-stack application for an **Assessment Platform**, as outlined in the [PS_SRS.pdf](https://github.com/user-attachments/files/16437755/PS_SRS.pdf) requirements document. The platform enables exam management, user authentication, and result processing, providing a seamless experience for both administrators and examinees.

## ✨ Features

- **User Authentication:** Secure login system using Flask and bcrypt.
- **Exam Management:** Add, edit, and view question papers and exams.
- **Result Tracking:** Display and manage exam results.
- **Messaging System:** Interface for viewing and sending messages.
- **Help & Support:** Dedicated help section for users.
- **Responsive Frontend:** HTML templates styled with CSS for a modern look.
- **Database Integration:** Utilizes SQLAlchemy ORM for robust data handling.

## 🛠️ Installation

Follow these steps to get the project up and running locally:

1. **Clone the repository**
    ```bash
    git clone https://github.com/pranesh-2005/BIT-FULL-STACK-Code.git
    cd BIT-FULL-STACK-Code
    ```

2. **Set up a Python virtual environment (optional but recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database**
    - Set up your database URI in `app.py` as required.
    - Run initial migrations if using Flask-Migrate.

5. **Run the Flask application**
    ```bash
    python app.py
    ```
    The app will be available at [http://localhost:5000](http://localhost:5000).

## 🚦 Usage

- **Admin Panel:** Manage exams, question papers, and results via the provided HTML templates.
- **Student Portal:** Log in, participate in exams, view results, and access help resources.
- **Messaging:** Use the messaging module to communicate within the platform.

To explore the workflow and architecture, review the [PS_SRS.pdf](https://github.com/user-attachments/files/16437755/PS_SRS.pdf) for system requirements and design documentation.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/YourFeature
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Add your feature"
    ```
4. Push to your branch:
    ```bash
    git push origin feature/YourFeature
    ```
5. Open a Pull Request.

Please ensure your code follows best practices and is well-documented.

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

> For more information, refer to the workflow and requirements in [PS_SRS.pdf](https://github.com/user-attachments/files/16437755/PS_SRS.pdf).

---

**Developed with ❤️ by the BIT-FULL-STACK-Code Team**

## License
This project is licensed under the **MIT** License.

---
🔗 GitHub Repo: https://github.com/Pranesh-2005/BIT-FULL-STACK-Code