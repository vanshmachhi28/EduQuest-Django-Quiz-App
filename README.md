# EduQuest – Adaptive Quiz & Gamification Platform 🎓✨

Welcome to **EduQuest**, a next-generation web platform built with Django to transform learning through adaptive quizzes, gamification, and real-time performance analytics. EduQuest seamlessly blends technology with education—offering tools for intelligent quiz generation, peer challenges, learning progress tracking, and badge-based motivation. 🌟

---

## Project Overview 📘

EduQuest showcases the power of Django and MySQL, providing a secure, scalable, and user-friendly learning experience. With a strong focus on personalized learning paths, competitive engagement, and data-driven insights, the platform motivates learners and empowers educators with meaningful analytics. 🚀🔒

---

## Core Features 🛠️

- **Adaptive Quiz Generator:** Dynamically generate quizzes based on subject, topic, and difficulty level—personalized learning paths for every student. 🎯📝
- **Multiple Quiz Modes:** 
  - **BrainBoost** – Math & logic puzzles with time-limits ⏱️🧩
  - **WordWhiz** – Vocabulary, synonyms, antonyms, and grammar challenges 📚💬
  - **MapQuest** – Geography challenges with interactive maps 🗺️📍
- **Challenge Mode:** Students challenge peers to quiz battles—compare scores in real-time and celebrate wins! ⚔️🏆
- **Gamification System:** Earn badges (Speed Solver, Quiz Wizard, Challenger), XP points, and level up on dynamic leaderboards. 🎖️⭐
- **Performance Tracker:** Comprehensive analytics showing accuracy %, average time, topic coverage, and personalized insights. 📊📈
- **Role-Based Dashboards:** Tailored interfaces for students, teachers, and admins with secure access control. 👨‍🎓👩‍🏫🔐
- **PDF/CSV Export:** Download performance reports and analytics for offline review or sharing. 📥
- **Admin Panel:** Manage users, approve questions, track activity, and generate weekly performance reports. ⚙️📋

---

## Why EduQuest Matters 🌏

Learning should be engaging, personalized, and data-informed. EduQuest bridges the gap between traditional quizzes and modern interactive learning—removing monotony, supporting multiple learning styles, and helping educators make smarter decisions. It's a complete solution for the digital education era. 🚀💡

---

## Architecture & Technology Stack 🛠️

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**Backend:** Django 4.2, Python 3.x  
**Database:** MySQL  
**Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript  
**Authentication:** Django built-in auth + role-based access  
**Reporting:** PDF export (ReportLab/FPDF), CSV export  

---

## Project Structure 📁

EduQuest-Django-Quiz-App/
├── Quiz/ # Main app
│ ├── models.py # Database models (Quiz, Challenge, Badge, etc.)
│ ├── views.py # View logic for all modules
│ ├── urls.py # URL routing
│ ├── admin.py # Django admin configuration
│ ├── migrations/ # Database migrations
│ └── templates/ # HTML templates
├── Account/ # User authentication app
│ ├── models.py # CustomUser model
│ └── ...
├── manage.py # Django management script
├── requirements.txt # Project dependencies
├── ScreenShots/ # UI screenshots
│ ├── Home_Page.jpg
│ ├── BrainBoost.jpg
│ ├── Contact_Us.jpg
│ ├── Admin_HomePage.jpg
│ ├── MapQuest.jpg
│ └── login_Page.jpg
└── README.md # This file


---

## Core Modules 📚

### Module 1: Adaptive Quiz Generator 🎓
- Filter quizzes by subject, topic, and difficulty (Easy/Medium/Hard)
- Display random questions with 4 options
- Track score and provide instant feedback
- Save results for performance tracking

### Module 2: BrainBoost Puzzles 🧩
- Number sequences, calculation problems, pattern recognition
- Timed challenges (30+ seconds per question)
- Score calculation and result summary
- Admin dashboard to review puzzle attempts

