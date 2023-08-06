document.addEventListener('DOMContentLoaded', () => {

    let toastElList = [].slice.call(document.querySelectorAll('.toast'))
    let toastList = toastElList.map((toastEl) => {
        return new bootstrap.Toast(toastEl)
    })
})