import { AnnotationWidget } from "./annotationWidget.js";
import { getCookie } from "./utils.js";

var anno = null

document.addEventListener("DOMContentLoaded", () => {
    anno = Annotorious.init({
        image: 'document',
        widgets: [{ widget: AnnotationWidget, force: 'PlainJS' }]
    });

    anno.on('createAnnotation', function (annotation) {
        createAnnotation(annotation)
    })

    anno.on('updateAnnotation', function (annotation, previous) {
        updateAnnotation(annotation, previous)
    })

    anno.on('deleteAnnotation', function (annotation) {
        deleteAnnotation(annotation)
    });

})

export function loadAnnotations(doc_id) {
    const getAnnotationsURL = `/api/get_annotations/${doc_id}/`
    fetch(getAnnotationsURL, {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data.annos)
            const annos = data.annos
            annos.forEach(element => {

                let anno_element = {
                    '@context': 'http://www.w3.org/ns/anno.jsonld',
                    type: 'Annotation',
                    body: [
                        {
                            type: 'TextualBody',
                            purpose: 'annotate',
                            value: element.body_value
                        }
                    ],
                    target: {
                        selector: {
                            type: 'FragmentSelector',
                            conformsTo: 'http://www.w3.org/TR/media-frags/',
                            value: element.target_selector_value
                        }
                    },
                    id: element.id
                }

                anno.addAnnotation(anno_element)
            });
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });
}

export function createAnnotation(annotation) {
    const doc_id = document.getElementById("document").dataset.did;
    var csrfToken = getCookie('csrftoken');
    const createAnnotationsURL = '/api/create_annotation/';
    // Send POST request with the annotation data and CSRF token
    fetch(createAnnotationsURL, {
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
        const doc_id = document.getElementById("document").dataset.did;
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
    const doc_id = document.getElementById("document").dataset.did;
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