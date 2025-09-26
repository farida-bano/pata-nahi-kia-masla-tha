import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import random
from datetime import datetime
import io
import sqlite3
import hashlib
import time

class SocialStudiesProjects:
    """
    All three Social Studies projects in one class
    """
    
    def __init__(self):
        # Timeline data
        self.historical_data = {
            "Pakistan History": [
                {"event": "Birth of Quaid-e-Azam", "date": "1876-12-25"},
                {"event": "Foundation of Muslim League", "date": "1906-12-30"},
                {"event": "Pakistan Resolution", "date": "1940-03-23"},
                {"event": "Independence of Pakistan", "date": "1947-08-14"},
                {"event": "First Constitution", "date": "1956-03-23"}
            ],
            "Mughal Empire": [
                {"event": "Babur's conquest of India", "date": "1526-04-21"},
                {"event": "Humayun's accession to throne", "date": "1530-12-26"},
                {"event": "Akbar's accession to throne", "date": "1556-02-14"},
                {"event": "Taj Mahal construction started", "date": "1632-01-01"},
                {"event": "Death of Aurangzeb", "date": "1707-03-03"}
            ]
        }
        
        # Country data
        self.country_data = {
            "Pakistan": {
                "area": 881913,  # square km
                "population": 242923845,
                "capital": "Islamabad",
                "languages": ["Urdu", "Punjabi", "Sindhi", "Pashto"],
                "currency": "Pakistani Rupee",
                "economy": "Agriculture, Textiles, Services",
                "flag_colors": ["Green", "White"],
                "national_animal": "Markhor",
                "national_bird": "Chukar Partridge"
            },
            "India": {
                "area": 3287263,
                "population": 1428627663,
                "capital": "New Delhi",
                "languages": ["Hindi", "English", "Bengali", "Telugu"],
                "currency": "Indian Rupee",
                "economy": "Information Technology, Agriculture, Manufacturing",
                "flag_colors": ["Saffron", "White", "Green"],
                "national_animal": "Bengal Tiger",
                "national_bird": "Indian Peacock"
            },
            "Bangladesh": {
                "area": 147570,
                "population": 172954319,
                "capital": "Dhaka",
                "languages": ["Bengali"],
                "currency": "Taka",
                "economy": "Textiles, Agriculture, Remittances",
                "flag_colors": ["Green", "Red"],
                "national_animal": "Royal Bengal Tiger",
                "national_bird": "Oriental Magpie-Robin"
            }
        }
        
        # Quiz questions - Now with Pakistani map, flag, war, animal questions
        self.questions = {
            "Easy": [
                {
                    "question": "In which year was Pakistan created?",
                    "options": ["1940", "1947", "1956", "1971"],
                    "answer": "1947"
                },
                {
                    "question": "When is Quaid-e-Azam's birthday celebrated?",
                    "options": ["14 August", "25 December", "23 March", "6 September"],
                    "answer": "25 December"
                },
                {
                    "question": "What was the first capital of Pakistan?",
                    "options": ["Islamabad", "Lahore", "Karachi", "Dhaka"],
                    "answer": "Karachi"
                },
                {
                    "question": "Who is known as the Poet of the East?",
                    "options": ["Quaid-e-Azam", "Allama Iqbal", "Sir Syed Ahmed Khan", "Liaquat Ali Khan"],
                    "answer": "Allama Iqbal"
                },
                {
                    "question": "Which river is the longest in Pakistan?",
                    "options": ["Indus", "Jhelum", "Chenab", "Ravi"],
                    "answer": "Indus"
                },
                {
                    "question": "What is the national language of Pakistan?",
                    "options": ["English", "Punjabi", "Urdu", "Sindhi"],
                    "answer": "Urdu"
                },
                {
                    "question": "When is Pakistan Day celebrated?",
                    "options": ["14 August", "6 September", "23 March", "25 December"],
                    "answer": "23 March"
                },
                {
                    "question": "Which country shares the longest border with Pakistan?",
                    "options": ["India", "Afghanistan", "Iran", "China"],
                    "answer": "Afghanistan"
                },
                {
                    "question": "What is the national sport of Pakistan?",
                    "options": ["Cricket", "Hockey", "Football", "Squash"],
                    "answer": "Hockey"
                },
                {
                    "question": "Which mountain is the highest in Pakistan?",
                    "options": ["Nanga Parbat", "K2", "Tirich Mir", "Rakaposhi"],
                    "answer": "K2"
                }
            ],
            "Medium": [
                {
                    "question": "In which year was the Pakistan Resolution passed?",
                    "options": ["1930", "1940", "1947", "1956"],
                    "answer": "1940"
                },
                {
                    "question": "Who was the first Governor-General of Pakistan?",
                    "options": ["Allama Iqbal", "Liaquat Ali Khan", "Quaid-e-Azam", "Iskander Mirza"],
                    "answer": "Quaid-e-Azam"
                },
                {
                    "question": "When did the 1965 Pakistan-India war start?",
                    "options": ["6 September", "14 August", "23 March", "16 December"],
                    "answer": "6 September"
                },
                {
                    "question": "Who was the first Prime Minister of Pakistan?",
                    "options": ["Quaid-e-Azam", "Liaquat Ali Khan", "Khwaja Nazimuddin", "Ibrahim Ismail Chundrigar"],
                    "answer": "Liaquat Ali Khan"
                },
                {
                    "question": "When was the Simla Agreement signed?",
                    "options": ["1965", "1971", "1972", "1974"],
                    "answer": "1972"
                },
                {
                    "question": "Which city is called the City of Gardens?",
                    "options": ["Islamabad", "Karachi", "Lahore", "Peshawar"],
                    "answer": "Lahore"
                },
                {
                    "question": "When was the State Bank of Pakistan established?",
                    "options": ["1947", "1948", "1956", "1960"],
                    "answer": "1948"
                },
                {
                    "question": "Who wrote the national anthem of Pakistan?",
                    "options": ["Allama Iqbal", "Hafeez Jalandhari", "Ahmed Ghulam Ali Chagla", "Abdul Rab Nishtar"],
                    "answer": "Hafeez Jalandhari"
                },
                {
                    "question": "Which province of Pakistan is the largest by area?",
                    "options": ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan"],
                    "answer": "Balochistan"
                },
                {
                    "question": "When was the 1973 Constitution adopted?",
                    "options": ["14 August 1973", "23 March 1973", "10 April 1973", "12 May 1973"],
                    "answer": "10 April 1973"
                }
            ],
            "Hard": [
                {
                    "question": "Who was the Viceroy of India during Partition?",
                    "options": ["Lord Mountbatten", "Lord Wavell", "Lord Linlithgow", "Lord Irwin"],
                    "answer": "Lord Mountbatten"
                },
                {
                    "question": "In which city was the Muslim League founded?",
                    "options": ["Lahore", "Dhaka", "Karachi", "Aligarh"],
                    "answer": "Dhaka"
                },
                {
                    "question": "When was Pakistan's first constitution adopted?",
                    "options": ["1947", "1956", "1962", "1973"],
                    "answer": "1956"
                },
                {
                    "question": "Who was the first Chief Justice of Pakistan?",
                    "options": ["Abdul Rashid", "Muhammad Munir", "A.R. Cornelius", "Muhammad Shahabuddin"],
                    "answer": "Abdul Rashid"
                },
                {
                    "question": "When did Pakistan become a nuclear power?",
                    "options": ["1974", "1998", "2002", "2005"],
                    "answer": "1998"
                },
                {
                    "question": "Who was the first woman Prime Minister of Pakistan?",
                    "options": ["Fatima Jinnah", "Benazir Bhutto", "Kulsoom Nawaz", "Hina Rabbani Khar"],
                    "answer": "Benazir Bhutto"
                },
                {
                    "question": "Which year was declared as the Year of Education in Pakistan?",
                    "options": ["2000", "2005", "2010", "2015"],
                    "answer": "2005"
                },
                {
                    "question": "Who designed the national flag of Pakistan?",
                    "options": ["Quaid-e-Azam", "Allama Iqbal", "Ameer-ud-Din Khidwai", "Liaquat Ali Khan"],
                    "answer": "Ameer-ud-Din Khidwai"
                },
                {
                    "question": "When was the Lahore Resolution passed?",
                    "options": ["22 March 1940", "23 March 1940", "24 March 1940", "25 March 1940"],
                    "answer": "23 March 1940"
                },
                {
                    "question": "Which Pakistani scientist is known as the 'Father of Pakistan's Nuclear Program'?",
                    "options": ["Dr. Abdul Qadeer Khan", "Dr. Abdus Salam", "Dr. Ishrat Hussain", "Dr. Atta-ur-Rahman"],
                    "answer": "Dr. Abdul Qadeer Khan"
                },
                # New questions about Pakistani map, flag, war, animal
                {
                    "question": "What are the colors of Pakistan's flag?",
                    "options": ["Green and White", "Green and Red", "White and Black", "Green and Yellow"],
                    "answer": "Green and White"
                },
                {
                    "question": "Which animal is the national animal of Pakistan?",
                    "options": ["Snow Leopard", "Markhor", "Ibex", "Asian Elephant"],
                    "answer": "Markhor"
                },
                {
                    "question": "In which year did the Indo-Pakistani War of 1971 take place?",
                    "options": ["1965", "1971", "1973", "1999"],
                    "answer": "1971"
                },
                {
                    "question": "What shape is Pakistan's map often compared to?",
                    "options": ["Triangle", "Square", "Rabbit", "Crescent"],
                    "answer": "Rabbit"
                },
                {
                    "question": "Which bird is the national bird of Pakistan?",
                    "options": ["Eagle", "Sparrow", "Chukar Partridge", "Peacock"],
                    "answer": "Chukar Partridge"
                }
            ]
        }

    def create_timeline(self, topic):
        """Create a timeline visualization for the selected topic"""
        try:
            if topic not in self.historical_data:
                return None, f"Topic '{topic}' not found."
            
            events = self.historical_data[topic]
            
            # Convert dates to datetime objects
            dates = [datetime.strptime(event['date'], '%Y-%m-%d') for event in events]
            event_names = [event['event'] for event in events]
            
            # Create the timeline
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot events on timeline
            ax.plot_date(dates, [1] * len(dates), linestyle='-', marker='o', markersize=8)
            
            # Add event labels
            for i, (date, event) in enumerate(zip(dates, event_names)):
                ax.annotate(event, (date, 1), 
                           xytext=(10, 15 + (i % 3) * 10), 
                           textcoords='offset points',
                           rotation=45,
                           fontsize=9)
            
            # Format the timeline
            ax.set_title(f'Historical Timeline: {topic}', fontsize=14, fontweight='bold')
            ax.set_yticks([])
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            ax.xaxis.set_major_locator(mdates.YearLocator(10))
            ax.grid(True, alpha=0.3)
            fig.autofmt_xdate()
            
            # Save to buffer
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            return buf, f"Timeline for {topic} generated successfully!"
            
        except Exception as e:
            return None, f"Error creating timeline: {str(e)}"

    def compare_countries(self, country1, country2):
        """Compare two countries and create visualization"""
        try:
            if country1 not in self.country_data or country2 not in self.country_data:
                return None, None, "One or both countries not found."
            
            data1 = self.country_data[country1]
            data2 = self.country_data[country2]
            
            # Create comparison DataFrame
            comparison_data = {
                'Metric': ['Area (sq km)', 'Population', 'Capital', 'Currency', 'National Animal', 'National Bird'],
                country1: [
                    f"{data1['area']:,}",
                    f"{data1['population']:,}",
                    data1['capital'],
                    data1['currency'],
                    data1.get('national_animal', 'N/A'),
                    data1.get('national_bird', 'N/A')
                ],
                country2: [
                    f"{data2['area']:,}",
                    f"{data2['population']:,}",
                    data2['capital'],
                    data2['currency'],
                    data2.get('national_animal', 'N/A'),
                    data2.get('national_bird', 'N/A')
                ]
            }
            
            df = pd.DataFrame(comparison_data)
            
            # Create comparison chart for numerical data
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Area comparison
            areas = [data1['area'], data2['area']]
            ax1.bar([country1, country2], areas, color=['green', 'orange'])
            ax1.set_title('Area Comparison (sq km)')
            ax1.set_ylabel('Square Kilometers')
            
            # Population comparison (in millions for better scaling)
            populations = [data1['population'] / 1e6, data2['population'] / 1e6]
            ax2.bar([country1, country2], populations, color=['green', 'orange'])
            ax2.set_title('Population Comparison (millions)')
            ax2.set_ylabel('Population in Millions')
            
            plt.tight_layout()
            
            # Save chart to buffer
            chart_buf = io.BytesIO()
            plt.savefig(chart_buf, format='png', dpi=150, bbox_inches='tight')
            chart_buf.seek(0)
            plt.close()
            
            return df, chart_buf, f"Comparison between {country1} and {country2} completed!"
            
        except Exception as e:
            return None, None, f"Error comparing countries: {str(e)}"

    def get_quiz_questions(self, difficulty, num_questions):
        """Get random quiz questions for the selected difficulty"""
        if difficulty not in self.questions:
            return []
        
        available_questions = self.questions[difficulty]
        return random.sample(available_questions, min(num_questions, len(available_questions)))

