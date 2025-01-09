
console.log("Hello world")
window.onload = () => {
    fetch('/courses')
        .then(response => response.json())  // Parse JSON response
        .then(coursesData => {
            console.log(coursesData);  // Log the data to the console

        })
        .catch(error => console.error('Error fetching courses:', error));  // Error handling
};