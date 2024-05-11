export var AnnotationWidget = function (args) {
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