class DatabaseManager:
    """Manages student registration and records"""
    
    def __init__(self):
        self.conn = sqlite3.connect('students.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                grade TEXT,
                school TEXT,
                email TEXT UNIQUE,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                difficulty TEXT,
                score INTEGER,
                total_questions INTEGER,
                percentage REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        self.conn.commit()
    
    def register_student(self, name, age, grade, school, email):
        """Register a new student"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, age, grade, school, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, grade, school, email))
        self.conn.commit()
        return cursor.lastrowid
    
    def save_quiz_result(self, student_id, difficulty, score, total_questions, percentage):
        """Save quiz result for a student"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO quiz_results (student_id, difficulty, score, total_questions, percentage)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, difficulty, score, total_questions, percentage))
        self.conn.commit()
    
    def get_student_results(self, student_id):
        """Get all quiz results for a student"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT difficulty, score, total_questions, percentage, timestamp 
            FROM quiz_results 
            WHERE student_id = ? 
            ORDER BY timestamp DESC
        ''', (student_id,))
        return cursor.fetchall()
    
    def get_all_students(self):
        """Get all registered students"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT s.*, COUNT(r.id) as quiz_count, MAX(r.timestamp) as last_activity
            FROM students s
            LEFT JOIN quiz_results r ON s.id = r.student_id
            GROUP BY s.id
            ORDER BY s.registration_date DESC
        ''')
        return cursor.fetchall()
    
    def get_student_by_email(self, email):
        """Get student by email"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students WHERE email = ?', (email,))
        return cursor.fetchone()

def main():
    st.set_page_config(
        page_title="Social Studies Projects",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2ca02c;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .student-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize database and projects
    db = DatabaseManager()
    projects = SocialStudiesProjects()
    
    # Initialize session state
    if 'current_student' not in st.session_state:
        st.session_state.current_student = None
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_finished' not in st.session_state:
        st.session_state.quiz_finished = False
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "Dashboard"
    
    st.markdown('<div class="main-header">🌟 Social Studies Projects</div>', unsafe_allow_html=True)
    
    # Student registration/login section
    show_student_auth(db)
    
    # Main navigation only if student is logged in
    if st.session_state.current_student:
        show_main_navigation(projects, db)
        
        # Show the current view based on session state
        if st.session_state.current_view == "Dashboard":
            show_dashboard(projects, db)
        elif st.session_state.current_view == "Timeline Generator":
            show_timeline_generator(projects)
        elif st.session_state.current_view == "Country Comparison":
            show_country_comparison(projects)
        elif st.session_state.current_view == "History Quiz":
            show_history_quiz(projects, db)
        elif st.session_state.current_view == "My Progress":
            show_student_progress(db)
    else:
        st.warning("⚠️ Please register or login to access the learning tools.")

def show_student_auth(db):
    """Show student registration and login section"""
    st.sidebar.markdown("## 👨‍🎓 Student Portal")
    
    tab1, tab2, tab3 = st.sidebar.tabs(["Register", "Login", "Records"])
    
    with tab1:
        st.markdown("### 📝 New Registration")
        
        with st.form("registration_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=5, max_value=100, value=15)
            grade = st.selectbox("Grade", ["6th", "7th", "8th", "9th", "10th", "11th", "12th", "College", "University"])
            school = st.text_input("School/College Name")
            email = st.text_input("Email Address")
            
            if st.form_submit_button("Register"):
                if name and email:
                    try:
                        student_id = db.register_student(name, age, grade, school, email)
                        st.session_state.current_student = {
                            'id': student_id,
                            'name': name,
                            'age': age,
                            'grade': grade,
                            'school': school,
                            'email': email
                        }
                        st.success(f"🎉 Welcome {name}! Registration successful.")
                        time.sleep(1)
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("❌ Email already exists. Please use a different email or login.")
                    except Exception as e:
                        st.error(f"Registration failed: {str(e)}")
                else:
                    st.error("Please fill all required fields.")
    
    with tab2:
        st.markdown("### 🔐 Login")
        email = st.text_input("Enter your email")
        
        if st.button("Login"):
            student = db.get_student_by_email(email)
            if student:
                st.session_state.current_student = {
                    'id': student[0],
                    'name': student[1],
                    'age': student[2],
                    'grade': student[3],
                    'school': student[4],
                    'email': student[5]
                }
                st.success(f"Welcome back, {student[1]}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Student not found. Please register first.")
    
    with tab3:
        st.markdown("### 📊 All Students")
        students = db.get_all_students()
        
        if students:
            for student in students:
                with st.expander(f"🎓 {student[1]} - {student[3]} Grade"):
                    st.write(f"**Age:** {student[2]}")
                    st.write(f"**School:** {student[4]}")
                    st.write(f"**Email:** {student[5]}")
                    st.write(f"**Quizzes Taken:** {student[6]}")
                    st.write(f"**Last Activity:** {student[7]}")
        else:
            st.info("No students registered yet.")

def show_main_navigation(projects, db):
    """Show main navigation for logged-in students"""
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.current_student['name']}!")
    
    # Student info card
    student = st.session_state.current_student
    st.sidebar.markdown(f"""
    <div class="student-card">
        <strong>🎓 Student Info</strong><br>
        Name: {student['name']}<br>
        Grade: {student['grade']}<br>
        School: {student['school']}<br>
        Age: {student['age']}
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation selectbox that updates session state
    options = ["Dashboard", "Timeline Generator", "Country Comparison", "History Quiz", "My Progress"]
    new_view = st.sidebar.selectbox(
        "📚 Choose Learning Tool",
        options,
        index=options.index(st.session_state.current_view)
    )
    
    # Update session state if selection changed
    if new_view != st.session_state.current_view:
        st.session_state.current_view = new_view
        st.rerun()
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.current_student = None
        st.session_state.quiz_started = False
        st.session_state.quiz_finished = False
        st.session_state.current_view = "Dashboard"
        st.rerun()

def show_dashboard(projects, db):
    """Show student dashboard"""
    st.markdown('<div class="section-header">🏠 Student Dashboard</div>', unsafe_allow_html=True)
    
    # Welcome message
    student = st.session_state.current_student
    st.success(f"🌟 Welcome to your learning portal, {student['name']}!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Quick Stats")
        
        # Get student results
        results = db.get_student_results(student['id'])
        
        if results:
            total_quizzes = len(results)
            total_correct = sum([r[1] for r in results])
            total_questions = sum([r[2] for r in results])
            avg_score = (total_correct / total_questions) * 100 if total_questions > 0 else 0
            best_score = max([r[1] for r in results]) if results else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Quizzes", total_quizzes)
            with col2:
                st.metric("Average Score", f"{avg_score:.1f}%")
            with col3:
                st.metric("Best Score", f"{best_score} points")
            
            # Recent activity
            st.markdown("### 📈 Recent Activity")
            for result in results[:3]:
                st.write(f"**{result[0]} Quiz:** {result[1]}/{result[2]} ({result[3]:.1f}%) - {result[4]}")
        else:
            st.info("🎯 Take your first quiz to see your progress here!")
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("📅 Start Timeline Generator", use_container_width=True):
            st.session_state.current_view = "Timeline Generator"
            st.rerun()
        
        if st.button("🌍 Compare Countries", use_container_width=True):
            st.session_state.current_view = "Country Comparison"
            st.rerun()
        
        if st.button("❓ Take a Quiz", use_container_width=True):
            st.session_state.current_view = "History Quiz"
            st.rerun()
    
    # Learning resources
    st.markdown("---")
    st.markdown("### 📖 Learning Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🇵🇰 Pakistan Facts")
        st.write("• National Animal: Markhor")
        st.write("• National Bird: Chukar Partridge")
        st.write("• National Sport: Hockey")
        st.write("• Longest River: Indus")
    
    with col2:
        st.markdown("#### 🏛️ Historical Events")
        st.write("• Independence: 14 Aug 1947")
        st.write("• Pakistan Resolution: 23 Mar 1940")
        st.write("• First Constitution: 1956")
        st.write("• Nuclear Power: 1998")
    
    with col3:
        st.markdown("#### 🗺️ Geography")
        st.write("• Area: 881,913 sq km")
        st.write("• Population: 242 million")
        st.write("• Provinces: 4")
        st.write("• Capital: Islamabad")

def show_timeline_generator(projects):
    """Show timeline generator section"""
    st.markdown('<div class="section-header">📅 Historical Timeline Generator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        topic = st.selectbox(
            "Select Historical Topic",
            list(projects.historical_data.keys())
        )
        
        if st.button("Generate Timeline"):
            with st.spinner("Creating timeline..."):
                image_buf, message = projects.create_timeline(topic)
                
                if image_buf:
                    st.success(message)
                    st.image(image_buf, use_column_width=True)
                    
                    # Show event details
                    st.markdown("### 📋 Event Details")
                    events = projects.historical_data[topic]
                    for event in events:
                        st.write(f"**{event['event']}** - {event['date']}")
                else:
                    st.error(message)
    
    with col2:
        st.markdown("### ℹ️ About Timeline Generator")
        st.write("This tool creates visual timelines of historical events. Select a topic from the dropdown and click 'Generate Timeline' to see the timeline.")
        st.write("**Available events for each topic:**")
        
        for topic_name, events in projects.historical_data.items():
            st.write(f"**{topic_name}:**")
            for event in events:
                st.write(f"- {event['event']} ({event['date']})")

def show_country_comparison(projects):
    """Show country comparison section"""
    st.markdown('<div class="section-header">🌍 Country Comparison Tool</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        country1 = st.selectbox(
            "Select First Country",
            list(projects.country_data.keys()),
            key="country1"
        )
        
        # Display country facts
        st.markdown(f"### 🇵🇰 {country1} Facts")
        data = projects.country_data[country1]
        st.write(f"**Area:** {data['area']:,} sq km")
        st.write(f"**Population:** {data['population']:,}")
        st.write(f"**Capital:** {data['capital']}")
        st.write(f"**Currency:** {data['currency']}")
        st.write(f"**National Animal:** {data.get('national_animal', 'N/A')}")
    
    with col2:
        country2 = st.selectbox(
            "Select Second Country",
            list(projects.country_data.keys()),
            index=1,
            key="country2"
        )
        
        # Display country facts
        st.markdown(f"### 🇮🇳 {country2} Facts")
        data = projects.country_data[country2]
        st.write(f"**Area:** {data['area']:,} sq km")
        st.write(f"**Population:** {data['population']:,}")
        st.write(f"**Capital:** {data['capital']}")
        st.write(f"**Currency:** {data['currency']}")
        st.write(f"**National Animal:** {data.get('national_animal', 'N/A')}")
    
    if st.button("Compare Countries"):
        if country1 == country2:
            st.warning("Please select two different countries for comparison.")
        else:
            with st.spinner("Comparing countries..."):
                comparison_df, chart_buf, message = projects.compare_countries(country1, country2)
                
                if comparison_df is not None:
                    st.success(message)
                    
                    # Display comparison table
                    st.markdown("### 📊 Comparison Table")
                    st.dataframe(comparison_df, use_container_width=True)
                    
                    # Display comparison chart
                    if chart_buf:
                        st.markdown("### 📈 Visual Comparison")
                        st.image(chart_buf, use_column_width=True)
                else:
                    st.error(message)

def show_history_quiz(projects, db):
    """Show history quiz section"""
    st.markdown('<div class="section-header">❓ History Quiz Bot</div>', unsafe_allow_html=True)
    
    if not st.session_state.quiz_started:
        show_quiz_setup(projects)
    else:
        if st.session_state.quiz_finished:
            show_quiz_results(projects, db)
        else:
            show_quiz_question(projects)

def show_quiz_setup(projects):
    """Show quiz setup interface"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Quiz Setup")
        difficulty = st.selectbox(
            "Select Difficulty Level",
            ["Easy", "Medium", "Hard"]
        )
        
        num_questions = st.slider(
            "Number of Questions",
            min_value=3,
            max_value=15,
            value=5
        )
        
        if st.button("Start Quiz"):
            st.session_state.quiz_questions = projects.get_quiz_questions(difficulty, num_questions)
            st.session_state.quiz_difficulty = difficulty
            st.session_state.total_questions = len(st.session_state.quiz_questions)
            st.session_state.quiz_score = 0
            st.session_state.current_question = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_started = True
            st.session_state.quiz_finished = False
            st.rerun()
    
    with col2:
        st.markdown("### 📊 Difficulty Info")
        st.write("**Easy:** Basic facts about Pakistan")
        st.write("**Medium:** Intermediate historical knowledge") 
        st.write("**Hard:** Advanced historical details")
        st.write(f"**Questions available:** 10+ per difficulty")
        
        # Show new questions info
        st.markdown("### 🆕 New Questions")
        st.write("• Pakistan Flag colors")
        st.write("• National Animal (Markhor)")
        st.write("• 1971 War details")
        st.write("• Pakistan Map shape")
        st.write("• National Bird")

def show_quiz_question(projects):
    """Show individual quiz questions"""
    current_q = st.session_state.current_question
    total_q = st.session_state.total_questions
    question_data = st.session_state.quiz_questions[current_q]
    
    st.markdown(f"### ❓ Question {current_q + 1} of {total_q}")
    st.markdown(f"**{question_data['question']}**")
    
    # Store the answer options
    options = question_data['options']
    
    # Create radio buttons for options
    user_answer = st.radio(
        "Select your answer:",
        options,
        key=f"q{current_q}"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⏭️ Next Question", use_container_width=True):
            # Store the answer
            st.session_state.quiz_answers[current_q] = user_answer
            
            if current_q < total_q - 1:
                st.session_state.current_question += 1
                st.rerun()
            else:
                calculate_final_score()
                st.session_state.quiz_finished = True
                st.rerun()
    
    with col2:
        if st.button("🔄 Restart Quiz", use_container_width=True):
            reset_quiz()

def calculate_final_score():
    """Calculate the final quiz score"""
    score = 0
    for i, question_data in enumerate(st.session_state.quiz_questions):
        user_answer = st.session_state.quiz_answers.get(i, "")
        if user_answer == question_data['answer']:
            score += 1
    st.session_state.quiz_score = score

def show_quiz_results(projects, db):
    """Show quiz results"""
    score = st.session_state.quiz_score
    total = st.session_state.total_questions
    percentage = (score / total) * 100
    
    st.markdown("### 📊 Quiz Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Questions", total)
    with col2:
        st.metric("Correct Answers", score)
    with col3:
        st.metric("Percentage", f"{percentage:.1f}%")
    
    # Save result to database
    if st.session_state.current_student:
        db.save_quiz_result(
            st.session_state.current_student['id'],
            st.session_state.quiz_difficulty,
            score,
            total,
            percentage
        )
    
    # Performance message
    if percentage >= 80:
        st.success("🎉 Excellent performance! You're a history expert!")
    elif percentage >= 60:
        st.info("👍 Good performance! You have solid historical knowledge!")
    else:
        st.warning("💪 Keep practicing! History is interesting to learn!")
    
    # Show answers review
    st.markdown("### 📝 Review Answers")
    for i, question_data in enumerate(st.session_state.quiz_questions):
        user_answer = st.session_state.quiz_answers.get(i, "Not answered")
        correct_answer = question_data['answer']
        
        with st.expander(f"Question {i+1}: {question_data['question']}"):
            if user_answer == correct_answer:
                st.success(f"✅ Your answer: {user_answer} (Correct)")
            else:
                st.error(f"❌ Your answer: {user_answer}")
                st.success(f"✅ Correct answer: {correct_answer}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Quiz"):
            reset_quiz()
    with col2:
        if st.button("📊 View My Progress"):
            st.session_state.current_view = "My Progress"
            st.rerun()

def show_student_progress(db):
    """Show student progress section"""
    st.markdown('<div class="section-header">📈 My Learning Progress</div>', unsafe_allow_html=True)
    
    student = st.session_state.current_student
    results = db.get_student_results(student['id'])
    
    if results:
        # Progress statistics
        total_quizzes = len(results)
        total_questions = sum([r[2] for r in results])
        correct_answers = sum([r[1] for r in results])
        overall_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Quizzes", total_quizzes)
        with col2:
            st.metric("Total Questions", total_questions)
        with col3:
            st.metric("Correct Answers", correct_answers)
        with col4:
            st.metric("Overall Score", f"{overall_percentage:.1f}%")
        
        # Quiz history
        st.markdown("### 📋 Quiz History")
        for result in results:
            with st.expander(f"{result[0]} Quiz - {result[4]}"):
                st.write(f"**Score:** {result[1]}/{result[2]}")
                st.write(f"**Percentage:** {result[3]:.1f}%")
                st.write(f"**Date:** {result[4]}")
                
                # Progress bar
                progress = result[1] / result[2]
                st.progress(progress)
    else:
        st.info("📚 You haven't taken any quizzes yet. Start learning by taking a quiz!")

def reset_quiz():
    """Reset quiz state"""
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.current_question = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answers = {}
    st.rerun()

if __name__ == "__main__":
    main()