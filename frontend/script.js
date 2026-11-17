const API_URL = "http://127.0.0.1:8000";


// =========================================================
// ELEMENTS
// =========================================================

const jobDescription =
    document.getElementById("jobDescription");

const resumes =
    document.getElementById("resumes");

const screenButton =
    document.getElementById("screenButton");

const selectedFiles =
    document.getElementById("selectedFiles");

const loading =
    document.getElementById("loading");

const errorMessage =
    document.getElementById("errorMessage");

const resultsSection =
    document.getElementById("resultsSection");

const candidateResults =
    document.getElementById("candidateResults");

const jobInfo =
    document.getElementById("jobInfo");


// =========================================================
// JOB DESCRIPTION SELECTED
// =========================================================

jobDescription.addEventListener("change", function () {

    console.log(
        "JOB DESCRIPTION:",
        jobDescription.files
    );

});


// =========================================================
// RESUMES SELECTED
// =========================================================

resumes.addEventListener("change", function () {

    selectedFiles.innerHTML = "";

    const files =
        Array.from(resumes.files);

    console.log(
        "RESUMES:",
        files
    );


    if (files.length === 0) {
        return;
    }


    let html = `
        <p class="fw-bold">
            ${files.length} resume(s) selected:
        </p>

        <ul class="list-group">
    `;


    files.forEach(function (file) {

        html += `
            <li class="list-group-item">
                ${escapeHtml(file.name)}
            </li>
        `;

    });


    html += `</ul>`;


    selectedFiles.innerHTML =
        html;

});


// =========================================================
// SCREEN BUTTON
// =========================================================

screenButton.addEventListener(
    "click",
    async function (event) {

        // Prevent any browser default action
        event.preventDefault();

        console.log(
            "================================"
        );

        console.log(
            "SCREEN BUTTON CLICKED"
        );

        console.log(
            "================================"
        );


        // -------------------------------------------------
        // CLEAR OLD RESULTS / ERRORS
        // -------------------------------------------------

        hideError();

        resultsSection.classList.add(
            "d-none"
        );

        candidateResults.innerHTML = "";

        jobInfo.innerHTML = "";


        // -------------------------------------------------
        // CHECK JD
        // -------------------------------------------------

        if (
            !jobDescription.files ||
            jobDescription.files.length === 0
        ) {

            showError(
                "Please select a Job Description."
            );

            return;
        }


        // -------------------------------------------------
        // CHECK RESUMES
        // -------------------------------------------------

        if (
            !resumes.files ||
            resumes.files.length === 0
        ) {

            showError(
                "Please select at least one resume."
            );

            return;
        }


        // -------------------------------------------------
        // CURRENT BACKEND LIMIT
        // -------------------------------------------------

        if (resumes.files.length > 4) {

            showError(
                "Please select a maximum of 4 resumes."
            );

            return;
        }


        // -------------------------------------------------
        // SHOW LOADING
        // -------------------------------------------------

        loading.classList.remove(
            "d-none"
        );

        screenButton.disabled = true;


        // -------------------------------------------------
        // CREATE FORM DATA
        // -------------------------------------------------

        const formData =
            new FormData();


        // JD

        formData.append(
            "job_description",
            jobDescription.files[0]
        );


        // Resumes

        const resumeFiles =
            Array.from(resumes.files);


        for (
            let i = 0;
            i < 4;
            i++
        ) {

            const file =
                resumeFiles[
                    Math.min(
                        i,
                        resumeFiles.length - 1
                    )
                ];


            formData.append(
                `resume${i + 1}`,
                file
            );

        }


        // -------------------------------------------------
        // DEBUG
        // -------------------------------------------------

        console.log(
            "Files being sent:"
        );


        for (
            const [key, value]
            of formData.entries()
        ) {

            console.log(
                key,
                value.name
            );

        }


        // -------------------------------------------------
        // CALL FASTAPI
        // -------------------------------------------------

        try {

            console.log(
                "Sending request to:",
                `${API_URL}/screen`
            );


            const response =
                await fetch(
                    `${API_URL}/screen`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            console.log(
                "HTTP STATUS:",
                response.status
            );


            // ------------------------------------------------
            // READ RESPONSE
            // ------------------------------------------------

            const responseText =
                await response.text();


            console.log(
                "RAW RESPONSE:",
                responseText
            );


            let data;


            try {

                data =
                    JSON.parse(
                        responseText
                    );

            } catch (jsonError) {

                throw new Error(
                    "FastAPI returned an invalid JSON response."
                );

            }


            console.log(
                "PARSED RESPONSE:",
                data
            );


            // ------------------------------------------------
            // API ERROR
            // ------------------------------------------------

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    `API Error: ${response.status}`
                );

            }


            // ------------------------------------------------
            // DISPLAY RESULTS
            // ------------------------------------------------

            displayResults(data);


        } catch (error) {

            console.error(
                "SCREENING ERROR:",
                error
            );


            showError(
                `Screening failed: ${error.message}`
            );


        } finally {

            loading.classList.add(
                "d-none"
            );

            screenButton.disabled =
                false;

        }

    }
);


// =========================================================
// DISPLAY RESULTS
// =========================================================

