import requests

def main():
    login_res = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        json={"email": "mrigeshdeshpande246@gmail.com", "password": "Mrigesh@123"}
    )
    token = login_res.json()["access_token"]
    
    course_res = requests.post(
        "http://localhost:8000/api/v1/academy/catalog/courses",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Course 2"}
    )
    print("Status:", course_res.status_code)
    print("Response:", course_res.text)

if __name__ == "__main__":
    main()
