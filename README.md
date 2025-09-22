# Decor

Decor is a web app that helps users visualize and manage décor items: create, collect your favorites, organize, and design beautiful spaces.  

---

## 🚀 Features

- Browse décor items with images and details  
- Add items to your **Favorites**  
- Add items to your **Cart** for purchase planning  
- Categorized décor collections for easier browsing  
- User authentication (login/logout)  
- Media management: upload/display images of décor items  

---

## 🧰 Tech Stack

- Backend: Python / Django  
- Frontend: JavaScript / HTML / CSS  
- Database: SQLite (for development)  
- Deployment: (Add if you’re using Heroku / AWS / etc.)  
- Other tools / libs: requirements specified in `requirements.txt`  

---

## 📂 Project Structure

```text
/
├── authentication/     # user login/register, profile management
├── cart/               # cart handling, adding/removing items
├── decor/              # main décor item models, views
├── favorites/          # saving favorite décor items
├── item/               # item-specific logic
├── media/              # media files (images etc.)
├── static/             # static files (CSS, JavaScript, images)
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── db.sqlite3          # Development database
```

---

## 🔧 Installation & Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/0xCode7/Decor.git
   cd Decor
   ```

2. **Create a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (if any)  
   You may need to set secrets like:
   - `SECRET_KEY`  
   - Database settings  
   - Media storage settings  

5. **Apply migrations**  
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

7. **Access the app**  
   Open your browser to `http://127.0.0.1:8000`  

---


## 🌐 Deployment

(Write instructions specific to your deployment)  
E.g., Deploy to Heroku / AWS / etc.:

- Optionally set up `Procfile`  
- Ensure static files are collected  
- Configure allowed hosts  
- Set up environment vars  

---
## 👤 About Me

Built by **0xCode7** (Mahmoud Said).

📧 Email: mahmoudsaid1704@gmail.com  
📱 Phone: +201030455138  

Passionate about full-stack dev.  
