$(document).ready(function(){
    $('#menu').click(function(){
        $(this).toggleClass('fa-times')
        $('.navbar').toggleClass('nav-toggle')
    })
    $('#login').click(function(){
        $('.login-form').addClass('popup');

    })
    $('.login-form form .fa-times').click(function(){
        $('.login-form').removeClass('popup');
    })
    $(window).on('load scroll',function(){
        $('#menu').removeClass('fa-times')
        $('.navbar').removeClass('nav-toggle')
        $('.login-form').removeClass('popup');

    })
});




// Assuming we have a role to check
let userRole = 'teacher'// Can be 'teacher' or 'student'
let enrollmentStatus = [true, false, true, false]; // An array representing whether the student is enrolled in each course (true = enrolled, false = not enrolled)

function updateButtonsForStudent() {
    // Loop through 4 courses (1 to 4)
    for (let i = 1; i <= 4; i++) {
        // Check enrollment status for each course
        if (enrollmentStatus[i - 1]) { // If the student is enrolled (true)
            document.getElementById('enroll-button-' + i).style.display = 'none'; // Hide Enroll button
            document.getElementById('completed-button-' + i).style.display = 'inline-block'; // Show Completed button
        } else {
            document.getElementById('enroll-button-' + i).style.display = 'inline-block'; // Show Enroll button
            document.getElementById('completed-button-' + i).style.display = 'none'; // Hide Completed button
        }

        // Hide the Edit button for the student
        document.getElementById('edit-button-' + i).style.display = 'none';
    }
}

function updateButtonsForTeacher() {
    // Loop through 4 courses (1 to 4)
    for (let i = 1; i <= 4; i++) {
        // Hide the Enroll and Completed buttons for the teacher
        document.getElementById('enroll-button-' + i).style.display = 'none';
        document.getElementById('completed-button-' + i).style.display = 'none';
        
        // Show the Edit button for the teacher
        document.getElementById('edit-button-' + i).style.display = 'inline-block';
    }
}

// Assuming the user is a student
if (userRole === 'student') {
    updateButtonsForStudent();
} else if (userRole === 'teacher') {
    updateButtonsForTeacher();
}
