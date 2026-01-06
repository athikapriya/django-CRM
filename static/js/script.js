function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}


const noteInput = document.querySelector('input[name="note"]');
if (noteInput) {
    noteInput.addEventListener('input', debounce(function() {
        this.form.submit();
    }, 500)); 
}