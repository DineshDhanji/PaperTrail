export function getCookie(name = 'csrftoken') {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if this cookie contains the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function renderloading() {
    const docTable = document.getElementById("doc-table-div");
    docTable.innerText = "";
    docTable.innerHTML = `
                            <div class="d-flex flex-column justify-content-center align-items-center p-5">
                                <div class="spinner-grow text-dark" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                                <div class="lead mt-2">
                                    Kindly wait while we fetch your documents.
                                </div>
                            </div>
                        `;
}

export function fetchDocuments() {
    const documentsURL = "/api/get_documents/";
    console.log("Initiating fetching ...")
    fetch(documentsURL, {
        method: 'GET',
    }).then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok / invalid delete method');
        }
        return response.json();
    })
        .then((data) => {
            const docTable = document.getElementById("doc-table-div");
            docTable.innerText = "";
            const documentFiles = data['docs'];
            if (documentFiles.length === 0) {
                const responseDiv = document.createElement("div");
                responseDiv.innerHTML = `
                                        <div class="alert alert-light" style="margin-bottom: 0;">
                                            <div colspan="5" class="text-secondary text-center">You got no doc ~(>_<。)＼</div>
                                        </div>
                                    `;
                docTable.appendChild(responseDiv);
            } else {
                const tableDiv = document.createElement("table");
                tableDiv.className = "table table-hover table-striped";
                tableDiv.innerHTML = `
                                        <thead>
                                            <tr>
                                            <th scope="col">#</th>
                                            <th scope="col">File Name</th>
                                            <th scope="col">Created</th>
                                            <th scope="col">Type</th>
                                            <th scope="col"></th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        </tbody>
                                    `;
                const tBodyDiv = tableDiv.querySelector("tbody");

                documentFiles.forEach((documentFile, index) => {
                    let trComponent = document.createElement("tr");
                    // Format the date and time
                    const formattedDate = new Date(documentFile.created).toLocaleDateString('en-US');
                    const formattedTime = new Date(documentFile.created).toLocaleTimeString('en-US');
                    trComponent.innerHTML = `
                                            <td>${index + 1}</td>
                                            <td>
                                                <a href="${documentFile.get_doc_link}" class="text-break"><div>${documentFile.doc_name}</div></a>
                                            </td>
                                            <td>${formattedDate}, ${formattedTime}</td>
                                            <td>${documentFile.doc_type}</td>
                                            <td>
                                                <button class="delete-btn btn btn-danger btn-sm"><i class="bi bi-trash3"></i></button>
                                            </td>
                    `;
                    const deleteButton = trComponent.querySelector(".delete-btn");
                    deleteButton.addEventListener("click", () => {
                        deleteDoc(documentFile.pk);
                    });
                    tBodyDiv.appendChild(trComponent);
                });
                docTable.appendChild(tableDiv);
            }
        })
        .catch((error) => {
            console.error('Error while quering documents:', error);
            const docTable = document.getElementById("doc-table-div");
            docTable.innerText = "";
            const errorDiv = document.createElement("div");
            errorDiv.innerHTML = `
                                    <div class="alert alert-danger" role="alert" style="margin-bottom: 0px">
                                        Something went wrong. Unable to query the server at the moment. 
                                    </div>
                                `;
            docTable.appendChild(errorDiv);
        });
    console.log("Fetching has been done by client side.")
}

function deleteDoc(doc_id) {
    const deleteDocURL = `/api/delete_docfile/`
    const csrftoken = getCookie()

    fetch(deleteDocURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ doc_id })
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok / invalid delete method')
            }
            return response.json()
        })
        .then((data) => {
            alert(data['message'])
            window.location.reload()
        })
        .catch((error) => {
            console.error('Error while deleting annotation:', error)
            alert('Something went wrong. Invalid delete method.')
        })
}

export function fetchSharedDocuments() {
    const sharedDocURL = "/api/get_share_docs/";
    console.log("Initiating fetching ...")
    fetch(sharedDocURL, {
        method: 'GET',
    }).then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok / invalid delete method');
        }
        return response.json();
    })
        .then((data) => {
            const docTable = document.getElementById("doc-table-div");
            docTable.innerText = "";
            const documentFiles = data['docs'];
            if (documentFiles.length === 0) {
                const responseDiv = document.createElement("div");
                responseDiv.innerHTML = `
                                        <div class="alert alert-light" style="margin-bottom: 0;">
                                            <div colspan="5" class="text-secondary text-center">No one has shared anyting with you yet ~(>_<。)＼</div>
                                        </div>
                                    `;
                docTable.appendChild(responseDiv);
            } else {
                const tableDiv = document.createElement("table");
                tableDiv.className = "table table-hover table-striped";
                tableDiv.innerHTML = `
                                        <thead>
                                            <tr>
                                            <th scope="col">#</th>
                                            <th scope="col">File Name</th>
                                            <th scope="col">Created</th>
                                            <th scope="col">Type</th>
                                            <th scope="col">Owner</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        </tbody>
                                    `;
                const tBodyDiv = tableDiv.querySelector("tbody");

                documentFiles.forEach((documentFile, index) => {
                    console.log(documentFile)
                    let trComponent = document.createElement("tr");
                    // Format the date and time
                    const formattedDate = new Date(documentFile.created).toLocaleDateString('en-US');
                    const formattedTime = new Date(documentFile.created).toLocaleTimeString('en-US');
                    trComponent.innerHTML = `
                                            <td>${index + 1}</td>
                                            <td>
                                                <a href="/${documentFile.get_doc_link}" class="text-break"><div>${documentFile.doc_name}</div></a>
                                            </td>
                                            <td>${formattedDate}, ${formattedTime}</td>
                                            <td>${documentFile.doc_type}</td>
                                            <td>${documentFile.get_owner_username}</td>
                    `;
                    tBodyDiv.appendChild(trComponent);
                });
                docTable.appendChild(tableDiv);
            }
        })
        .catch((error) => {
            console.error('Error while quering documents:', error);
            const docTable = document.getElementById("doc-table-div");
            docTable.innerText = "";
            const errorDiv = document.createElement("div");
            errorDiv.innerHTML = `
                                    <div class="alert alert-danger" role="alert" style="margin-bottom: 0px">
                                        Something went wrong. Unable to query the server at the moment. 
                                    </div>
                                `;
            docTable.appendChild(errorDiv);
        });
    console.log("Fetching has been done by client side.")
}

