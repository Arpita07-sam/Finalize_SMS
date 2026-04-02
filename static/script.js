
function registerFunction(){
   window.location.href = "/register";
}

function loginFunction() {
   window.location.href = "/login";
}

/* Verification code */




// function loginUser() {
//     window.location.href = "/dashboard";
// }

// 1. Create a global variable to track status
let passwordReady = false;

function validatePassword() {
    const password = document.getElementById('password').value;
    const hint = document.getElementById('password-hint');

    if (password === "") {
        hint.innerText = "";
        passwordReady = false;
        return;
    }
    // Check conditions
    if (password.length < 8) {
        hint.innerText = "● Must be at least 8 characters";
        passwordReady = false;
    } else if (!/\d/.test(password)) {
        hint.innerText = "● Must include at least one number";
        passwordReady = false;
    } else if (!/[!@#$%^&*]/.test(password)) {
        hint.innerText = "● Must include a special character (@, #, $)";
        passwordReady = false;
    } else {
        hint.innerText = "✔ Password looks strong!";
        hint.style.color = "#2ecc71";
        passwordReady = true; // Only now is it "Ready"
    }

}

function handleFormSubmit(event) {
    if (!passwordReady) {
        event.preventDefault(); // This kills the request before it leaves the browser
        alert("Password is too weak!");
        return false;
    }
}

/* SHOW PASSWORD */

function togglePassword(){
   let pass = document.getElementById("password");
   let btn = document.querySelector(".show-btn");

   if(pass.type === "password"){
      pass.type = "text";
      btn.innerText = "Hide";
   }else{
      pass.type = "password";
      btn.innerText = "Show";
   }
}

function registerUser()
{
    let dept_name = document.getElementById("dept_name").value;
    let dept_id = document.getElementById("dept_id").value;
    let hod_name = document.getElementById("hod_name").value;
    let tech_name = document.getElementById("tech_name").value;

    let email = document.getElementById("email").value;
    let tech_phno = document.getElementById("tech_phno").value;
    let hod_phno = document.getElementById("hod_phno").value;
    let password = document.getElementById("password").value;

    // if(!dept || !email || !phno1 || !phno2 || !password) {
    //     alert("Please fill all fields");
    //     return;
    // }

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            dept_name: dept_name,
            dept_id: dept_id,
            hod_name: hod_name,
            tech_name: tech_name,
            email: email,
            tech_phno: tech_phno,
            hod_phno: hod_phno, 
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {

        alert(data.message);

        if(data.status == "success") {
            window.location.href = "/login";
        }
    })
    .catch(error => console.log(error));
}

async function loginUser() {
    const data = {
        dept_id: document.getElementById("dept_id").value,
        tech_phno: document.getElementById("tech_phno").value,
        password: document.getElementById("password").value
    }

    const response = await fetch("/login", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    })

    const result = await response.json()
    if(result.status == "success") {
        alert("Login successfull..")
        window.location.href = "/dashboard"
    } else {
        alert(result.message)
    }
}

/* LIVE PASSWORD CHECK */

function checkPassword(){

let pass = document.getElementById("password").value;

document.getElementById("length").style.color =
pass.length >= 8 ? "green" : "red";

document.getElementById("upper").style.color =
/[A-Z]/.test(pass) ? "green" : "red";

document.getElementById("number").style.color =
/[0-9]/.test(pass) ? "green" : "red";

document.getElementById("special").style.color =
/[@$!%*?&]/.test(pass) ? "green" : "red";

}


function toggleMenu(){
   let sidebar = document.getElementById("sidebar");
   sidebar.classList.toggle("active");
}

// document.querySelector('.category-header').addEventListener('click', function() {
//     this.parentElement.classList.toggle('active');
    
//     // Toggle showing/hiding the submenu
//     const submenu = this.nextElementSibling;
//     if (submenu.style.display === "block") {
//         submenu.style.display = "none";
//     } else {
//         submenu.style.display = "block";
//     }
// });

// const categoryHeader = document.querySelector('.category-header')
// if(categoryHeader) {
//     categoryHeader.addEventListener('click', function() {
//         this.parentElement.classList.toggle('active')

//         const submenu = this.nextElementSibling
//         if(submenu.style.display === "block") {
//             submenu.style.display = "none"
//         }
//         else {
//             submenu.style.display = "block"
//         }
//     })
// }

function handleMultipleUpload(event) {
    const files = event.target.files;
    const container = document.getElementById('image-list');

    for (let i = 0; i < files.length; i++) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            // Create wrapper
            const wrapper = document.createElement('div');
            wrapper.classList.add('image-wrapper');

            // Create image
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('uploaded-image-rect');

            // Create remove mark
            const removeBtn = document.createElement('button');
            removeBtn.innerHTML = '×';
            removeBtn.classList.add('remove-mark');
            
            // Remove functionality
            removeBtn.onclick = function() {
                wrapper.remove();
            };

            wrapper.appendChild(img);
            wrapper.appendChild(removeBtn);
            container.appendChild(wrapper);
        }
        
        reader.readAsDataURL(files[i]);
    }
    // Clear input so you can re-upload the same image if needed
    event.target.value = "";
}