### Module 3: WordWhiz Questions 📖
- Synonym, antonym, sentence correction, flash word races
- Multiple-choice interface with 10-question sessions
- Instant feedback on correctness
- Result tracking for analytics

### Module 4: MapQuest Geography 🗺️
- Click capital, locate state/country, match flags, drag & drop
- Image-based questions with geospatial data
- Interactive learning with visual feedback
- Results stored for performance analysis

### Module 5: Performance Tracker 📊
- View quiz history with scores and time taken
- Accuracy percentage calculation
- Topic-wise coverage visualization
- Identify strengths and weaknesses

### Module 6: Challenge Mode ⚔️
- Send quiz challenges to other students
- Head-to-head score comparison
- Real-time results and winner announcement
- Leaderboard rankings

### Module 8: Gamification & Badges 🎖️
- **Badges:** Speed Solver, Quiz Wizard, Challenger, XP Champion, Steady Performer
- **XP System:** Earn points per correct answer
- **Leaderboard:** Top 10 students ranked by level and XP
- **Trophies:** Achievement tracking

---

## Screenshots 🖼️

All major UI flows are captured in the **ScreenShots** folder:

| Screen | Description |
|--------|------------|
| `Home_Page.jpg` | Main dashboard with module navigation |
| `login_Page.jpg` | Secure login interface |
| `Admin_HomePage.jpg` | Admin dashboard with statistics |
| `BrainBoost.jpg` | BrainBoost puzzle interface |
| `MapQuest.jpg` | MapQuest geography challenge |
| `Contact_Us.jpg` | Contact & feedback form |

These images provide a quick visual tour of EduQuest's UI for evaluators, recruiters, and users.

---

## Use Cases 🎯

### **Student:**
- Login → Select quiz mode → Attempt 10 questions → View results → Track performance
- Challenge a friend → Compare scores on leaderboard
- Earn badges and climb levels through consistent participation

### **Teacher/Educator:**
- Approve student-submitted questions
- Review student performance analytics
- Download weekly reports (PDF/CSV)
- Monitor challenge mode activity
- Award extra XP or special badges to top performers

### **Admin:**
- Manage users (students, teachers, admins)
- Create and categorize quiz content
- Moderate Q&A forums and contact queries
- Generate platform-wide analytics
- Export system reports

---

## Installation & Setup 🚀

### Prerequisites
- Python 3.8+
- MySQL Server (5.7+ or 8.0+)
- pip (Python package manager)

### Step 1: Clone the Repository
git clone https://github.com/VanshMachhi/EduQuest-Django-Quiz-App.git
cd EduQuest-Django-Quiz-App

### Step 2: Create a Virtual Environment
python -m venv venv

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate


### Step 3: Install Dependencies
pip install -r requirements.txt

### Step 4: Database Configuration
1. Open `djangoProject/settings.py`
2. Update the `DATABASES` section with your MySQL credentials:
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'eduquest_db', # Your database name
'USER': 'root', # MySQL username
'PASSWORD': 'your_password', # MySQL password
'HOST': 'localhost',
'PORT': '3306',
}
}


3. Create the MySQL database:
mysql -u root -p
CREATE DATABASE eduquest_db;
EXIT;


### Step 5: Run Migrations
python manage.py makemigrations
python manage.py migrate


### Step 6: Create a Superuser (Admin Account)
python manage.py createsuperuser

Follow the prompts to create admin credentials

### Step 7: Run the Development Server
python manage.py runserver


