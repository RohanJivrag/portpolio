
var pos="odd";
routes = []; 

fetch('/fetchcourses')
    .then(response => response.json())
    .then(coursesData => {
        var dest = document.getElementById('container');

        coursesData.forEach(course => {
            // Extract course details
            var name =course.course_name;
            let newStr = name.replace(/ /g,"");
            var price = course.course_price;
            // var desc="xyz clasess";
            var id=course.course_id;

            var imageurl = `data:image/jpeg;base64,${course.image_data}`;


            // Create a new div element
            var newDiv = document.createElement('div');
            newDiv.classList.add('new-div');

            // Create and set up the details div
            var details = document.createElement("div");
            details.innerHTML = "<h1>  " + name + "</h1> <p> This course ID is "+ id +" and Price is <strong>"+price+'/-</strong> </p>'//<a type"buttun" href="/buy" id="buy-btn">Buy Now</a>';
            details.style.marginLeft="30px";
            
            buy=document.createElement("a");
            buy.href=`/add${newStr}`;
            buy.id="buy-btn"
            buy.innerHTML="Buy Now";
            addRoute(`/add${newStr}`, 'contact', 'contact.html');
            

            // Create and set up the image element
            var thumbnail = document.createElement('img');
            thumbnail.classList.add("thumbnail");
            thumbnail.src = imageurl;  // Set the image source
            thumbnail.style.backgroundPosition = "center";
            thumbnail.style.backgroundSize = "cover";

            // Append the image and details to the new div
            newDiv.appendChild(thumbnail);
            newDiv.appendChild(details);
            newDiv.appendChild(buy);
            
            
            if(pos=="odd")
            {   newDiv.setAttribute('data-aos', 'fade-left');
                newDiv.style.marginRight='-400px';
                newDiv.style.boxShadow="15px 15px 20px rgb(0, 0, 0)";
                pos="even";
            }else{
                newDiv.setAttribute('data-aos', 'fade-right');
                newDiv.style.marginLeft='-400px';
                newDiv.style.boxShadow="-15px 15px 20px rgb(0, 0, 0)";
                pos="odd";
            }

            newDiv.setAttribute('data-aos-duration','1000');
        
            
            // Append the new div to the container
            dest.prepend(newDiv);
            // console.log(routes);

            
        });
        
        // buy= document.getElementById("buy-btn");
        // buy.addEventListener('click',buycourse("rohan")); 
        
    })
    

    
    
    console.log(routes);
    
    
    
    
    
    // fetch('/api/routes')
    // .then(response => response.json())
    // .then(data => {
        //     console.log('Routes:', data);
        //     // Now you can use the routes data in your JavaScript code
        //     data.forEach(route => {
            //         console.log(`Route: ${route.route}, View Function: ${route.view_func}, Template: ${route.template}`);
            //     });
            
            // })
            // .catch(error => console.error('Error fetching routes:', error));
            
            
            
            function addRoute(route, viewFunc, template) {
                const newRoute = {
                    route: route,
                    view_func: viewFunc,
                    template: template
                };
                sendRoutesToFlask(newRoute);
                console.log(newRoute)
                // routes.push(newRoute);
                
            }
            

    // Example usage
    
    // Fetch routes
    function sendRoutesToFlask(routes) {
        fetch('/receive_routes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(routes)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    }    
    // function sendRoutesToFlask(routes) {
        
    //     fetch('/receive_routes', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify(routes)
    //     })
    //     .then(response => response.json())
    //     .then(data => console.log(data))
    //     .catch(error => console.error('Error:', error));
    // }


    