function submitToDB() {
   // 1. Grab values from the input fields
   const name = document.getElementById('newName').value;
   const category = document.getElementById('newCategory').value;
   const qty = document.getElementById('newQty').value;

   if(!name || !category || !qty) {
      alert("Please fill in all fields");
      return;
   }

   // 2. Logic to send to your database (via Fetch API later)
   console.log("Sending to DB:", { name, category, qty });

   // For now, let's just clear the inputs
   document.getElementById('newName').value = '';
   document.getElementById('newCategory').value = '';
   document.getElementById('newQty').value = '';
   
   alert("Ready to connect to backend!");
}



async function addData() {
    const facultyData = {
        faculty_id: document.getElementById('newName').value.trim(),
        name: document.getElementById('newCategory').value.trim(),
        ph_no: document.getElementById('newQty').value.trim(),
        sub: document.getElementById('newSub').value.trim()
    };

    // empty check
    if (!facultyData.faculty_id || !facultyData.name || !facultyData.ph_no || !facultyData.sub) {
        alert("Fill all fields");
        return;
    }

    // phone validation
    if (facultyData.ph_no.length != 10) {
        alert("Phone number must be 10 digits");
        return;
    }

    // duplicate check from table
    let rows = document.querySelectorAll("#faculty-table-body tr");
    for (let r of rows) {
        let existingID = r.cells[0].innerText;
        let existingPH = r.cells[2].innerText;

        if (existingID == facultyData.faculty_id) {
            alert("ID already exists");
            return;
        }

        if (existingPH == facultyData.ph_no) {
            alert("Phone already exists");
            return;
        }
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/add-faculty', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(facultyData)
        });
        const result = await response.json();
        alert(result.message);
    }
    catch(error) {
        console.error(error);
        alert("Error connecting to Flask");

    }
}

function loadFaculty() {
    console.log("Loading...");
    fetch("http://127.0.0.1:5000/get-faculty")
    .then(res => res.json())
    .then(data => {
        const tableBody = document.getElementById("faculty-table-body");
        tableBody.innerHTML = "";

        data.forEach(f => {
            let row = document.createElement("tr");
            let td1 = document.createElement("td");
            td1.innerText = f.faculty_id;  

            let td2 = document.createElement("td");
            td2.innerText = f.name;
            
            let td3 = document.createElement("td");
            td3.innerText = f.ph_no;
            
            let td4 = document.createElement("td");
            td4.innerText = f.sub;

            let td5 = document.createElement("td");
            td5.innerHTML = `
                <span onclick="editRow(this)">✏️</span>
                &nbsp;
                <span onclick="deleteRow(this)">🗑️</span>
            `;

            row.appendChild(td1);
            row.appendChild(td2);
            row.appendChild(td3);
            row.appendChild(td4);
            row.appendChild(td5);
            tableBody.appendChild(row);
        });
    });
}


function saveData() {
    let rows = document.querySelectorAll("#data-table tbody tr");
    let updatedData = [];
    rows.forEach(row => {
        let cells = row.querySelectorAll("td");
        updatedData.push({
            faculty_id: cells[0].innerText,
            name: cells[1].innerText,
            ph_no: cells[2].innerText,
            sub: cells[3].innerText
        });
    });
    fetch("/update-faculty", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updatedData)
    })
    .then(res => res.json())
    .then(data => {
        alert("Changes saved");
        loadFaculty(); // reload updated data
    });
}

function editRow(icon){
    let row = icon.closest("tr");
    let name = row.children[1];
    let phone = row.children[2];
    let subject = row.children[3];
    // check mode
    if(icon.innerText == "✏️"){
        name.contentEditable = true;
        phone.contentEditable = true;
        subject.contentEditable = true;
        row.style.backgroundColor = "#fff3cd";
        icon.innerText = "💾";
    }
    else{
        let id = row.children[0].innerText;
        let updatedData = {
            name: name.innerText,
            ph_no: phone.innerText,
            sub: subject.innerText
        };
        fetch(`http://127.0.0.1:5000/update-faculty/${id}`,{
            method:"PUT",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify(updatedData)
        });
        name.contentEditable = false;
        phone.contentEditable = false;
        subject.contentEditable = false;
        row.style.backgroundColor = "";
        icon.innerText = "✏️";
    }
}

function deleteRow(icon){
    let row = icon.closest("tr");
    let id = row.children[0].innerText;
    if(!confirm("Delete this record?"))
        return;
    fetch(`http://127.0.0.1:5000/delete-faculty/${id}`,{
        method:"DELETE"
    });
    row.remove();
}

function uploadData() {
    alert("Upload clicked");
}

window.onload = function () {

    const input = document.getElementById("imageInput");
    const preview = document.getElementById("preview");

    let images = [];

    input.addEventListener("change", function (event) {
        const files = Array.from(event.target.files);

        if (images.length + files.length > 20) {
            alert("Maximum 20 images allowed");
            return;
        }

        files.forEach(file => {
            const reader = new FileReader();

            reader.onload = function (e) {
                images.push(e.target.result);
                displayImages();
            };

            reader.readAsDataURL(file);
        });
    });

    function displayImages() {
        preview.innerHTML = "";

        images.forEach((src, index) => {
            const div = document.createElement("div");
            div.className = "image-box";

            const img = document.createElement("img");
            img.src = src;

            const btn = document.createElement("button");
            btn.innerText = "×";
            btn.className = "remove-btn";

            btn.onclick = function () {
                images.splice(index, 1);
                displayImages();
            };

            div.appendChild(img);
            div.appendChild(btn);
            preview.appendChild(div);
        });
    }

};
