var AnnotationWidget = function (args) {
    // 1. Find the annotation, if any
    var currentAnnotation = args.annotation
        ? args.annotation.bodies.find(function (b) {
            return b.purpose == 'annotate'
        })
        : null

    // 2. Keep the annotation's value in a variable
    var currentAnnotationValue = currentAnnotation ? currentAnnotation.value : null

    //// 3. Triggers callbacks on user action
    var addAnnotation = function (evt) {
        if (currentAnnotationValue) {
            const annotation = evt.target.parentNode.querySelector('textarea').value
            if (annotation) {
                args.onUpdateBody(currentAnnotation, {
                    type: 'TextualBody',
                    purpose: 'annotate',
                    value: annotation
                })
            }
        } else {
            const annotation = evt.target.parentNode.querySelector('textarea').value
            if (annotation) {
                args.onAppendBody({
                    type: 'TextualBody',
                    purpose: 'annotate',
                    value: annotation
                })
            }
        }
    }

    // 4. This create the save button.
    var createButton = function () {
        var button = document.createElement('button')
        button.innerText = 'Save'
        button.classList = 'btn btn-dark mx-2 my-3'
        button.addEventListener('click', addAnnotation)
        return button
    }
    // 5. This part create the textarea.
    var createTextarea = function () {
        var annotationTextarea = document.createElement('textarea')
        annotationTextarea.classList = 'r6o-editable-text p-2'
        annotationTextarea.value = currentAnnotationValue
        return annotationTextarea
    }

    var container = document.createElement('div')
    container.className = 'r6o-widget comment editable'

    var annotationTextarea = createTextarea()
    var saveButton = createButton()

    container.appendChild(annotationTextarea)
    container.appendChild(saveButton)
    return container
}

function getCookie(name) {
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
var anno = null

document.addEventListener("DOMContentLoaded", () => {
    anno = Annotorious.init({
        image: 'document',
        widgets: [{ widget: AnnotationWidget, force: 'PlainJS' }]
    });

    anno.on('createAnnotation', function (annotation) {
        createAnnotation(annotation)
    })

    anno.on('updateAnnotation', function (annotation) {
        fun1('Update', annotation)
    })

})

function loadAnnotations(doc_id) {
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

function createAnnotation(annotation) {
    console.log(annotation);
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
        body: JSON.stringify({annotation, doc_id})
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