export function sharedWith(username, docID) {
    const sharedWithURL = "/api/share_with/";
    const csrftoken = getCookie();

    fetch(sharedWithURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ username, docID })
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Something went wrong.");
            }
            return response.json();
        })
        .then((data) => {
            alert(data['message']);
            window.location.reload();
        })
        .catch((error) => {
            alert(error.message);
        });
}

export function refreshSharedList(doc_id) {
    const parent = document.getElementById("shared-list");
    parent.innerText = "";
    parent.innerHTML = `
                        <div class="d-flex flex-column justify-content-center align-items-center">
                        <div class="spinner-border text-dark" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <div> Fetching entries</div>
                        </div>
    `;

    const sharedListURL = `/api/get_shared_list/${doc_id}/`;
    fetch(sharedListURL, {
        method: 'GET',
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Something went wrong.");
            }
            return response.json();
        })
        .then((data) => {
            parent.innerText = "";
            const users = data['users'];
            if (users.length == 0) {
                const divComponent = document.createElement("div");
                divComponent.className = 'p-2';
                divComponent.innerText = "Not shared."
                parent.append(divComponent);
            }
            else {

                const ulComponent = document.createElement("ul");
                ulComponent.className = "list-group list-group-flush";
                users.forEach(user => {
                    let li = document.createElement("li");
                    li.className = "list-group-item bg-transparent d-flex justify-content-between";
                    li.innerHTML = `
                <div>${user.username}</div>
                <button type="button" id="remove-access-btn"  class="btn btn-outline-danger btn-sm"><i class="bi bi-dash"></i></button>
                                `;
                    li.querySelector("#remove-access-btn").addEventListener("click", () => {
                        removeAccess(user.pk, doc_id);
                    })
                    ulComponent.appendChild(li);
                });
                parent.appendChild(ulComponent);
            }
        })
        .catch((error) => {
            parent.innerHTML = `
                                <div class="alert alert-danger" role="alert">
                                    Sorry, we can't get the user list at the moment.
                                </div>
            `;
        });
}

function removeAccess(userID, docID) {
    const removeAccessURL = `/api/remove_access/`;
    const csrftoken = getCookie();
    fetch(removeAccessURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ userID, docID })
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Something went wrong.");
            }
            return response.json();
        })
        .then((data) => {
            alert(data['message']);
            window.location.reload();
        })
        .catch((error) => {
            alert(error.message);
        });
}

function renderLoading() {
    const outputDiv = document.getElementById("outputDiv");
    outputDiv.innerText = '';
    outputDiv.innerHTML = `
                            <div class="alert alert-light d-flex flex-column justify-content-center align-items-center">
                                <div class="spinner-border text-dark" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            <div class="mt-2">Fetching the results ...</div>
                            </div> 
    `;
}
export function initiateSearchQuery(query, checkboxValues) {
    renderLoading();
    const searchQueryURL = '/api/search_query/';
    const csrftoken = getCookie();
    fetch(searchQueryURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ query, checkboxValues })
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Something went wrong.");
            }
            return response.json();
        })
        .then((data) => {
            console.log(data['message']);
            updateOutputDiv(data['docs'])
        })
        .catch((error) => {
            console.log(error)
            renderError()
        });
}

function updateOutputDiv(documents) {
    const outputDiv = document.getElementById("outputDiv");
    outputDiv.innerText = '';

    if (documents.length === 0) {
        outputDiv.innerHTML = `
        <div class="alert alert-warning">Nothing matches your search query.</div>
        `;
    }
    else {
        const tableDiv = document.createElement("table");
        tableDiv.className = "table table-hover table-striped";
        tableDiv.innerHTML = `
                                        <thead>
                                            <tr>
                                            <th scope="col">#</th>
                                            <th scope="col">File Name</th>
                                            <th scope="col">Created</th>
                                            <th scope="col">Type</th>
                                            <th scope="col">Owner</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        </tbody>
                                    `;
        const tBodyDiv = tableDiv.querySelector("tbody");

        documents.forEach((doc, index) => {
            let trComponent = document.createElement("tr");
            // Format the date and time
            const formattedDate = new Date(doc.created).toLocaleDateString('en-US');
            const formattedTime = new Date(doc.created).toLocaleTimeString('en-US');
            trComponent.innerHTML = `
                                            <td>${index + 1}</td>
                                            <td>
                                                <a href="/${doc.get_doc_link}" class="text-break"><div>${doc.doc_name}</div></a>
                                            </td>
                                            <td>${formattedDate}, ${formattedTime}</td>
                                            <td>${doc.doc_type}</td>
                                            <td>${doc.get_owner_username}</td>
                    `;
            tBodyDiv.appendChild(trComponent);
        });
        outputDiv.append(tableDiv);
    }

}
function renderError() {
    const outputDiv = document.getElementById("outputDiv");
    outputDiv.innerText = '';
    outputDiv.innerHTML = `
    <div class="alert alert-danger">
    <span class="fw-semibold me-2">Server Error:</span>Unable to entertain your query at the moment. ~(>_<。)＼</div>
    `;
}