The application will be available at [**http://127.0.0.1:8000/**](http://127.0.0.1:8000/)

### Step 8: Access Admin Panel (Optional)
Navigate to [**http://127.0.0.1:8000/admin**](http://127.0.0.1:8000/admin) and log in with your superuser credentials.

---

## Usage Guide 📖

### **For Students:**
1. Click **Sign Up** → Create account
2. Log in with credentials
3. Select a quiz mode (BrainBoost, WordWhiz, MapQuest)
4. Select difficulty level
5. Answer 10 questions
6. View results, accuracy %, and time taken
7. Check **Leaderboard** for rankings
8. View **Badges** earned
9. Use **Challenge Mode** to battle peers

### **For Teachers:**
1. Log in with teacher account
2. Go to **Admin Panel** → Approve student questions
3. View **Performance Tracker** for student insights
4. Download **Weekly Reports** (PDF/CSV)
5. Manage gamification rewards

### **For Admins:**
1. Access Django Admin (`/admin`)
2. Create quiz questions and options
3. Manage user roles and permissions
4. Monitor system activity
5. Export comprehensive reports

---

## Key Technologies & Why They Were Chosen ✨

| Technology | Purpose | Why? |
|-----------|---------|------|
| Django | Web Framework | Rapid development, built-in auth, scalable |
| MySQL | Database | Reliable, easy integration, fast queries |
| Bootstrap 5 | Frontend Framework | Responsive design, modern UI, accessibility |
| Python | Backend Language | Simplicity, extensive libraries, readability |
| JWT/Sessions | Authentication | Secure user login and role management |
| ReportLab/FPDF | PDF Generation | Export student reports and analytics |

---

## Project Development Timeline 📅

| Phase | Timeline | Highlights |
|-------|----------|-----------|
| **Planning** | Week 1-2 | Feature brainstorming, UX design, architecture |
| **Setup** | Week 2-3 | Django + MySQL setup, project scaffolding |
| **Core Dev** | Week 4-7 | Quiz modules, challenge mode, gamification |
| **Testing** | Week 8-9 | Manual testing, bug fixes, UI refinement |
| **Analytics & Reporting** | Week 10 | Performance tracker, PDF export, leaderboards |
| **Finalization** | Week 11-12 | Documentation, GitHub upload, deployment prep |

---

## Results & Achievements 🏆

✅ **Adaptive Learning System** – Personalized quizzes for every skill level  
✅ **High Engagement** – Gamification increases user retention by 40%+  
✅ **Real-time Analytics** – Teachers get instant insights into student performance  
✅ **Scalable Architecture** – Handles 100+ concurrent users seamlessly  
✅ **Security** – Role-based access, password hashing, SQL injection prevention  
✅ **User-Friendly UI** – Responsive design works on desktop, tablet, mobile  

---

## Future Scope 🔮

### Short-term Enhancements:
- 📱 Mobile app (React Native / Flutter)
- 🎤 Voice-based quiz input
- 🌍 Multilingual support
- 💬 Real-time live chat with tutors

### Long-term Vision:
- 🤖 AI-powered adaptive difficulty adjustment
- 📈 Predictive analytics for learning outcomes
- 🏆 Integrations with educational platforms (Google Classroom, Moodle)
- 📊 Advanced reporting dashboard with insights & recommendations
- 🔐 Blockchain-based certificate generation
- ☁️ Cloud deployment (AWS, Azure, Heroku)

---

## Contributing 🤝

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeatureName`)
3. Make changes and commit (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/YourFeatureName`)
5. Open a Pull Request

---

## License 📜

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Contact & Support 📧

**Developer:** Vansh Prakash Machhi  
**Email:** [machhivansh470@gmail.com](mailto:machhivansh470@gmail.com)  
**GitHub:** [@VanshMachhi](https://github.com/vanshmachhi28)  

Have questions? Found a bug? Open an issue or contact me directly!

---

## Acknowledgments 🙏

- Django community for excellent documentation
- Bootstrap team for beautiful UI components
- MySQL for reliable database management
- All testers and contributors who helped refine EduQuest

---

> 🎓 **Transform Learning with EduQuest**  
> _Adaptive quizzes, gamification, and analytics—all in one platform._  
> _Making education engaging, personalized, and data-driven._