function displayResults(data) {

    console.log(
        "Displaying results..."
    );


    if (!data) {

        throw new Error(
            "No data received from the API."
        );

    }


    const job =
        data.job_information;


    const candidates =
        data.ranked_candidates;


    if (!job) {

        throw new Error(
            "Job information is missing from API response."
        );

    }


    if (!candidates) {

        throw new Error(
            "Candidate ranking is missing from API response."
        );

    }


    // -----------------------------------------------------
    // JOB INFORMATION
    // -----------------------------------------------------

    jobInfo.innerHTML = `

        <div class="alert alert-primary">

            <h5>
                Job Information
            </h5>

            <strong>
                Job Title:
            </strong>

            ${escapeHtml(
                job.job_title || "Unknown"
            )}

            <br>

            <strong>
                Required Skills:
            </strong>

            ${escapeHtml(
                (job.required_skills || [])
                    .join(", ")
            )}

        </div>

    `;


    // -----------------------------------------------------
    // CANDIDATES
    // -----------------------------------------------------

    if (candidates.length === 0) {

        candidateResults.innerHTML = `

            <div class="alert alert-warning">

                No candidates were returned.

            </div>

        `;

    }


    candidates.forEach(
        function (candidate) {

            const card =
                document.createElement("div");

            card.className =
                "candidate-card";


            card.innerHTML = `

                <div
                    class="d-flex
                           justify-content-between
                           align-items-center
                           mb-4"
                >

                    <div>

                        <span
                            class="badge bg-dark"
                        >

                            Rank #${candidate.rank}

                        </span>

                        <h3 class="mt-2">

                            ${escapeHtml(
                                candidate.name
                            )}

                        </h3>

                    </div>


                    <div class="text-end">

                        <div class="text-muted">

                            Final Score

                        </div>

                        <div class="score">

                            ${candidate.final_score}%

                        </div>

                    </div>

                </div>


                <div class="row g-3 mb-4">

                    ${createScoreBox(
                        "Skill Match",
                        candidate.skill_score
                    )}

                    ${createScoreBox(
                        "Semantic",
                        candidate.semantic_score
                    )}

                    ${createScoreBox(
                        "Experience",
                        candidate.experience_score
                    )}

                    ${createScoreBox(
                        "Education",
                        candidate.education_score
                    )}

                </div>


                <div class="row">

                    <div class="col-md-6">

                        <h5 class="matched">
                            Matched Requirements
                        </h5>

                        ${createMatchedRequirements(
                            candidate.matched_requirements
                        )}

                    </div>


                    <div class="col-md-6">

                        <h5 class="missing">
                            Missing Requirements
                        </h5>

                        ${createMissingRequirements(
                            candidate.missing_requirements
                        )}

                    </div>

                </div>

            `;


            candidateResults.appendChild(
                card
            );

        }
    );


    // -----------------------------------------------------
    // SHOW RESULTS
    // -----------------------------------------------------

    resultsSection.classList.remove(
        "d-none"
    );


    // Scroll automatically to results

    resultsSection.scrollIntoView({
        behavior: "smooth"
    });


    console.log(
        "Results displayed successfully."
    );

}


// =========================================================
// SCORE BOX
// =========================================================

function createScoreBox(
    title,
    score
) {

    return `

        <div class="col-md-3">

            <div class="score-item">

                <div class="text-muted">

                    ${title}

                </div>

                <strong>

                    ${score}%

                </strong>

            </div>

        </div>

    `;

}


// =========================================================
// MATCHED REQUIREMENTS
// =========================================================

function createMatchedRequirements(
    requirements
) {

    if (
        !requirements ||
        requirements.length === 0
    ) {

        return `

            <p class="text-muted">

                No matched requirements.

            </p>

        `;

    }


    return `

        <ul class="list-group">

            ${requirements.map(
                function (item) {

                    return `

                        <li
                            class="list-group-item"
                        >

                            <strong>

                                ${escapeHtml(
                                    item.requirement
                                )}

                            </strong>

                            <br>

                            <small>

                                Matched with:

                                ${escapeHtml(
                                    item.matched_skill
                                )}

                                <br>

                                Similarity:

                                ${item.similarity}

                            </small>

                        </li>

                    `;

                }
            ).join("")}

        </ul>

    `;

}


// =========================================================
// MISSING REQUIREMENTS
// =========================================================

function createMissingRequirements(
    requirements
) {

    if (
        !requirements ||
        requirements.length === 0
    ) {

        return `

            <p class="text-success">

                No missing requirements.

            </p>

        `;

    }


    return `

        <ul class="list-group">

            ${requirements.map(
                function (item) {

                    return `

                        <li
                            class="list-group-item"
                        >

                            <strong>

                                ${escapeHtml(
                                    item.requirement
                                )}

                            </strong>

                        </li>

                    `;

                }
            ).join("")}

        </ul>

    `;

}


// =========================================================
// ERROR
// =========================================================

function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "d-none"
    );

}


function hideError() {

    errorMessage.classList.add(
        "d-none"
    );

}


// =========================================================
// ESCAPE HTML
// =========================================================

function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";

    }


    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}