document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.querySelector('.light-dark-mode');
    const themeIcon = document.querySelector('.theme-mode-icon');
    
    // Check for saved theme in localStorage
    const savedTheme = localStorage.getItem('theme') || 'light'; // Default to light
    applyTheme(savedTheme);

    // Add event listener to the toggle button
    themeToggle.addEventListener('click', (e) => {
        e.preventDefault();
        const currentTheme = localStorage.getItem('theme') === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', currentTheme);
        applyTheme(currentTheme);
    });

    // Function to apply theme
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.dataset.bsTheme = 'dark';
            themeIcon.classList.replace('ri-sun-line', 'ri-moon-line'); 
        } else {
            document.body.dataset.bsTheme = 'light';
            themeIcon.classList.replace('ri-moon-line', 'ri-sun-line');
        }
    }
});

const getCSRFToken = () => {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.content : '';
};

let currentId;
document.addEventListener('chatOpened', () => {
    const userAddLine = document.querySelector('.ri-user-add-line');
    currentId = userAddLine.id
    const userName = document.getElementById('add-form')
    
    document.getElementById('add-user-btn').addEventListener('click', async ()=>{

        const csrfToken = getCSRFToken();
        try {
                const response = await fetch(`http://127.0.0.1:8000/chat/${currentId}/add_user`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({username: userName.value})
                })
                const data = await response.json()

                if (!response.ok) {
                    console.error("Error:", data.error || "Unknown error");
                }
                console.log(data)

                userName.value = ''
        
        } catch (error) {
            console.error("Fetch error:", error);
        }
        
        })

});


document.getElementById('open-create').addEventListener('click', ()=>{
    console.log('Open')
    document.dispatchEvent(new Event('createGroup'));
})


// Create group



// console.log(createRoomBtn.style.display)

document.addEventListener('createGroup', async ()=>{
    const roomName = document.getElementById('addgroupname-input')
    const roomDesc = document.getElementById('addgroupdescription-input')
    const createRoomBtn = document.getElementById('create-room')

    
    createRoomBtn.addEventListener('click', async()=>{
        
    const url = 'http://127.0.0.1:8000/chat/create'
    try {
        const csrfToken = getCSRFToken();
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                    },
            body: JSON.stringify({room_name: roomName.value, room_desc:roomDesc.value})
        })
        const data = await response.json()
        if (!response.ok) {
            throw new Error("Error creating room");
        }
        console.log(data)
        roomName.value = ''
        roomDesc.value = ''
        window.location.href = window.location.href;
    } catch (error) {
        console.error("Fetch error:", error);
    }
    })

})