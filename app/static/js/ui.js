document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const loginMessage = document.getElementById("login-message");
    const logoutButton = document.getElementById("logout-button");

    const userCard = document.getElementById("user-card");
    const guestCard = document.getElementById("guest-card");
    const actions = document.getElementById("actions");
    const output = document.getElementById("output");
    const outputContent = document.getElementById("output-content");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify({
                    email,
                    password,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                loginMessage.textContent = data.detail || "Ошибка входа";
                loginMessage.className = "message error";
                return;
            }

            loginMessage.textContent = "Вход выполнен успешно";
            loginMessage.className = "message success";

            window.location.href = "/ui";
        });
    }

    if (logoutButton) {
        logoutButton.addEventListener("click", async () => {
            await fetch("/auth/logout", {
                method: "POST",
                credentials: "include",
            });

            window.location.href = "/ui/login";
        });
    }

    if (window.location.pathname === "/ui") {
        loadDashboard();
    }

    async function loadDashboard() {
        const response = await fetch("/auth/me", {
            credentials: "include",
        });

        if (!response.ok) {
            showGuestState();
            return;
        }

        const user = await response.json();

        showUserState(user);
        bindActionButtons();
    }

    function showGuestState() {
        if (guestCard) guestCard.classList.remove("hidden");
        if (userCard) userCard.classList.add("hidden");
        if (actions) actions.classList.add("hidden");
        if (logoutButton) logoutButton.classList.add("hidden");
    }

    function showUserState(user) {
        const isAdmin = user.is_admin || user.is_super_admin;

        document.getElementById("user-email").textContent = user.email;
        document.getElementById("user-name").textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById("user-roles").textContent = getUserRoles(user).join(", ");

        userCard.classList.remove("hidden");
        actions.classList.remove("hidden");
        logoutButton.classList.remove("hidden");

        document.querySelectorAll(".auth-only").forEach((element) => {
            element.classList.remove("hidden");
        });

        if (isAdmin) {
            document.querySelectorAll(".admin-only").forEach((element) => {
                element.classList.remove("hidden");
            });
        }
    }

    function getUserRoles(user) {
        const roles = [];

        if (user.is_user) roles.push("Пользователь");
        if (user.is_student) roles.push("Студент");
        if (user.is_teacher) roles.push("Преподаватель");
        if (user.is_admin) roles.push("Администратор");
        if (user.is_super_admin) roles.push("Суперадминистратор");

        return roles.length ? roles : ["Без роли"];
    }

    function bindActionButtons() {
        document.querySelectorAll("[data-action]").forEach((button) => {
            button.addEventListener("click", async () => {
                const action = button.dataset.action;

                if (action === "load-students") {
                    await loadStudents();
                }

                if (action === "load-majors") {
                    await loadMajors();
                }

                if (action === "show-add-student") {
                    await showAddStudentForm();
                }
                if (action === "show-update-student") {
                    await showUpdateStudentForm();
                }
                if (action === "show-add-major") {
                    showForm("add-major-form", "Добавить специальность");
                }

                if (action === "show-delete-student") {
                    showForm("delete-student-form", "Удалить студента");
                }
            });
        });
    }

    async function loadStudents() {
        const response = await fetch("/students", {
            credentials: "include",
        });

        const data = await response.json();

        showResult(data);
    }

    async function loadMajors() {
        const response = await fetch("/majors", {
            credentials: "include",
        });

        const data = await response.json();

        showResult(data);
    }

    function showMessage(message) {
        showResult({
            message,
        });
    }

    function showResult(data) {
        output.classList.remove("hidden");
        outputContent.textContent = JSON.stringify(data, null, 2);
    }
    const formsArea = document.getElementById("forms-area");
const formTitle = document.getElementById("form-title");

function hideAllForms() {
    document.querySelectorAll("#forms-area form").forEach((form) => {
        form.classList.add("hidden");
    });
}

function showForm(formId, title) {
    hideAllForms();

    formsArea.classList.remove("hidden");
    formTitle.textContent = title;

    document.getElementById(formId).classList.remove("hidden");
}

async function showAddStudentForm() {
    await fillMajorsSelect("student-major-id");
    showForm("add-student-form", "Добавить студента");
}

async function showUpdateStudentForm() {
    await fillMajorsSelect("update-student-major-id", true);
    showForm("update-student-form", "Обновить студента");
}

async function fillMajorsSelect(selectId, withEmptyOption = false) {
    const select = document.getElementById(selectId);

    select.innerHTML = "";

    if (withEmptyOption) {
        const emptyOption = document.createElement("option");
        emptyOption.value = "";
        emptyOption.textContent = "Не менять специальность";
        select.appendChild(emptyOption);
    }

    const response = await fetch("/majors", {
        credentials: "include",
    });

    const majors = await response.json();

    majors.forEach((major) => {
        const option = document.createElement("option");
        option.value = major.id;
        option.textContent = `${major.id} — ${major.major_name}`;
        select.appendChild(option);
    });
}   const addMajorForm = document.getElementById("add-major-form");

if (addMajorForm) {
    addMajorForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const response = await fetch("/majors", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                major_name: document.getElementById("major-name").value,
                major_description: document.getElementById("major-description").value || null,
            }),
        });

        const data = await response.json();

        showResult(data);
    });
}

const addStudentForm = document.getElementById("add-student-form");

if (addStudentForm) {
    addStudentForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const response = await fetch("/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                phone_number: document.getElementById("student-phone").value,
                first_name: document.getElementById("student-first-name").value,
                last_name: document.getElementById("student-last-name").value,
                date_of_birth: document.getElementById("student-date-of-birth").value,
                email: document.getElementById("student-email").value,
                address: document.getElementById("student-address").value,
                enrollment_year: Number(document.getElementById("student-enrollment-year").value),
                course: Number(document.getElementById("student-course").value),
                special_notes: document.getElementById("student-special-notes").value || null,
                major_id: Number(document.getElementById("student-major-id").value),
            }),
        });

        const data = await response.json();

        showResult(data);
    });
}

const updateStudentForm = document.getElementById("update-student-form");

if (updateStudentForm) {
    updateStudentForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const studentId = document.getElementById("update-student-id").value;
        const course = document.getElementById("update-student-course").value;
        const majorId = document.getElementById("update-student-major-id").value;

        const body = {};

        if (course) {
            body.course = Number(course);
        }

        if (majorId) {
            body.major_id = Number(majorId);
        }

        const response = await fetch(`/students/${studentId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(body),
        });

        const data = await response.json();

        showResult(data);
    });
}

const deleteStudentForm = document.getElementById("delete-student-form");

if (deleteStudentForm) {
    deleteStudentForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const studentId = document.getElementById("delete-student-id").value;

        const response = await fetch(`/students/${studentId}`, {
            method: "DELETE",
            credentials: "include",
        });

        const data = await response.json();

        showResult(data);
    });
} 
});