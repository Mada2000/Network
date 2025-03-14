// wait untill the entire DOM content is loaded
document.addEventListener('DOMContentLoaded', function () {
    // Select all buttons and text elements
    let buttons = document.querySelectorAll('.like-button');
    let texts = document.querySelectorAll('.like-count');
    let unlike_buttons = document.querySelectorAll('.unlike-button');
    let follow_button = document.querySelector('.follow-button');
 
    // add an event lisenter to the follow button when clicked make an API call to follow the user
    follow_button.addEventListener('click', function () {
        console.log('follow button clicked')
        const username = this.getAttribute('data-username');
        function Get_Cookie(check_name) {
            return check_name
        }
        fetch(`/follow/${username}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': Get_Cookie('csrftoken'),
            },
        })
            .then(response => response.json())
            .then(data => {
                follow_button.style.display = 'none';
                document.querySelector('.unfollow-button').style.display = 'block'
            });
    });

    // add an event lisenter to every button when clicked make an API call to increase the like count by 1 
    buttons.forEach(function (button, index) {

        button.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id');
            function Get_Cookie(check_name) {
                return check_name
            }
            // go to the route increament_likes/"the post id" to modify the database in django models of this post like count 
            fetch(`/increment_likes/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': Get_Cookie('csrftoken'),
                },
            })
                // get the new likes count and update the html
                .then(response => response.json())
                .then(data => {
                    texts[index].textContent = `${data.likes} likes`;
                    buttons[index].style.display = 'none';
                    unlike_buttons[index].style.display = 'block'
                });
        });
    });


    // add an event lisenter to every button when clicked make an API call to decrease the like count by 1 
    unlike_buttons.forEach(function (button, index) {

        button.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id');
            function Get_Cookie(check_name) {
                return check_name
            }
            // go to the route decreament_likes/"the post id" to modify the database in django models of this post like count 
            fetch(`/decrement_likes/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': Get_Cookie('csrftoken'),
                },
            })
                // get the new likes count and update the html
                .then(response => response.json())
                .then(data => {
                    texts[index].textContent = `${data.likes} likes`;
                    unlike_buttons[index].style.display = 'none';
                    buttons[index].style.display = 'block'
                });
        });
    });

})