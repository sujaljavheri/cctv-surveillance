# Real-Time CCTV Surveillance System

This project is a real-time CCTV surveillance system with face recognition. It includes a Python backend and a React frontend.

---

## Features

* Add faces to the database
* Perform face recognition
* Delete a person from the database
* Web-based frontend interface

---

## Project Structure

```
real_time_cctv/
│
├── add_faces.py
├── test.py
├── delete_person.py
├── server.py
├── my-react-app/
```

---

## Setup

Clone the repository:

```
git clone https://github.com/sujaljavheri/cctv-surveillance.git
cd real_time_cctv
```

---

## Usage

### Add Faces

Run the following command from the root directory:

```
python add_faces.py
```

---

### Test Recognition

```
python test.py
```

---

### Delete a Person

```
python delete_person.py
```

---

### Start Backend Server

```
python server.py
```

---

### Start Frontend

```
cd my-react-app
npm install
npm run dev
```

---

## Notes

* Run all Python files from the root directory
* Make sure the backend server is running before starting the frontend
* Ensure required dependencies are installed
