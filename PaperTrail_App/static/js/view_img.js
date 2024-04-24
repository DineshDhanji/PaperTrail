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
var anno = null

document.addEventListener("DOMContentLoaded", () => {
    anno = Annotorious.init({
        image: 'document',
        widgets: [{ widget: AnnotationWidget, force: 'PlainJS' }]
    });

    anno.on('createAnnotation', function (annotation) {
        fun1('Create', annotation)
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

