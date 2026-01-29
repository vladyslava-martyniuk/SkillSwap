let allSkills = [];
let currentUserId = null;

window.onload = () => {
    const skillsList = document.getElementById("skillsList");
    const createSkillBtn = document.getElementById("createSkillBtn");
    const applyFilterBtn = document.getElementById("applyFilterBtn");
    const searchInput = document.getElementById("searchSkill");
    const filterCategory = document.getElementById("filterCategory");
    const filterLevel = document.getElementById("filterLevel");
    const greeting = document.getElementById("greeting");

    const loginBtn = document.getElementById("loginBtn");
    const registerBtn = document.getElementById("registerBtn");
    const logoutBtn = document.getElementById("logoutBtn");

    // ---------- AUTH UI ----------
   function setAuthUI(isLoggedIn, username = "") {
    if (isLoggedIn) {
        loginBtn.style.display = "none";
        registerBtn.style.display = "none";
        logoutBtn.style.display = "inline-block";

        loginBox.style.display = "none";
        registerBox.style.display = "none";

        greeting.textContent =
            `Привіт, ${username}! Раді бачити тебе на SkillSwap 🤝`;
    } else {
        loginBtn.style.display = "inline-block";
        registerBtn.style.display = "inline-block";
        logoutBtn.style.display = "none";

        greeting.textContent =
            "Привіт! Увійди або зареєструйся, щоб почати 🚀";
    }

   
    greeting.style.textAlign = "center";       
    greeting.style.fontWeight = "bold";        
    greeting.style.margin = "20px 0";         
    greeting.style.fontSize = "1.2rem";       
}

    // ---------- SHOW / HIDE FORMS ----------
    window.showLogin = () => {
        document.getElementById("loginBox").style.display = "block";
        document.getElementById("registerBox").style.display = "none";
    };

    window.showRegister = () => {
        document.getElementById("loginBox").style.display = "none";
        document.getElementById("registerBox").style.display = "block";
    };

    // ---------- AUTH ----------
    window.register = async () => {
        const data = {
            username: document.getElementById("regUsername").value,
            email: document.getElementById("regEmail").value,
            password: document.getElementById("regPassword").value
        };

        const res = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        document.getElementById("regResult").innerText =
            result.message || result.detail;
    };

    window.login = async () => {
        const data = {
            username: document.getElementById("loginUsername").value,
            password: document.getElementById("loginPassword").value
        };

        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        document.getElementById("loginResult").innerText =
            result.message || result.detail;

        if (res.ok) {
            await loadMe();
            loadSkills();
            document.getElementById("loginBox").style.display = "none";
        }
    };

    async function loadMe() {
        const res = await fetch("/me");

        if (res.ok) {
            const data = await res.json();
            currentUserId = data.id;
            setAuthUI(true, data.username);
        } else {
            currentUserId = null;
            setAuthUI(false);
        }
    }

    window.logout = async () => {
        await fetch("/logout");

        currentUserId = null;
        allSkills = [];
        skillsList.innerHTML = "";

        setAuthUI(false);
    };

    // ---------- SKILLS ----------
    createSkillBtn.onclick = createSkill;

    async function loadSkills() {
        const res = await fetch("/skills");
        if (res.ok) {
            allSkills = await res.json();
            renderSkills(allSkills);
        }
    }

    function renderSkills(skills) {
        skillsList.innerHTML = "";

        skills.forEach(skill => {
            let deleteBtn = "";
            if (currentUserId && skill.user_id === currentUserId) {
                deleteBtn =
                    `<button onclick="deleteSkill(${skill.id})">Видалити</button>`;
            }

            const li = document.createElement("li");
            li.innerHTML = `
                <b>${skill.title}</b> (${skill.category}, ${skill.level})<br>
                ${skill.description}<br>
                Можу навчати: ${skill.can_teach ? "✅" : "❌"},
                Хочу вчитися: ${skill.want_learn ? "✅" : "❌"}
                ${deleteBtn}
            `;
            skillsList.appendChild(li);
        });
    }

    async function createSkill() {
        const data = {
            title: document.getElementById("skillTitle").value,
            description: document.getElementById("skillDesc").value,
            category: document.getElementById("skillCategoryAdd").value,
            level: document.getElementById("skillLevelAdd").value,
            can_teach: document.getElementById("canTeach").checked,
            want_learn: document.getElementById("wantLearn").checked
        };

        const res = await fetch("/skills", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            document.getElementById("skillTitle").value = "";
            document.getElementById("skillDesc").value = "";
            loadSkills();
        } else {
            const err = await res.json();
            alert("Помилка: " + (err.detail || "невідома"));
        }
    }

    window.deleteSkill = async (id) => {
        if (!confirm("Видалити навичку?")) return;

        const res = await fetch(`/skills/${id}`, { method: "DELETE" });
        if (res.ok) loadSkills();
    };

    // ---------- FILTER & SEARCH ----------
    applyFilterBtn.onclick = () => {
        let filtered = [...allSkills];

        const searchVal = searchInput.value.toLowerCase();
        const categoryVal = filterCategory.value;
        const levelVal = filterLevel.value;

        if (searchVal) {
            filtered = filtered.filter(s =>
                s.title.toLowerCase().includes(searchVal) ||
                s.description.toLowerCase().includes(searchVal)
            );
        }

        if (categoryVal)
            filtered = filtered.filter(s => s.category === categoryVal);

        if (levelVal)
            filtered = filtered.filter(s => s.level === levelVal);

        renderSkills(filtered);
    };

    // ---------- INITIAL LOAD ----------
    loadMe();
    loadSkills();
};
