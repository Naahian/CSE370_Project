
//Fetch API
async function getUsers() {
    json = await fetch(`/users`).then(response => response.json());
    createUserInfo(json.users)
    createdByOption(json.users)
}

async function getCourses() {
    response = await Promise.all([fetch(`/courses`), fetch(`/enrollments`)])
    courses = await response[0].json()
    enrollment = await response[1].json()
    createCourseInfo(courses.courses, enrollment.enrollment)
}



async function getStudentCourses() {
    json = await fetch(`/enrollments?user_id=${window.djangoVars.userId}`).then(response => response.json());
    createEnrollInfo(json.enrollment)
}

async function enrollNavEvent() {
    response = await Promise.all([fetch(`/courses`), fetch(`/users`)])
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


function createCourseInfo(courses, enrollment = []) {
    courseTable = document.getElementById("courses-list");
    courseSelect = document.getElementById("course-select");
    if (courseTable.children.length == 0) {

        courses.forEach(course => {
            console.log(course)
            enrollment_count = enrollment.filter(enroll => enroll.course.id === course.id).length
            courseSelect.innerHTML += `<option value=${course.id}>${course.title}</option>`;
            row = document.createElement("tr")

            date = new Date(course.last_login).toString()
            row.innerHTML += `<td> ${course.title} </td>`
            row.innerHTML += `<td> ${course.created_by__username} </td>`
            row.innerHTML += `<td> ${enrollment_count} </td>`


            courseTable.appendChild(row)
        });
    }
}

function createEnrollInfo(enrollment = []) {
    courseTable = document.getElementById("courses-list");
    courseSelect = document.getElementById("course-select");
    if (courseTable.children.length == 0) {

        enrollment.forEach(enroll => {

            courseSelect.innerHTML += `<option value=${enroll.course.id}>${enroll.course.title}</option>`;
            row = document.createElement("tr")

            row.innerHTML += `<td> ${enroll.course.title} </td>`
            row.innerHTML += `<td> ${enroll.course.created_by} </td>`



            courseTable.appendChild(row)
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
            coursesList.innerHTML += `<option value=${course.id}>${course.title}</option>`;
        })
    }

}

// Delete User Button Event
document.getElementById("delete-user-btn").addEventListener("click", (e) => {
    userId = document.getElementById("user-select").value;
    base_url = window.location.origin
    window.location.href = `${base_url}/users/delete?id=${userId}`
    console.log(`deleted user ${courseId}`)
})

// Delete Course Button Event
document.getElementById("delete-course-btn").addEventListener("click", (e) => {
    courseId = document.getElementById("course-select").value;
    base_url = window.location.origin
    window.location.href = `${base_url}/courses/delete?id=${courseId}`
    console.log(`deleted course ${courseId}`)
})
