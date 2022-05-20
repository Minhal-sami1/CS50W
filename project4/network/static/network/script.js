// Start with first post
var counter = 0;

// Load posts 20 at a time
const quantity = 5;


document.addEventListener("DOMContentLoaded", ()=> {
    
    

    document.addEventListener("click", (event)=>{
        
        let csrftoken = getCookie('csrftoken');
        const element = document.createElement('div');
        element.role = "alert";
        element.className = "alert alert-info";
        element.id = "success";
        element.style.display = "none";
        
        const target = event.target;

        if(target.id === "like" || target.parentElement.id === "like" || target.parentElement.parentElement.id === "like" ){
            const liker = target.dataset.user;
            const liketo = target.dataset.post;
            fetch(`/dolike/${liker}/${liketo}`)
            .then(response => response.json())
            .then(result => {
                if (result["already"] === "FALSE") {
                    dolike(liker, liketo, target, csrftoken, element);
                }else{
                    dounlike(liker, liketo, target, csrftoken, element);
                }
            }
            );
            
        }


        if (target.id == "editpost"){
            const contents = document.querySelector("#id_edit_data").value;
            const post_id = document.querySelector("#editpost").dataset.post;
            fetch(`/editpost/${post_id}/`,{
                method:"POST",
                body: JSON.stringify(contents),
                headers: { 'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken }, 
            }).then(response => response.json())
            .then(result => {
                const message = result["message"];
                
                if (message == "Post Edited Successfully!"){
                    const change = document.querySelector("#editedpost");
                    change.innerHTML = `<h5 class="card-title"><a href = "/profile/${target.dataset.ownerid}">${target.dataset.user}</a></h5>
    
    
    
    <p class="card-text">${contents}</p>
    <hr>
    <small class="text-muted">${target.dataset.time}</small>
    
    <br>
    
    <button href="#" class="btn btn-outline-danger" id = "like" data-post = "${target.dataset.post}" data-user="${target.dataset.ownerid}" data-status = "">0
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-half" viewBox="0 0 16 16">
        <path d="M8 2.748v11.047c3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
      </svg>
    </button>
    
    <button type="button" id = "edit" data-post = "${post_id}" data-contents = "${contents}" data-ownerid = "${target.dataset.ownerid}" data-user = "${target.dataset.user}" data-time = "${target.dataset.time}" data-likes = "${target.dataset.likes}" class="btn btn-outline-warning">Edit</button>
    `;
                change.id = "edit";
                }
                document.querySelector('#alert').append(element);
                element.innerHTML = message;
                element.style.display = "block";
                element.style.animationPlayState = 'running';
                setTimeout(function () {
                    element.remove()
               }, 4100)
            });

        }
        
        if(target.id == "post"){
            const textarea = document.querySelector("#id_data");
            fetch("/post/",{
                method:"PUT",
                body: JSON.stringify(textarea.value),
                headers: { 'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken }, 
            }).then(response => response.json())
            .then(result => {
                const message = result["message"];
                console.log(result)
                document.querySelector('#alert').append(element);
                element.innerHTML = message;
                element.style.display = "block";
                element.style.animationPlayState = 'running';
                load();
                setTimeout(function () {
                    element.remove()
                }, 4100)
                textarea.value = "";
            });
            
        }
        if(target.id == "edit"){
            const contents = target.dataset.contents;
            target.parentElement.className = "";
            target.parentElement.innerHTML = `<div class="card-body" id = "editedpost">
                                        <h5 class="card-header">Edit Post</h5>
                                         <textarea name="data" cols="5" rows="6" class="form-control form-control-lg" placeholder="Post here!" maxlength="300" required id="id_edit_data">${contents}</textarea>
                                        <br>
                                        <button id="editpost" data-post = "${target.dataset.post}" data-ownerid = "${target.dataset.ownerid}" data-user = "${target.dataset.user}" data-time = "${target.dataset.time}" data-likes = "${target.dataset.likes}" class="btn btn-outline-danger">Save!</button>`;
            //const another = document.querySelector(`#${target.dataset.post}`);
            //another.append(upper_div);

        }


        if(target.id =="follow"){
            const follower = target.dataset.follower;
            const following = target.dataset.following;
            const do_what = target.dataset.do;
            fetch(`/dofollow/${follower}/${following}/${do_what}`)
            .then(response => response.json())
            .then(result => {
                console.log(result)
                if(result["message"] == "Follow"){
                    document.querySelector("#follow").innerHTML = "Follow";
                    document.querySelector("#follow").dataset.do = "follow";
                }else{
                    document.querySelector("#follow").innerHTML = "Unfollow";
                    document.querySelector("#follow").dataset.do = "unfollow";
                }
            });

        }
        
        if(target.id == "post"){
            const textarea = document.querySelector("#id_data");
            fetch("/post/",{
                method:"PUT",
                body: JSON.stringify(textarea.value),
                headers: { 'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken }, 
            }).then(response => response.json())
            .then(result => {
                const message = result["message"];
                console.log(result)
                document.querySelector('#alert').append(element);
                element.innerHTML = message;
                element.style.display = "block";
                element.style.animationPlayState = 'running';
                load();
                setTimeout(function () {
                    element.remove()
                }, 4100)
                textarea.value = "";
            });

            
        }
    })
})

//window.onscroll = () => {
  //  if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    //    load();
   // }
// };


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function dounlike(liker, liketo, target, csrftoken, element) {

                fetch(`/dolike/${liker}/${liketo}/`,{
                            method:"PUT",
                            body: JSON.stringify("UNLIKE"),
                            headers: { 'Accept': 'application/json, text/plain, */*',
                            'Content-Type': 'application/json',
                            "X-CSRFToken": csrftoken }, 
                        }).then(response => response.json())
                        .then(result => {
                            message = result["message"];
                            const likes = target.children;
                            likes[0].innerHTML = parseInt(likes[0].innerHTML)-1;
                            
                            document.querySelector('#alert').append(element);
                            element.innerHTML = message;
                            element.style.display = "block";
                            element.style.animationPlayState = 'running';
                            setTimeout(function () {
                                element.remove()
                            }, 4100)});
    
}

function dolike(liker, liketo, target, csrftoken, element) {

                fetch(`/dolike/${liker}/${liketo}/`,{
                            method:"PUT",
                            body: JSON.stringify("LIKE"),
                            headers: { 'Accept': 'application/json, text/plain, */*',
                            'Content-Type': 'application/json',
                            "X-CSRFToken": csrftoken }, 
                        }).then(response => response.json())
                        .then(result => {
                            message = result["message"];
                            const likes = target.children;
                            likes[0].innerHTML = parseInt(likes[0].innerHTML)+1;
                            
                            document.querySelector('#alert').append(element);
                            element.innerHTML = message;
                            element.style.display = "block";
                            element.style.animationPlayState = 'running';
                            setTimeout(function () {
                                element.remove()
                            }, 4100)});
    
}

function add_post(contents) {
    if(contents !== "ENDED"){
        // Creating new post elements
        const post_cont = document.createElement('div');
        post_cont.className = 'card text-center mx-auto col-6';
        post_cont.style.margin = "15px"
        
        const card_header = document.createElement("h5");
        card_header.className = "card-title";
        const profile_link = document.createElement('a');
        profile_link.href = `/profile/${contents[0]}`;
        
        const card_body = document.createElement("div");
        card_body.className = "card-body";
        
        const card_footer = document.createElement("div");
        card_footer.innerHTML = "<hr>";
        
        const card_text = document.createElement("p");
        card_text.className = "card-text";
        
        const card_date = document.createElement("small");
        card_date.className = "text-muted";
        
        const card_end = document.createElement("div");
        
        
        const card_button = document.createElement("button");
        card_button.className = "btn btn-outline-danger";
            
        
        // adding content to post elements
        card_text.innerHTML = contents[2];
        card_date.innerHTML = contents[3];
        card_button.innerHTML = `0    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-half" viewBox="0 0 16 16">
        <path d="M8 2.748v11.047c3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
        </svg>`;
        card_button.style.margin = "5px";
        
        const user = document.querySelector("#hidden").innerHTML;
        
        if (user === "1"){            
            profile_link.innerHTML = contents[1];
            card_header.appendChild(profile_link)
            card_end.appendChild(card_button)
        }else{
            card_header.innerHTML = contents[1];
        }
        // Structuring the card
        card_body.appendChild(card_header);
        card_body.appendChild(card_text);
        card_footer.appendChild(card_date);
        card_body.appendChild(card_footer);
        card_body.appendChild(card_end);
        
        post_cont.appendChild(card_body);
        
        // Add post to DOM
        document.querySelector('#newposts').append(post_cont);
    }else{
        document.querySelector("#ended").innerHTML = `<div class="card text-white bg-dark mb-5 col-6 text-center mx-auto" style="max-width: 18rem;">
        <div class="card-header">Message</div>
        <div class="card-body">
    <h5 class="card-title">The posts have been ended</h5>
    <p class="card-text">No more posts found!</p>
    </div>
    </div>`;
}
console.log(contents)
};

// Update the Counter!
//fetch("/getcounter/")
//.then(response => response.json())
//.then(data => 
  //  {
    //    counter = data["counter"];
        
   // }
   // )
    // Load next set of posts
function load() {
    // Set start and end post numbers, and update counter
        const start = counter - 1;
        const end = start - quantity + 1;
        counter = end+1;
        console.log(`start: ${start}; end: ${end}; counter: ${counter}`);
    
        // Get new posts and add posts
        fetch(`/getposts?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
            if(data !=="ENDED"){
                console.log(data)
                Object.keys(data).reverse().forEach(element => {
                    add_post(data[element])
                });
            }
            
        })
    };