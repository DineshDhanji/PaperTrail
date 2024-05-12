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