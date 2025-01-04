//Fetch API
async function getUsers() {
    json = await fetch(`/user`).then(response => response.json());
    createUserInfo(json.users)
    createdByOption(json.users)
}

async function getCourses() {
    response = await Promise.all([fetch(`/courses`), fetch(`/enrollment`)])
    courses = await response[0].json()
    enrollment = await response[1].json()
    createCourseInfo(courses.courses, enrollment.enrollment)
}

async function enrollNavEvent() {
    response = await Promise.all([fetch(`/courses`), fetch(`/user`)])
    courses = await response[0].json()
    users = await response[1].json()
    EnrollmentOption(users.users, courses.courses)
}


// Create/Manipulate HTML Components
function createUserInfo(users) {
    userTable = document.getElementById("users-list");
    userSelect = document.getElementById("user-select");
    createdBy = document.getElementById("created-by");
    if (userTable.children.length == 0) {

        users.forEach(user => {
            userSelect.innerHTML += `<option value=${user.id}>${user.username}</option>`;
            row = document.createElement("tr")

            date = new Date(user.last_login).toString()
            row.innerHTML += `<td> ${user.username} </td>`
            row.innerHTML += `<td> ${user.email} </td>`
            if (user.user_type == "admin") row.innerHTML += `<th> ${user.user_type} </th>`
            else row.innerHTML += `<td> ${user.user_type} </td>`
            row.innerHTML += `<td> ${date.substr(4, 20)} </td>`

            userTable.appendChild(row)
        });
    }
}

function createdByOption(users) {
    createdBy = document.getElementById("created-by");
    if (createdBy.children.length == 0) {
        users.forEach(user => {
            if (user.user_type == "teacher")
                createdBy.innerHTML += `<option value=${user.id}>${user.username}</option>`;
        })
    }
}

function EnrollmentOption(users, courses) {
    enrolledBy = document.getElementById("enrolled-by");
    coursesList = document.getElementById("enroll-courses-list");
    if (coursesList.children.length == 0) {
        users.forEach(user => {
            enrolledBy.innerHTML += `<option value=${user.id}>${user.username}</option>`;
        })
        courses.forEach(course => {
            console.log(course.title)
            coursesList.innerHTML += `<option value=${course.id}>${course.title}</option>`;
        })
    }

}

function createCourseInfo(courses, enrollment = []) {
    courseTable = document.getElementById("courses-list");
    courseSelect = document.getElementById("course-select");
    if (courseTable.children.length == 0) {

        courses.forEach(course => {
            enrollment_count = enrollment.filter(enroll => enroll.course_id === course.id).length
            courseSelect.innerHTML += `<option value=${course.id}>${course.title}</option>`;
            row = document.createElement("tr")

            date = new Date(course.last_login).toString()
            row.innerHTML += `<td> ${course.title} </td>`
            row.innerHTML += `<td> ${course.created_by} </td>`
            row.innerHTML += `<td> ${enrollment_count} </td>`


            courseTable.appendChild(row)
        });
    }
}


// Delete User Button Event
document.getElementById("delete-user-btn").addEventListener("click", (e) => {
    console.log("GG")
    userId = document.getElementById("user-select").value;
    base_url = window.location.origin
    window.location.href = `${base_url}/user/delete?id=${userId}`
})

