const title = document.querySelectorAll('[data-title]');
const collapse = document.querySelectorAll('[data-id]');

// expand accordion
title.forEach((el) => {
  el.addEventListener('click', (e) => {
    let titleNumber = e.target.dataset.title;

    collapse.forEach((col) => {
      let minus = col.parentElement.firstElementChild.lastElementChild.firstElementChild;

      if(titleNumber === col.dataset.id) {
        col.classList.toggle('show');
        
        minus.classList.toggle('sign-active');
      } else {
        col.classList.remove('show');
        minus.classList.remove('sign-active');
      }
    })
  })
})