<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Quiz App Description</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        h1, h2 {
            color: #333;
        }
        p, ul, ol {
            margin-bottom: 20px;
        }
        ul, ol {
            padding-left: 20px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 4px;
            font-family: monospace;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Django Quiz App</h1>
    <p>The Django Quiz App is a customizable web application for creating and managing quizzes. With this app, you can easily create quizzes with multiple-choice questions, track user responses, and analyze quiz results.</p>
    
    <h2>Features</h2>
    <ul>
        <li>Quiz Creation: Create quizzes with custom titles, descriptions, and time limits.</li>
        <li>Multiple-Choice Questions: Add multiple-choice questions with options and correct answers.</li>
        <li>User Authentication: Require users to log in to take quizzes, allowing for personalized experiences.</li>
        <li>Quiz Attempt Tracking: Track user attempts for each quiz, including the submitted answers and scores.</li>
        <li>Real-Time Timer: Display a real-time countdown timer for quizzes with time limits.</li>
        <li>Result Analysis: Analyze quiz results, including overall scores, correct answers, and detailed feedback for each question.</li>
        <li>Responsive Design: Ensure a seamless user experience across devices with a responsive design.</li>
    </ul>
    
    <h2>Installation</h2>
    <ol>
        <li>Clone the repository: <code>git clone https://github.com/your-username/django-quiz-app.git</code></li>
        <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
        <li>Apply database migrations: <code>python manage.py migrate</code></li>
        <li>Run the development server: <code>python manage.py runserver</code></li>
        <li>Access the application at <a href="http://localhost:8000">http://localhost:8000</a>.</li>
    </ol>
    
    <h2>Usage</h2>
    <ol>
        <li>Create a superuser to access the admin interface: <code>python manage.py createsuperuser</code></li>
        <li>Log in to the admin interface (<a href="http://localhost:8000/admin">http://localhost:8000/admin</a>) to create quizzes and questions.</li>
        <li>Share the quiz links with users, and they can start taking quizzes immediately.</li>
    </ol>
</body>
</html>
