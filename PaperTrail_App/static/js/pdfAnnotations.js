import { AnnotationWidget } from "./annotationWidget.js";
import { getCookie } from "./utils.js";


export async function fetchAnnotations(doc_id) {
    const fetchAnnotationsURL = `/api/get_annotations/${doc_id}/`;
    try {
        const response = await fetch(fetchAnnotationsURL, {
            method: 'GET',
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data.annos;
    } catch (error) {
        console.error('Fetch error:', error);
        return [];
    }
}
export function createAnnotation(annotation, pageNumber) {
    const doc_id = document.getElementById("pdf-div").dataset.did;
    var csrfToken = getCookie('csrftoken');
    const createAnnotationsURL = '/api/create_annotation/';

    // Send POST request with the annotation data and CSRF token
    fetch(createAnnotationsURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ annotation, doc_id, pageNumber })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Annotation created:', data);
            annotation["id"] = data["anno_id"]
        })
        .catch(error => {
            console.error('Error creating annotation:', error);
            // Handle error
            alert("Something went wrong on the server side.");
            window.location.reload();
        });
}

export function updateAnnotation(annotation, previous) {
    const newValue = annotation["body"][0]["value"]
    const newPosition = annotation["target"]["selector"]["value"]
    const oldValue = previous["body"][0]["value"]
    const oldPosition = previous["target"]["selector"]["value"]

    if (newValue != oldValue || newPosition != oldPosition) {
        const doc_id = document.getElementById("pdf-div").dataset.did;
        var csrfToken = getCookie('csrftoken');
        const updateAnnotationsURL = '/api/update_annotation/';
        // Send POST request with the annotation data and CSRF token
        fetch(updateAnnotationsURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ annotation, doc_id })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Annotation updated:', data);
            })
            .catch(error => {
                console.error('Error creating annotation:', error);
                // Handle error
                alert("Something went wrong on the server side.");
                window.location.reload();
            });
    }
    else {
        return
    }
}

export function deleteAnnotation(annotation) {
    const doc_id = document.getElementById("pdf-div").dataset.did;
    var csrfToken = getCookie('csrftoken');
    const deleteAnnotationsURL = '/api/delete_annotation/';
    // Send POST request with the annotation data and CSRF token
    fetch(deleteAnnotationsURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ annotation, doc_id })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Annotation deleted:', data);
        })
        .catch(error => {
            console.error('Error creating annotation:', error);
            // Handle error
            alert("Something went wrong on the server side.");
            window.location.reload();
        });
}