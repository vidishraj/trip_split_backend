# 🧳 trip_split

**trip_split** is a free alternative to the popular expense-splitting app, SplitWise. Inspired by the limitations of SplitWise, such as ads and the lack of free features, trip_split allows users to easily split expenses with friends. 

Splitwise is a popular app that enables consumers to share the costs of bills among friends. By ensuring that everyone who pays is reimbursed accurately and minimizing the number of transactions, Splitwise simplifies the expense-splitting process.

## 🌐 Live Site
Check out the live version of the application here: [Trip_Split Live Site](https://trips-split.netlify.app/)  

## 💼 Project Flow

1. **Login**: Users can securely log in to their accounts.
2. **Create a Trip**: Users can create a trip and select up to three different currencies to be used during the trip.
3. **Add Users**: Invite friends or group members to the trip.
4. **Add Expenses**: Expenses can be added in any of the three currencies chosen for the trip, which will then be converted into all currencies using **LIVE CURRENCY RATES** (a key feature).
5. **View Balances**: Users can see their balances, indicating the amounts they owe or are owed.
6. **Total Expenses**: View the total expenses for the trip and analyze, edit, or delete expenses as needed.

## 🛠️ Technologies Used
- **Backend**: Flask (for handling API requests and backend logic)
- **Database**: MySQL (for data storage)
- **Server**: Linux (for hosting the application)
- **Web Server**: Nginx (for serving the application)
## 🛠️ Installation

### 📂 Cloning the Project

- **master** (Backend): Contains the Flask-based backend.

### Backend (Flask) Setup

1. Clone the backend code from the backend branch:
```bash
   git clone https://github.com/vidishraj/trip_split_backend.git
   cd trip_split_backend
  ```
2. Set up a virtual environment:
```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows use venv\Scripts\activate
  ```
3. Install the Python dependencies:
```bash
  pip install -r requirements.txt
```
4. Configure the database connection: <br></br>
  Open the db_connector.py file and add your database information.

5. Run the Flask app:
```bash
    flask run
```
  
## 🎯 Future Improvements
- Restrict available trips to the users who created them.
- Add notifications for changes made to a trip.
