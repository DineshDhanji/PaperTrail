function getCookie(name = 'csrftoken') {
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